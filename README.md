# ATOMIC MIND

A modular, script-driven conversational AI engine inspired by classic ELIZA systems.

**Principle:** Understand → Match → Reason → Respond → Remember

## Project status

**v0.1.0 — foundation release**

This first version is a deterministic, rule-based conversational engine. It does not claim to be a neural language model or possess human-like understanding. Its purpose is to provide a transparent, extensible core that can later connect to optional language models and external tools.

## Features

- Configurable JSON conversation scripts
- Keyword and pattern matching
- Capture groups and response templates
- Rule priorities and deterministic response selection
- Basic session memory and conversation history
- Simple CLI interface
- No external runtime dependencies

## Requirements

- Python 3.10+

## Run

```bash
python -m atomic_mind
```

Or:

```bash
python -m atomic_mind --script scripts/default.json
```

## Project layout

```
atomic-mind/
├── atomic_mind/
│   ├── __init__.py
│   ├── __main__.py
│   ├── engine.py
│   ├── memory.py
│   ├── normalizer.py
│   └── scripts.py
├── scripts/
│   └── default.json
├── tests/
│   └── test_engine.py
├── pyproject.toml
└── README.md
```

## Conversation script format

A script is JSON with a name, fallback responses, and ordered rules. Each rule can define keywords, a regular-expression pattern, priority, and response templates. Templates may use `{1}`, `{2}` for regex capture groups and `{input}` for the normalized user input.

Example:

```json
{
  "name": "Example",
  "fallback": ["Tell me more about that."],
  "rules": [
    {
      "keywords": ["hello", "hi"],
      "priority": 10,
      "responses": ["Hello. What would you like to discuss?"]
    },
    {
      "pattern": "\\bmy name is (.+)",
      "priority": 20,
      "responses": ["Nice to meet you, {1}."]
    }
  ]
}
```

## Roadmap

- [x] Core rule engine and JSON scripts
- [x] Basic session memory
- [x] Command-line chat loop
- [ ] Synonym groups and ELIZA-style decomposition/reassembly
- [ ] Multiple named personalities and script switching
- [ ] Persistent memory storage
- [ ] Plugin/tool interface with permission boundaries
- [ ] Optional LLM adapter
- [ ] Android interface

## Design principles

1. Keep the core small and understandable.
2. Keep personality and dialogue content outside Python code.
3. Make rule execution inspectable and testable.
4. Treat memory as explicit stored data, not assumed understanding.
5. Keep external model and plugin integrations optional.

## License

License not yet selected.
