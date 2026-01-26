from src.cli.main import main
from src.services.todo_service import TodoService
import io
from contextlib import redirect_stdout

def test_add_and_list_commands():
    """
    Tests the 'add' and 'list' commands of the CLI.
    """
    service = TodoService()
    f = io.StringIO()
    with redirect_stdout(f):
        main(["add", "--title", "Test Todo", "--description", "Test description"], todo_service=service)
        main(["add", "--title", "Another Todo"], todo_service=service)
        main(["list"], todo_service=service)
    
    output = f.getvalue()
    assert "Created todo with ID: 1 and Title: 'Test Todo'" in output
    assert "Created todo with ID: 2 and Title: 'Another Todo'" in output
    assert "[ ] 1: Test Todo" in output
    assert "[ ] 2: Another Todo" in output

def test_list_command_empty():
    """
    Tests the 'list' command when there are no todos.
    """
    service = TodoService()
    f = io.StringIO()
    with redirect_stdout(f):
        main(["list"], todo_service=service)
    
    output = f.getvalue()
    assert "No todos yet." in output

def test_add_command_empty_title():
    """
    Tests that the 'add' command fails with an empty title.
    """
    service = TodoService()
    f = io.StringIO()
    with redirect_stdout(f):
        main(["add", "--title", " "], todo_service=service)
    output = f.getvalue()
    assert "Error: Title must not be empty" in output

def test_complete_and_uncomplete_commands():
    """
    Tests the 'complete' and 'uncomplete' commands of the CLI.
    """
    service = TodoService()
    f = io.StringIO()
    with redirect_stdout(f):
        main(["add", "--title", "Test Todo"], todo_service=service)
        main(["complete", "--id", "1"], todo_service=service)
        main(["list"], todo_service=service)
    
    output = f.getvalue()
    assert "Todo 1 marked as complete." in output
    assert "[✔] 1: Test Todo" in output

    f = io.StringIO()
    with redirect_stdout(f):
        main(["uncomplete", "--id", "1"], todo_service=service)
        main(["list"], todo_service=service)

    output = f.getvalue()
    assert "Todo 1 marked as incomplete." in output
    assert "[ ] 1: Test Todo" in output

    f = io.StringIO()
    with redirect_stdout(f):
        main(["complete", "--id", "999"], todo_service=service)
    
    output = f.getvalue()
    assert "Todo with ID 999 not found." in output

def test_update_command():
    """
    Tests the 'update' command of the CLI.
    """
    service = TodoService()
    f = io.StringIO()
    with redirect_stdout(f):
        main(["add", "--title", "Test Todo"], todo_service=service)
        main(["update", "--id", "1", "--title", "Updated Title", "--description", "Updated description"], todo_service=service)
        main(["list"], todo_service=service)
    
    output = f.getvalue()
    assert "Todo 1 updated." in output
    assert "[ ] 1: Updated Title" in output

    f = io.StringIO()
    with redirect_stdout(f):
        main(["update", "--id", "999", "--title", "Not found"], todo_service=service)
    
    output = f.getvalue()
    assert "Todo with ID 999 not found." in output

def test_delete_command():

    """

    Tests the 'delete' command of the CLI.

    """

    service = TodoService()

    f = io.StringIO()

    with redirect_stdout(f):

        main(["add", "--title", "Test Todo"], todo_service=service)

        main(["delete", "--id", "1"], todo_service=service)

        main(["list"], todo_service=service)

    

    output = f.getvalue()

    assert "Todo 1 deleted." in output

    assert "No todos yet." in output



    f = io.StringIO()

    with redirect_stdout(f):

        main(["delete", "--id", "999"], todo_service=service)

    

    output = f.getvalue()

    assert "Todo with ID 999 not found." in output



def test_add_command_long_title():

    """

    Tests the 'add' command with a very long title.

    """

    service = TodoService()

    f = io.StringIO()

    long_title = "a" * 1000

    with redirect_stdout(f):

        main(["add", "--title", long_title], todo_service=service)

        main(["list"], todo_service=service)

    

    output = f.getvalue()

    assert f"Created todo with ID: 1 and Title: '{long_title}'" in output

    assert f"[ ] 1: {long_title}" in output
