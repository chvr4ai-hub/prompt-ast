from __future__ import annotations

import re
from ..ast import PromptAST


ROLE_PATTERNS = [
    r"\bact as (an? )?(?P<role>[^.\n]+)",
    r"\byou are (an? )?(?P<role>[^.\n]+)",
    r"\bas a(n)? (?P<role>[^,\n.]+)",
]


def parse_prompt_heuristic(text: str) -> PromptAST:
    raw = text.strip()
    ast = PromptAST(raw=raw)

    # 1) role
    ast.role = _infer_role(raw)

    # 2) labeled sections (Context/Task/Constraints/Output)
    sections = _split_labeled_sections(raw)
    if sections.get("context"):
        ast.context = sections["context"].strip() or None

    # Prefer explicit task, else infer
    if sections.get("task"):
        ast.task = sections["task"].strip() or None
    else:
        ast.task = _infer_task(raw)

    # Constraints
    if sections.get("constraints"):
        ast.constraints.extend(_lines_to_items(sections["constraints"]))

    # Output section -> usually constraints + output format hints
    if sections.get("output") or sections.get("result"):
        out_text = (sections.get("output") or sections.get("result") or "").strip()
        if out_text:
            ast.constraints.extend(_lines_to_items(out_text))

    # 3) infer output format + constraints from common phrases
    lowered = raw.lower()
    fmt = _infer_output_format(lowered)
    if fmt:
        ast.output_spec.format = fmt

    ast.constraints.extend(_infer_constraints(lowered))

    # Extract output structure if specified
    structure = _extract_output_structure(raw)
    if structure:
        ast.output_spec.structure = structure

    # 4) infer ambiguities
    ast.ambiguities.extend(_infer_ambiguities(raw, ast))

    # 5) dedupe for stability
    ast.constraints = _dedupe(ast.constraints)
    ast.ambiguities = _dedupe(ast.ambiguities)

    # MVP metadata
    ast.metadata.setdefault("extracted_by", "heuristic")
    ast.metadata.setdefault("confidence", 0.55)

    return ast


def _infer_role(text: str) -> str | None:
    lowered = text.lower()
    for pat in ROLE_PATTERNS:
        m = re.search(pat, lowered, flags=re.IGNORECASE)
        if m and m.groupdict().get("role"):
            role = m.group("role").strip().rstrip(".")
            # Keep original casing roughly by slicing from original text if possible
            return role
    return None


def _split_labeled_sections(text: str) -> dict[str, str]:
    """
    Enhanced section splitter supporting:
    - Standard: Context: ... / Task: ... / Constraints: ... / Output: ... / Result: ...
    - Markdown: ## Context / ## Task / ## Constraints / ## Output / ## Result
    - Numbered: 1. Context: ... / 2. Task: ... / 3. Constraints: ...
    - Aliases: Background→Context, Goal→Task, Requirements→Constraints
    """
    # Section aliases mapping
    aliases = {
        "background": "context",
        "goal": "task",
        "requirements": "constraints",
        "requirement": "constraints",
    }

    # Combined pattern for all formats
    # Matches: "Context:", "## Context", "1. Context:", "Background:", etc.
    pattern = r"(?im)^(?:#+\s*|\d+\.\s*)?(context|task|constraints|output|result|background|goal|requirements?)\s*:?\s*$"

    lines = text.split("\n")
    sections: dict[str, list[str]] = {}
    current_section: str | None = None

    for line in lines:
        # Check if this line is a section header
        match = re.match(pattern, line.strip())
        if match:
            section_name = match.group(1).lower()
            # Apply alias mapping
            section_name = aliases.get(section_name, section_name)
            current_section = section_name
            if current_section not in sections:
                sections[current_section] = []
        elif current_section:
            # Add content to current section
            stripped = line.strip()
            if stripped:  # Only add non-empty lines
                sections[current_section].append(line)

    # Join multi-line sections
    out: dict[str, str] = {}
    for section, lines_list in sections.items():
        if lines_list:
            out[section] = "\n".join(lines_list).strip()

    return out


