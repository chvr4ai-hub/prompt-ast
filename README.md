# 📦 `prompt-ast`

> **Parse human prompts into a canonical, structured Prompt AST.**

`prompt-ast` is a lightweight Python library that converts free-form human prompts into a **Prompt Abstract Syntax Tree (AST)** — a clean, machine-friendly representation that captures intent, constraints, and expected output.

It treats prompts as **first-class artifacts**, not just strings.

---

## ✨ Why `prompt-ast`?

Modern LLM workflows rely heavily on prompts — but prompts today are:

* unstructured text
* hard to analyze or validate
* difficult to reuse or compare
* tightly coupled to specific tools or models

`prompt-ast` introduces a **foundational layer** that sits *before* agents, chains, or LLM calls:

```
Human Prompt
     ↓
Prompt AST (this library)
     ↓
LLM / Agent / Tooling
```

By normalizing prompts into a canonical structure, you unlock better tooling, governance, and reuse — without forcing opinions on how prompts are stored or executed.

---

## 🧠 What is a Prompt AST?

Inspired by compiler ASTs, a **Prompt AST** is an abstract, structured representation of a prompt.

Example:

**Input**

```text
Act as a CTO. Be concise. Explain risks of migrating MySQL to RDS.
```

**Output (JSON)**

```json
{
  "version": "0.1",
  "raw": "Act as a CTO. Be concise. Explain risks of migrating MySQL to RDS.",
  "role": "CTO",
  "context": null,
  "task": "Explain risks of migrating MySQL to RDS",
  "constraints": [
    "Be concise"
  ],
  "assumptions": [],
  "ambiguities": [],
  "output_spec": {
    "format": null,
    "structure": [],
    "language": null
  },
  "metadata": {
    "extracted_by": "heuristic",
    "confidence": 0.55
  }
}
```

---

## 🚀 Features

* ✅ Parse free-form prompts into a canonical AST
* ✅ Heuristic (offline) parsing — no API key required
* ✅ Optional LLM-assisted parsing (pluggable)
* ✅ JSON and YAML export
* ✅ CLI and Python API
* ✅ Minimal, extensible schema
* ✅ Stateless by design (you own storage, versioning, governance)

---

## 📦 Installation

```bash
pip install prompt-ast
```

Optional extras:

```bash
pip install prompt-ast[yaml]     # YAML export
pip install prompt-ast[openai]   # OpenAI-compatible LLM parsing
pip install prompt-ast[all]
```

---

## 🧪 Quick Start (Python)

```python
from prompt_ast import parse_prompt

ast = parse_prompt(
    "Act as a senior backend architect. Be concise. Explain system design trade-offs.",
    mode="heuristic"
)

print(ast.to_json())
```

---

## � Documentation

For more detailed documentation, see the [docs](./docs/) folder:

- **[Concepts](./docs/concepts.md)** — Core concepts and terminology
- **[CLI Usage](./docs/cli.md)** — Command-line interface reference
- **[Examples](./docs/examples.md)** — Real-world usage examples

---

## �🖥 CLI Usage

```bash
prompt-ast normalize \
  "Act as a CTO. Be concise." \
  --mode heuristic \
  --format json
```

LLM-assisted mode (optional):

```bash
export OPENAI_API_KEY=...
prompt-ast normalize \
  "Design a scalable data pipeline." \
  --mode hybrid \
  --use-openai
```

---

## 🧩 Design Principles

`prompt-ast` is intentionally **lean**:

* ❌ No storage
* ❌ No prompt registry
* ❌ No agent framework
* ❌ No vendor lock-in

Instead, it provides a **clean abstraction** that other systems can build on.

This makes it ideal for:

* internal tooling
* prompt governance pipelines
* evaluation frameworks
* AI platform teams
* research & experimentation

---

## 🛣 Roadmap / Future Scope

The current version focuses on **core normalization**. Planned and possible future directions include:

### Near-term

* Improved heuristic extraction accuracy
* Better ambiguity detection
* Schema refinements based on real-world usage
* More LLM adapters (Anthropic, local models)

### Mid-term (opt-in tooling)

* Prompt linting (missing task, conflicting constraints)
* Prompt diffs (semantic-ish comparison)
* Prompt fingerprints / hashes
* Validation rules

### Long-term (out of scope for core)

* Prompt registries
* Governance workflows
* Evaluation frameworks
* UI tooling

> These are intentionally *not* bundled into the core library.

---

## 🤝 Contributing

Contributions are very welcome — especially in these areas:

* Improving heuristic parsing
* Adding test fixtures (real-world prompts)
* Refining the schema
* Documentation improvements
* CLI UX enhancements

### Getting started

```bash
git clone https://github.com/<your-username>/prompt-ast.git
cd prompt-ast
poetry install
poetry run pytest
```

Please:

* keep changes small and focused
* add tests for behavior changes
* avoid introducing heavy dependencies

Open an issue before large changes — discussion is encouraged.

If you’re new to the project, check issues labeled **good first issue** —
they are small, well-scoped tasks ideal for first-time contributors.


---

## 📜 License

**MIT License**

This project is released under the MIT License, which means:

* ✅ Free for personal and commercial use
* ✅ Permissive and business-friendly
* ✅ Attribution required
* ❌ No warranty provided

Perfect for individual contributors and early open-source traction.

(See `LICENSE` file for full text.)

---

## 🌱 Why this project exists

Prompts are becoming one of the most important interfaces in modern software — yet they lack the basic tooling we take for granted in other domains.

`prompt-ast` is an attempt to provide a **small, composable foundation** that the ecosystem can build upon.

If that resonates with you, you’re in the right place.

---

## ⭐ Support the project

If you find this useful:

* ⭐ Star the repo
* 🐛 Report issues
* 💡 Share ideas
* 🧑‍💻 Contribute code
