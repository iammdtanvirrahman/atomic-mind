"""Command-line entry point for ATOMIC MIND."""

import argparse
from pathlib import Path

from .engine import ConversationEngine
from .scripts import ScriptError, load_script


def main() -> None:
    parser = argparse.ArgumentParser(description="ATOMIC MIND conversational engine")
    parser.add_argument(
        "--script",
        default=str(Path(__file__).resolve().parent.parent / "scripts" / "default.json"),
        help="Path to a JSON conversation script",
    )
    args = parser.parse_args()

    try:
        engine = ConversationEngine(load_script(args.script))
    except ScriptError as exc:
        parser.error(str(exc))

    print(f"ATOMIC MIND — {engine.script.get('name', 'Default personality')}")
    print("Type /quit to exit. Type /help for commands.")
    while True:
        try:
            user_text = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nATOMIC MIND: Session ended.")
            break

        if user_text.casefold() in {"/quit", "/exit"}:
            print("ATOMIC MIND: Goodbye.")
            break
        if user_text.casefold() == "/help":
            print("Commands: /help, /quit, /exit")
            continue
        result = engine.respond(user_text)
        print(f"ATOMIC MIND: {result.text}")


if __name__ == "__main__":
    main()