def _infer_task(text: str) -> str | None:
    """
    MVP task inference:
    - first meaningful line that is not only persona-setting
    """
    for line in text.splitlines():
        striped = line.strip()
        if not striped:
            continue
        lower = striped.lower()
        if "act as" in lower or "you are" in lower:
            continue
        return striped.rstrip(".")
    return None


def _lines_to_items(text: str) -> list[str]:
    items = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        s = re.sub(r"^[-*•]\s*", "", s)
        items.append(s)
    return items


def _extract_output_structure(text: str) -> list[str]:
    """
    Extract output structure specifications like:
    - 'with sections: A, B, C'
    - 'include: X, Y, Z'
    - 'Output: ... with: P, Q, R'
    """
    structure = []

    # Pattern: "with sections: A, B, C" or "sections: A, B, C"
    sections_match = re.search(
        r"(?:with\s+)?sections?\s*:\s*([^.\n]+)", text, re.IGNORECASE
    )
    if sections_match:
        parts = sections_match.group(1).split(",")
        structure.extend([p.strip() for p in parts if p.strip()])

    # Pattern: "with: A, B, C" or "include: A, B, C"
    with_match = re.search(r"(?:with|include)\s*:\s*([^.\n]+)", text, re.IGNORECASE)
    if with_match and not sections_match:  # Don't double-count
        parts = with_match.group(1).split(",")
        # Only add if they look like section names (capitalized, short)
        potential = [p.strip() for p in parts if p.strip()]
        if all(len(p.split()) <= 4 and p[0].isupper() for p in potential if p):
            structure.extend(potential)

    return structure


def _infer_output_format(lowered: str) -> str | None:
    if "json" in lowered:
        return "json"
    if "yaml" in lowered:
        return "yaml"
    if "markdown" in lowered:
        return "markdown"
    if "table" in lowered:
        return "table"
    return None


def _infer_constraints(lowered: str) -> list[str]:
    out = []
    if "step-by-step" in lowered or "step by step" in lowered:
        out.append("Provide step-by-step output")
    if "concise" in lowered or "brief" in lowered:
        out.append("Be concise")
    if "detailed" in lowered:
        out.append("Be detailed")
    if "bullet" in lowered:
        out.append("Use bullet points")

    # Audience specifications
    if "for beginners" in lowered or "beginner" in lowered:
        out.append("For beginners")
    if "for experts" in lowered or "expert" in lowered:
        out.append("For experts")
    if "eli5" in lowered or "like i'm 5" in lowered or "like i'm five" in lowered:
        out.append("Explain like I'm 5")

    # Tone requirements
    if "professional tone" in lowered or "professionally" in lowered:
        out.append("Professional tone")
    if "casual" in lowered and "tone" in lowered:
        out.append("Casual tone")
    if "engaging" in lowered:
        out.append("Engaging")
    if "creative" in lowered:
        out.append("Creative")
    if "catchy" in lowered:
        out.append("Catchy")
    if "interactive" in lowered:
        out.append("Interactive")

    # Word/character limits
    word_limit_match = re.search(r"(in|under|within)\s+(\d+)\s+words?", lowered)
    if word_limit_match:
        out.append(f"{word_limit_match.group(2)} words")

    char_limit_match = re.search(r"(in|under|within)\s+(\d+)\s+characters?", lowered)
    if char_limit_match:
        out.append(f"{char_limit_match.group(2)} characters")

    # Other common constraints
    if "no code" in lowered:
        out.append("No code examples")
    if "include" in lowered and "troubleshooting" in lowered:
        out.append("Include troubleshooting steps")
    if "minimize downtime" in lowered:
        out.append("Minimize downtime")

    # Extract budget/timeline if mentioned
    budget_match = re.search(r"budget[:\s]+\$?([\d,]+k?)", lowered)
    if budget_match:
        out.append(f"Budget: ${budget_match.group(1)}")

    timeline_match = re.search(r"timeline[:\s]+(\d+)\s+(months?|weeks?|days?)", lowered)
    if timeline_match:
        out.append(f"Timeline: {timeline_match.group(1)} {timeline_match.group(2)}")

    return out


