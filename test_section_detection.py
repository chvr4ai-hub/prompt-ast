import re


def _split_labeled_sections_new(text: str) -> dict[str, str]:
    """Test new section detection logic."""
    aliases = {
        "background": "context",
        "goal": "task",
        "requirements": "constraints",
        "requirement": "constraints",
    }

    # Pattern that matches section headers with optional inline content
    pattern = r"(?im)^(?:#+\s*|\d+\.\s*)?(context|task|constraints|output|result|background|goal|requirements?)\s*:\s*(.*?)$"

    # Split text using the pattern
    parts = re.split(pattern, text)

    if len(parts) <= 1:
        return {}

    sections: dict[str, str] = {}
    i = 1
    while i < len(parts):
        if i + 1 < len(parts):
            section_name = parts[i].strip().lower()
            section_name = aliases.get(section_name, section_name)

            # Inline content (on same line as header)
            inline_content = parts[i + 1].strip() if i + 1 < len(parts) else ""

            # Multi-line content (between this header and next)
            multiline_content = parts[i + 2].strip() if i + 2 < len(parts) else ""

            # Combine inline and multiline content
            content_parts = []
            if inline_content:
                content_parts.append(inline_content)
            if multiline_content:
                content_parts.append(multiline_content)

            if content_parts:
                sections[section_name] = "\n".join(content_parts).strip()

            i += 3
        else:
            break

    return sections


# Test the new function
if __name__ == "__main__":
    test_text = """Context: We have a Python API endpoint that handles user authentication.
Task: Review the security implications of storing passwords in plain text.
Constraints:
- Focus on security best practices
- Suggest concrete improvements
Output: Provide a bullet-point list"""

    result = _split_labeled_sections_new(test_text)
    print("Result:", result)
