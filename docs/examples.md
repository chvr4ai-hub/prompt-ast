# Examples

This page provides practical, copy-paste friendly examples that demonstrate
how to use **prompt-ast** to treat prompts as structured Abstract Syntax Trees (ASTs)
instead of raw strings.

The examples focus on real-world usage patterns such as normalization,
serialization, validation, and CLI workflows.

---

## 1. Normalize a prompt (CLI)

Normalize a prompt from inline text:

```bash
prompt-ast normalize "Write a short story about a robot."
```

Normalize a prompt from a file:

```bash
prompt-ast normalize --file prompt.txt
```

---

## 2. Parse and normalize a prompt (Python)

```python
from prompt_ast import parse, normalize

prompt = "Write a haiku about databases."
ast = normalize(parse(prompt))

print(ast)
```

Use this when you want a stable, canonical representation of prompts.

---

## 3. Render AST back to text

```python
from prompt_ast import parse, normalize, render

prompt = """
Write a haiku about databases.

Constraints:
- 5-7-5 syllables
- include the word "index"
"""

ast = normalize(parse(prompt))
print(render(ast))
```

---

## 4. Serialize AST to JSON

Store normalized prompts safely in databases or files.

```python
from prompt_ast import parse, normalize, to_json

prompt = "Summarize this text in 3 bullet points."
ast = normalize(parse(prompt))

data = to_json(ast)
print(data)
```

Restore later:

```python
from prompt_ast import from_json, render

ast = from_json(data)
print(render(ast))
```

---

## 5. Extract placeholders / variables

```python
from prompt_ast import parse, extract_placeholders

prompt = "Write an email to {recipient} about {topic}."
ast = parse(prompt)

variables = extract_placeholders(ast)
print(variables)
```

Typical use cases:
- Validate required inputs
- Generate UI forms dynamically
- Prevent runtime prompt errors

---

## 6. Validate inputs before execution

```python
from prompt_ast import parse, extract_placeholders

def validate(prompt: str, values: dict):
    ast = parse(prompt)
    required = extract_placeholders(ast)
    missing = required - values.keys()
    if missing:
        raise ValueError(f"Missing variables: {missing}")

prompt = "Create a report for {team} covering {period}."
validate(prompt, {"team": "Data"})  # raises ValueError
```

---

## 7. Fill placeholders safely

```python
from prompt_ast import parse, normalize, fill_placeholders, render

template = """
Write a status update.

Project: {project}
Progress: {progress}
Next steps: {next_steps}
"""

values = {
    "project": "prompt-ast",
    "progress": "Added CLI file support",
    "next_steps": "Improve documentation"
}

ast = normalize(parse(template))
filled = fill_placeholders(ast, values)

print(render(filled))
```

---

## 8. Structural diff between prompts

```python
from prompt_ast import parse, normalize, diff

old = "Summarize in 3 bullet points."
new = "Summarize in 5 bullet points."

changes = diff(normalize(parse(old)), normalize(parse(new)))
print(changes)
```

This avoids noisy string-based diffs.

---

## 9. Normalize lists and formatting

```python
from prompt_ast import normalize, render

prompt = """
Steps:
* First step
- Second step
• Third step
"""

print(render(normalize(prompt)))
```

---

## 10. Batch normalization & fingerprinting

```python
from prompt_ast import normalize, to_json
import json, hashlib

def fingerprint(prompt: str) -> str:
    ast = normalize(prompt)
    raw = json.dumps(to_json(ast), sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

prompts = [
    "Summarize in 3 bullets.",
    "Summarize   in 3 bullets.",
]

for p in prompts:
    print(fingerprint(p), p)
```

Useful for deduplication and prompt versioning.

---

## Recommended workflow

1. Parse prompt → AST  
2. Normalize AST → canonical form  
3. Store AST (JSON)  
4. Render only when needed  
5. Diff ASTs instead of strings  

---

More examples will be added as the project evolves.