def _dedupe(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for x in items:
        key = x.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(x.strip())
    return out


def _infer_ambiguities(text: str, ast: PromptAST) -> list[str]:
    """
    Detect ambiguities and missing critical information in the prompt.
    """
    ambiguities = []
    lowered = text.lower()

    # Vague task detection
    vague_patterns = [
        r"\bhelp me\b",
        r"\bfix this\b",
        r"\bdo something\b",
        r"\bwork on this\b",
    ]

    if ast.task:
        task_lower = ast.task.lower()
        for pattern in vague_patterns:
            if re.search(pattern, task_lower):
                ambiguities.append(
                    "Task is too vague - missing details about what bug, what code, what symptoms"
                )
                break

    # Missing context for technical terms
    technical_indicators = [
        "api",
        "database",
        "system",
        "architecture",
        "code",
        "algorithm",
    ]
    has_technical_terms = any(term in lowered for term in technical_indicators)

    if has_technical_terms and not ast.context:
        # Check if it's a simple question (those don't need context)
        if not (
            ast.task and ast.task.strip().endswith("?") and len(ast.task.split()) < 10
        ):
            ambiguities.append(
                "Missing context about the technical system being discussed"
            )

    # Missing scope/boundaries when task exists but no constraints
    if ast.task and len(ast.constraints) == 0 and len(text.split()) > 15:
        # Only flag if it's a complex request
        if any(
            word in lowered
            for word in ["design", "create", "develop", "build", "implement", "analyze"]
        ):
            pass  # These often imply structured output, check for that instead

    # Missing output format when structured output is implied
    structured_indicators = ["list", "summarize", "compare", "analyze", "report"]
    if (
        any(ind in lowered for ind in structured_indicators)
        and not ast.output_spec.format
    ):
        # Check if structure is mentioned in output_spec
        if not ast.output_spec.structure:
            pass  # Don't flag this as it's often clear from context

    # Unclear references (pronouns without antecedents)
    unclear_refs = [r"\bthis\b", r"\bthat\b", r"\bit\b"]
    # Only flag if these appear early in the text without prior context
    first_sentence = text.split(".")[0].lower() if "." in text else lowered
    for ref_pattern in unclear_refs:
        if re.search(ref_pattern, first_sentence) and not ast.context:
            # Check if it's part of a common phrase like "this is"
            if not re.search(r"\bthis is\b|\bthat is\b|\bit is\b", first_sentence):
                pass  # Don't flag common constructions

    # Missing details for specific domains
    if "onboarding" in lowered and not ast.context:
        ambiguities.append("Missing details about current onboarding process")

    if "retention" in lowered and "strategy" in lowered:
        if not any(word in lowered for word in ["metric", "rate", "churn", "reason"]):
            ambiguities.append("Missing specific retention metrics and churn reasons")

    if "migration" in lowered or "monolith" in lowered:
        if not any(
            word in lowered for word in ["size", "users", "traffic", "complexity"]
        ):
            ambiguities.append("Missing details about monolith size and complexity")

    # Missing target audience for content creation
    content_types = ["blog", "article", "post", "content", "write"]
    if any(ct in lowered for ct in content_types):
        if not any(
            aud in lowered
            for aud in ["beginner", "expert", "audience", "reader", "for"]
        ):
            if "explain" not in lowered:  # "explain" often implies audience
                ambiguities.append("Missing target audience specification")

    # Missing context about data
    if "data" in lowered and any(
        word in lowered for word in ["analyze", "clean", "visualize"]
    ):
        if not ast.context:
            if not any(
                detail in lowered
                for detail in ["csv", "records", "dataset", "customers"]
            ):
                ambiguities.append("Missing context about data structure and volume")

    # Missing class/lesson details for education
    if "lesson" in lowered or "teach" in lowered:
        if not any(
            detail in lowered
            for detail in ["duration", "minutes", "hour", "grade", "age"]
        ):
            ambiguities.append(
                "Missing class duration and student prior knowledge level"
            )

    # Missing CLI/tool details for documentation
    if "cli" in lowered and "tool" in lowered:
        if not ast.context:
            ambiguities.append(
                "Missing context about which CLI tool and target platforms"
            )

    return ambiguities
