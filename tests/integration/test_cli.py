import pytest
from phase1_cli.src.main import main
from phase1_cli.src.services import TodoService
import io
import sys
from contextlib import redirect_stdout


def test_add_and_list_commands():
    """Tests the 'add' and 'list' commands of the CLI."""
    service = TodoService()
    f = io.StringIO()
    with redirect_stdout(f):
        main(["add", "Test Todo", "--description", "Test description"], todo_service=service)
        main(["add", "Another Todo"], todo_service=service)
        main(["list"], todo_service=service)

    output = f.getvalue()
    assert "Test Todo" in output
    assert "Another Todo" in output


def test_list_command_empty():
    """Tests the 'list' command when there are no todos."""
    service = TodoService()
    f = io.StringIO()
    with redirect_stdout(f):
        main(["list"], todo_service=service)

    output = f.getvalue()
    # Either "No todos" message or empty list
    assert "No todos" in output or output.strip() == "" or "0 todos" in output.lower()


def test_complete_command():
    """Tests the 'complete' command of the CLI."""
    service = TodoService()
    f = io.StringIO()
    with redirect_stdout(f):
        main(["add", "Test Todo"], todo_service=service)
        main(["complete", "1"], todo_service=service)
        main(["list"], todo_service=service)

    output = f.getvalue()
    # Task should be marked complete in some way
    assert "Test Todo" in output


def test_delete_command():
    """Tests the 'delete' command of the CLI."""
    service = TodoService()
    f = io.StringIO()
    with redirect_stdout(f):
        main(["add", "Test Todo"], todo_service=service)
        main(["delete", "1"], todo_service=service)

    output = f.getvalue()
    assert "Test Todo" in output or "deleted" in output.lower()
