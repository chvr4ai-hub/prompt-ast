"""
Golden snapshot tests for heuristic parser using fixtures.
"""

from __future__ import annotations

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
    assert actual_normalized.get("version") == expected_normalized.get("version"), \
        f"Version mismatch for: {fixture['description']}"
    
    assert actual_normalized.get("role") == expected_normalized.get("role"), \
        f"Role mismatch for: {fixture['description']}"
    
    assert actual_normalized.get("context") == expected_normalized.get("context"), \
        f"Context mismatch for: {fixture['description']}"
    
    assert actual_normalized.get("task") == expected_normalized.get("task"), \
        f"Task mismatch for: {fixture['description']}"
    
    assert actual_normalized.get("constraints") == expected_normalized.get("constraints"), \
        f"Constraints mismatch for: {fixture['description']}\nExpected: {expected_normalized.get('constraints')}\nActual: {actual_normalized.get('constraints')}"
    
    assert actual_normalized.get("assumptions") == expected_normalized.get("assumptions"), \
        f"Assumptions mismatch for: {fixture['description']}"
    
    assert actual_normalized.get("ambiguities") == expected_normalized.get("ambiguities"), \
        f"Ambiguities mismatch for: {fixture['description']}\nExpected: {expected_normalized.get('ambiguities')}\nActual: {actual_normalized.get('ambiguities')}"
    
    assert actual_normalized.get("output_spec") == expected_normalized.get("output_spec"), \
        f"Output spec mismatch for: {fixture['description']}\nExpected: {expected_normalized.get('output_spec')}\nActual: {actual_normalized.get('output_spec')}"
    
    # Metadata is checked separately as confidence might vary
    actual_meta = actual_normalized.get("metadata", {})
    expected_meta = expected_normalized.get("metadata", {})
    
    assert actual_meta.get("extracted_by") == expected_meta.get("extracted_by"), \
        f"Metadata extracted_by mismatch for: {fixture['description']}"


def test_fixture_count():
    """Ensure we have exactly 20 fixtures as specified."""
    assert len(FIXTURES) == 20, f"Expected 20 fixtures, got {len(FIXTURES)}"


def test_fixture_domain_coverage():
    """Ensure fixtures cover all specified domains."""
    descriptions = [f["description"].lower() for f in FIXTURES]
    
    # Count fixtures by domain (approximate based on description)
    domains = {
        "software": ["code", "api", "debug", "architect"],
        "data": ["data", "visualization", "statistical", "analysis"],
        "content": ["blog", "social media", "tweet", "documentation"],
        "education": ["lesson", "teacher", "explain", "eli5"],
        "business": ["retention", "strategy", "onboarding", "customer"],
        "creative": ["story", "brainstorm", "creative"],
        "research": ["research", "literature", "hypothesis", "papers"],
        "general": ["capital", "consultant", "migration"]
    }
    
    # Count how many fixtures match each domain
    domain_counts = {}
    for domain_name, keywords in domains.items():
        count = sum(
            1 for desc in descriptions
            if any(keyword in desc for keyword in keywords)
        )
        domain_counts[domain_name] = count
    
    # Verify we have diverse coverage across multiple domains
    domains_with_coverage = sum(1 for count in domain_counts.values() if count > 0)
    assert domains_with_coverage >= 5, \
        f"Expected coverage in at least 5 domains, got {domains_with_coverage}. Coverage: {domain_counts}"
    
    # Verify we have at least 20 fixtures total
    assert len(FIXTURES) >= 20, "Should have at least 20 diverse fixtures"
