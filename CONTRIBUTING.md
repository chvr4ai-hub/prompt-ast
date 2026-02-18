# Contributing to prompt-ast

Thank you for your interest in contributing to **prompt-ast** 🎉  
Contributions of all kinds are welcome — code, documentation, ideas, and feedback.

This project aims to stay **lean, readable, and composable**, so contributions
should align with that philosophy.

---

## Ways to Contribute

You can help in many ways:

- 🧠 Improve heuristic prompt parsing
- 🧪 Add test cases with real-world prompts
- 📚 Improve documentation or examples
- 🐛 Report bugs or edge cases
- 💡 Propose schema or design improvements
- 🧹 Refactor for clarity and maintainability

If you’re unsure where to start, look for issues labeled  
**`good first issue`** or open a discussion.

---

## Development Setup

### Prerequisites
- Python **3.11+**
- Poetry **2.x**

### Clone and install

```bash
git clone https://github.com/<your-username>/prompt-ast.git
cd prompt-ast
poetry install
````

### Run tests

```bash
poetry run pytest
```

### Add heuristic fixtures

Heuristic golden fixtures live in `tests/fixtures.py` and snapshot validation is in
`tests/test_fixtures.py`.

When adding or updating fixtures:

* Keep each fixture shape consistent: `description`, `domain`, `prompt`, `expected_ast`
* Use one of the supported domain values:
  `software`, `data`, `content`, `education`, `business`, `creative`, `research`, `general`
* Regenerate `expected_ast` from actual parser behavior (or update parser + fixture together)
* Run fixture-focused tests before opening a PR:

```bash
poetry run pytest tests/test_fixtures.py
```

If heuristic behavior changes intentionally, update fixtures in the same PR so snapshots
document the new behavior.

### Run linting

```bash
poetry run ruff check .
```

### Run the CLI locally

```bash
poetry run prompt-ast normalize "Act as a CTO. Be concise." --mode heuristic
```

---

## Project Structure

```
prompt_ast/
  ast.py          # Prompt AST schema
  parse/          # Heuristic + LLM parsing
  cli.py          # CLI entry point
  formats.py      # JSON/YAML serialization
tests/            # Unit tests
```

* **`ast.py`** defines the canonical schema
* **`parse/`** contains all parsing logic
* **`cli.py`** should stay thin and focused
* Tests should be added alongside behavior changes

---

## Contribution Guidelines

Please follow these principles:

### 1. Keep it simple

* Avoid introducing heavy abstractions
* Prefer clarity over cleverness
* This is a foundational library, not a framework

### 2. One change per PR

* Small, focused pull requests are easier to review
* Large refactors should be discussed first

### 3. Tests matter

* Add or update tests for behavior changes
* Especially for heuristic parsing improvements

### 4. Backward compatibility

* Avoid breaking the schema without discussion
* Schema changes should be additive where possible

---

## Schema Changes

The Prompt AST schema is intentionally minimal.

If you propose:

* new fields
* field renames
* semantic changes

Please open an issue first to discuss motivation and impact.

---

## Reporting Issues

When reporting a bug, please include:

* the prompt text
* expected behavior
* actual behavior
* Python version
* prompt-ast version

This helps reproduce issues quickly.

---

## Code Style

* Follow existing code style
* Run `ruff` before submitting
* Type hints are encouraged
* Keep functions small and readable

---

## Communication & Respect

This project follows a **Code of Conduct**.
Please be respectful, constructive, and collaborative.

Healthy discussion and disagreement are welcome — personal attacks are not.

---

## License

By contributing to this project, you agree that your contributions will be
licensed under the **MIT License**.

---

## Thank You ❤️

Open source is built by people who care.
Whether you submit a PR, open an issue, or share feedback — thank you for helping
make `prompt-ast` better.
