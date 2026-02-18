"""
Golden snapshot tests for heuristic parser using fixtures.
"""

from __future__ import annotations

from collections import Counter

import pytest
from prompt_ast.parse.heuristic import parse_prompt_heuristic
from .fixtures import FIXTURES


def _normalize_ast_for_comparison(ast_dict: dict) -> dict:
    """Normalize AST dict for comparison by removing raw field."""
    normalized = ast_dict.copy()
    # Remove 'raw' field as it's just the input prompt
    normalized.pop("raw", None)
    return normalized


@pytest.mark.parametrize("fixture", FIXTURES, ids=lambda f: f["description"])
def test_heuristic_golden_snapshots(fixture):
    """
    Test heuristic parser against golden snapshots.

    Each fixture contains:
    - description: What this test validates
    - prompt: Input prompt text
    - expected_ast: Golden expected output
    """
    prompt = fixture["prompt"]
    expected = fixture["expected_ast"]

    # Parse the prompt
    actual_ast = parse_prompt_heuristic(prompt)
    actual_dict = actual_ast.to_dict()

    # Normalize for comparison (remove 'raw' field)
    actual_normalized = _normalize_ast_for_comparison(actual_dict)
    expected_normalized = _normalize_ast_for_comparison(expected)

    # Compare each field individually for better error messages
    assert actual_normalized.get("version") == expected_normalized.get(
        "version"
    ), f"Version mismatch for: {fixture['description']}"

    assert actual_normalized.get("role") == expected_normalized.get(
        "role"
    ), f"Role mismatch for: {fixture['description']}"

    assert actual_normalized.get("context") == expected_normalized.get(
        "context"
    ), f"Context mismatch for: {fixture['description']}"

    assert actual_normalized.get("task") == expected_normalized.get(
        "task"
    ), f"Task mismatch for: {fixture['description']}"

    assert actual_normalized.get("constraints") == expected_normalized.get(
        "constraints"
    ), f"Constraints mismatch for: {fixture['description']}\nExpected: {expected_normalized.get('constraints')}\nActual: {actual_normalized.get('constraints')}"

    assert actual_normalized.get("assumptions") == expected_normalized.get(
        "assumptions"
    ), f"Assumptions mismatch for: {fixture['description']}"

    assert actual_normalized.get("ambiguities") == expected_normalized.get(
        "ambiguities"
    ), f"Ambiguities mismatch for: {fixture['description']}\nExpected: {expected_normalized.get('ambiguities')}\nActual: {actual_normalized.get('ambiguities')}"

    assert actual_normalized.get("output_spec") == expected_normalized.get(
        "output_spec"
    ), f"Output spec mismatch for: {fixture['description']}\nExpected: {expected_normalized.get('output_spec')}\nActual: {actual_normalized.get('output_spec')}"

    # Metadata is checked separately as confidence might vary
    actual_meta = actual_normalized.get("metadata", {})
    expected_meta = expected_normalized.get("metadata", {})

    assert actual_meta.get("extracted_by") == expected_meta.get(
        "extracted_by"
    ), f"Metadata extracted_by mismatch for: {fixture['description']}"


def test_fixture_count():
    """Ensure we have at least 20 fixtures as specified."""
    assert len(FIXTURES) >= 20, f"Expected at least 20 fixtures, got {len(FIXTURES)}"


def test_fixture_domain_coverage():
    """Ensure fixtures cover all supported domains via explicit fixture metadata."""
    required_domains = {
        "software",
        "data",
        "content",
        "education",
        "business",
        "creative",
        "research",
        "general",
    }
    domain_counts = Counter(fixture["domain"] for fixture in FIXTURES)

    missing_domains = required_domains - set(domain_counts)
    assert not missing_domains, f"Missing fixture domains: {sorted(missing_domains)}"

    unexpected_domains = set(domain_counts) - required_domains
    assert not unexpected_domains, f"Unexpected fixture domains: {sorted(unexpected_domains)}"
