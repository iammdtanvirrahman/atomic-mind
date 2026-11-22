"""Load and validate JSON dialogue scripts."""

import json
from pathlib import Path
from typing import Any


class ScriptError(ValueError):
    """Raised when a dialogue script is invalid."""


def load_script(path: str | Path) -> dict[str, Any]:
    script_path = Path(path)
    try:
        data = json.loads(script_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ScriptError(f"Script not found: {script_path}") from exc
    except json.JSONDecodeError as exc:
        raise ScriptError(f"Invalid JSON in {script_path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ScriptError("The script root must be a JSON object.")
    if not isinstance(data.get("rules", []), list):
        raise ScriptError("'rules' must be a list.")
    if not isinstance(data.get("fallback", []), list):
        raise ScriptError("'fallback' must be a list.")

    for index, rule in enumerate(data.get("rules", [])):
        if not isinstance(rule, dict):
            raise ScriptError(f"Rule {index} must be an object.")
        if not rule.get("keywords") and not rule.get("pattern"):
            raise ScriptError(f"Rule {index} needs 'keywords' or 'pattern'.")
        if not isinstance(rule.get("responses", []), list) or not rule.get("responses"):
            raise ScriptError(f"Rule {index} needs a non-empty 'responses' list.")
    return data
