"""Text normalization helpers."""

import re
import unicodedata


def normalize(text: str) -> str:
    """Normalize user text for matching while preserving readable words."""
    text = unicodedata.normalize("NFKC", text).casefold().strip()
    text = re.sub(r"[^\w\s']", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def words(text: str) -> list[str]:
    return normalize(text).split()
