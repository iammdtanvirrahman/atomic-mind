"""Deterministic rule-based conversation engine."""

import re
from dataclasses import dataclass
from typing import Any

from .memory import SessionMemory
from .normalizer import normalize


@dataclass
class EngineResponse:
    text: str
    rule_id: str | None = None
    matched: bool = False


class ConversationEngine:
    """Matches user input against ordered JSON rules and response templates.

    This is symbolic pattern matching, not a neural language model.
    """

    def __init__(self, script: dict[str, Any], memory: SessionMemory | None = None) -> None:
        self.script = script
        self.memory = memory or SessionMemory()
        self._rules = sorted(
            enumerate(script.get("rules", [])),
            key=lambda pair: int(pair[1].get("priority", 0)),
            reverse=True,
        )
        self._response_cursors: dict[int, int] = {}

    def respond(self, user_text: str) -> EngineResponse:
        cleaned = normalize(user_text)
        if not cleaned:
            return EngineResponse("Please enter a message.")

        for original_index, rule in self._rules:
            match = self._match(rule, cleaned)
            if match is None:
                continue
            captures = match
            template = self._next_response(original_index, rule.get("responses", []))
            values = {str(i + 1): value for i, value in enumerate(captures)}
            values["input"] = cleaned
            values["last_user"] = self._last_user_text()
            try:
                answer = template.format_map(_SafeFormat(values))
            except (ValueError, AttributeError):
                answer = template
            self.memory.add("user", user_text)
            self.memory.add("assistant", answer)
            return EngineResponse(answer, str(rule.get("id", original_index)), True)

        fallback = self.script.get("fallback") or ["Tell me more about that."]
        answer = self._next_response(-1, fallback)
        self.memory.add("user", user_text)
        self.memory.add("assistant", answer)
        return EngineResponse(answer)

    def _match(self, rule: dict[str, Any], text: str) -> list[str] | None:
        pattern = rule.get("pattern")
        if pattern:
            found = re.search(str(pattern), text, flags=re.IGNORECASE)
            if found:
                return list(found.groups())
            return None

        keywords = [normalize(str(item)) for item in rule.get("keywords", [])]
        for keyword in keywords:
            if keyword and re.search(r"(?<!\w)" + re.escape(keyword) + r"(?!\w)", text):
                return []
        return None

    def _next_response(self, rule_index: int, responses: list[str]) -> str:
        if not responses:
            return "I am listening."
        cursor = self._response_cursors.get(rule_index, 0)
        self._response_cursors[rule_index] = cursor + 1
        return str(responses[cursor % len(responses)])

    def _last_user_text(self) -> str:
        for turn in reversed(self.memory.recent(20)):
            if turn.role == "user":
                return turn.text
        return ""


class _SafeFormat(dict):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"
