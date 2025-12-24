from typer.testing import CliRunner

from prompt_ast.cli import app

runner = CliRunner()


def test_normalize_with_file(tmp_path):
    """Test that --file option reads prompt from file."""

    prompt_file = tmp_path / "test_prompt.txt"
    prompt_file.write_text("This is a test prompt")

    result = runner.invoke(app, ["normalize", "--file", str(prompt_file)])

    assert result.exit_code == 0
    assert "Prompt AST" in result.stdout


def test_normalize_file_not_exists():
    """Test error message when file does not exists."""

    result = runner.invoke(app, ["normalize", "--file", "nonexistent.txt"])

    assert result.exit_code == 1
    assert "does not exist" in result.stdout


def test_normalize_with_text_arguments():
    """Test existing behavior: text as positional argument."""

    result = runner.invoke(app, ["normalize", "test prompt text"])

    assert result.exit_code == 0
    assert "Prompt AST" in result.stdout


def test_normalize_both_text_and_file(tmp_path):
    """Test that using both text and --file raises error."""

    prompt_file = tmp_path / "test.txt"
    prompt_file.write_text("file content")

    result = runner.invoke(app, ["normalize", "text arg", "--file", str(prompt_file)])

    assert result.exit_code == 1
    assert "Cannot specify both" in result.stdout


def test_normalize_neither_text_nor_file():
    """Test that providing neither text nor file raises error."""

    result = runner.invoke(app, ["normalize"])

    assert result.exit_code == 1
    assert "Must provide either" in result.stdout


def test_normalize_file_with_multiline_content(tmp_path):
    """Test that multiline prompts from file work correctly."""

    prompt_file = tmp_path / "multiline.txt"
    prompt_file.write_text("Line1\nLine2\nLine3")

    result = runner.invoke(app, ["normalize", "--file", str(prompt_file)])

    assert result.exit_code == 0


def test_normalize_file_short_flag(tmp_path):
    """Test that -f short flag works."""

    prompt_file = tmp_path / "text.txt"
    prompt_file.write_text("test content")

    result = runner.invoke(app, ["normalize", "-f", str(prompt_file)])

    assert result.exit_code == 0


def test_normalize_empty_string_with_file(tmp_path):
    """Test mutual exclusion catches empty string text with file."""

    prompt_file = tmp_path / "test.txt"
    prompt_file.write_text("file content")

    result = runner.invoke(app, ["normalize", "", "--file", str(prompt_file)])

    assert result.exit_code == 1
    assert "Cannot specify both" in result.stdout


def test_normalize_file_is_directory(tmp_path):
    """Test error when --file points to a directory."""

    directory = tmp_path / "test_dir"
    directory.mkdir()

    result = runner.invoke(app, ["normalize", "--file", str(directory)])

    assert result.exit_code == 1
    assert "is not a file" in result.stdout


def test_normalize_file_with_tilde(tmp_path, monkeypatch):
    """Test that ~ expansion works in file paths."""

    monkeypatch.setenv("HOME", str(tmp_path))

    prompt_file = tmp_path / "prompt.txt"
    prompt_file.write_text("test content")

    result = runner.invoke(app, ["normalize", "--file", "~/prompt.txt"])

    assert result.exit_code == 0


def test_normalize_file_too_large(tmp_path):
    """Test error when file exceeds 5MB size limit."""

    large_file = tmp_path / "large.txt"
    large_file.write_text("x" * (6 * 1024 * 1024))

    result = runner.invoke(app, ["normalize", "--file", str(large_file)])

    assert result.exit_code == 1
    assert "too large" in result.stdout
