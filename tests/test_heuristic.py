from prompt_ast.parse.heuristic import parse_prompt_heuristic


def test_heuristic_extracts_role_and_constraints():
    text = "Act as a senior backend architect. Be concise. Use bullet points. Provide step by step."
    ast = parse_prompt_heuristic(text)
    assert ast.role is not None
    assert any("concise" in c.lower() for c in ast.constraints)
    assert any("bullet" in c.lower() for c in ast.constraints)
    assert ast.metadata.get("extracted_by") == "heuristic"
