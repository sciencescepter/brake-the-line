"""Tag one fault message with the language model, validated by the Pydantic schema.

Every answer goes through validate_triage(). An invalid answer is sent back to
the model with the validation error and retried. If it is still invalid after
the last attempt the message is flagged for a person to review. It is never
accepted as it is.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Protocol

from pydantic import ValidationError

from .prompt import SYSTEM_PROMPT, retry_prompt, user_prompt
from .schema import FaultMessage, TriageResult, validate_triage

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MAX_ATTEMPTS = 3
# Room for the model's reasoning plus a ~100-token JSON answer.
MAX_TOKENS = 3000


class DailyLimitReached(RuntimeError):
    """The provider's daily request cap is used up. Stop the run; resume later."""


class ChatFn(Protocol):
    """Takes a chat message list, returns the model's raw text answer."""

    def __call__(self, messages: list[dict[str, str]]) -> str: ...


@dataclass
class TagOutcome:
    message: FaultMessage
    result: TriageResult | None          # None when flagged
    attempts: int
    errors: list[str] = field(default_factory=list)  # one entry per failed attempt

    @property
    def flagged(self) -> bool:
        return self.result is None


def _response_format() -> dict:
    """JSON schema for structured outputs, built from the Pydantic model."""
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "triage_result",
            "strict": True,
            "schema": TriageResult.model_json_schema(),
        },
    }


def openrouter_chat(model: str | None = None, api_key: str | None = None) -> ChatFn:
    """A ChatFn that calls OpenRouter. Reads OPENROUTER_API_KEY / OPENROUTER_MODEL."""
    from openai import OpenAI

    key = api_key or os.environ.get("OPENROUTER_API_KEY", "").strip()
    model = model or os.environ.get("OPENROUTER_MODEL", "").strip()
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY is not set (put it in .env)")
    if not model:
        raise RuntimeError("OPENROUTER_MODEL is not set (put it in .env)")

    client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=key, max_retries=4, timeout=120)
    fmt = _response_format()

    def chat(messages: list[dict[str, str]]) -> str:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
            max_tokens=MAX_TOKENS,
            response_format=fmt,
            extra_body={"provider": {"require_parameters": True}},
        )
        return resp.choices[0].message.content or ""

    chat.model = model  # type: ignore[attr-defined]
    return chat


def _short_error(e: Exception) -> str:
    """Error type, status and first sentence only: no URLs or account details in logs."""
    import re
    text = re.sub(r"https?://\S+", "<url>", str(e)).split(". ")[0]
    return f"{type(e).__name__}: {text[:160]}"


def _strip_fences(text: str) -> str:
    """Remove ```json fences if a model adds them; the JSON itself is untouched."""
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else ""
        if t.rstrip().endswith("```"):
            t = t.rstrip()[:-3]
    return t.strip()


def tag_message(msg: FaultMessage, chat: ChatFn, max_attempts: int = MAX_ATTEMPTS) -> TagOutcome:
    """Ask the model for a tag, validate it, retry with the error, or flag."""
    convo: list[dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt(msg)},
    ]
    errors: list[str] = []
    for attempt in range(1, max_attempts + 1):
        try:
            raw = chat(convo)
        except Exception as e:  # network / API error: count it as a failed attempt
            if "per-day" in str(e):
                raise DailyLimitReached(_short_error(e)) from e
            errors.append(f"attempt {attempt}: API error: {_short_error(e)}")
            time.sleep(2 * attempt)
            continue
        try:
            result = validate_triage(_strip_fences(raw), msg)
            return TagOutcome(msg, result, attempt, errors)
        except ValidationError as e:
            detail = "; ".join(err["msg"] for err in e.errors())
            errors.append(f"attempt {attempt}: {detail}")
            convo += [
                {"role": "assistant", "content": raw},
                {"role": "user", "content": retry_prompt(detail)},
            ]
    return TagOutcome(msg, None, max_attempts, errors)
