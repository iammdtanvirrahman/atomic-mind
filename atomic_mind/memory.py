"""Small explicit session-memory store."""

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Turn:
    role: str
    text: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SessionMemory:
    """Keeps a bounded conversation history and explicit key/value facts."""

    def __init__(self, max_turns: int = 40) -> None:
        self.history: deque[Turn] = deque(maxlen=max_turns)
        self.facts: dict[str, str] = {}

    def add(self, role: str, text: str) -> None:
        self.history.append(Turn(role=role, text=text))

    def remember(self, key: str, value: str) -> None:
        self.facts[key.strip().casefold()] = value.strip()

    def recall(self, key: str) -> str | None:
        return self.facts.get(key.strip().casefold())

    def recent(self, limit: int = 6) -> list[Turn]:
        return list(self.history)[-limit:]
