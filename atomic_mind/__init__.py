"""ATOMIC MIND: a modular, script-driven conversational engine."""

__version__ = "0.1.0"

from .engine import ConversationEngine, EngineResponse
from .memory import SessionMemory
from .scripts import load_script

__all__ = ["ConversationEngine", "EngineResponse", "SessionMemory", "load_script"]
