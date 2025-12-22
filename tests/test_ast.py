from prompt_ast.ast import PromptAST


def test_ast_json_serialization():
    ast = PromptAST(raw="Hello", task="Say hello")
    j = ast.to_json()
    assert '"task": "Say hello"' in j
