---
description: "Task list for testing the Todo MVC console application"
---

# Tasks: Testing the Todo Console UI

**Input**: This document provides instructions on how to test the CRUD (Create, Read, Update, Delete) functionality of the console application.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Manual Testing from the Console

**Purpose**: To manually verify that each command works as expected from the command line. Run these commands from the root of the project directory.

- [ ] T001 [US1] **Test Add**: Run the `add` command to create a new todo.
  - **Command**: `python -m src.cli.main add --title "My First Todo" --description "A test description"`
  - **Expected Output**: `Created todo with ID: 1 and Title: 'My First Todo'`

- [ ] T002 [US2] **Test List**: Run the `list` command to see the newly created todo.
  - **Command**: `python -m src.cli.main list`
  - **Expected Output**: `[ ] 1: My First Todo`

- [ ] T003 [US3] **Test Complete**: Run the `complete` command to mark the todo as complete.
  - **Command**: `python -m src.cli.main complete --id 1`
  - **Expected Output**: `Todo 1 marked as complete.`

- [ ] T004 [US3] **Verify Complete**: Run the `list` command again to see the status change.
  - **Command**: `python -m src.cli.main list`
  - **Expected Output**: `[✔] 1: My First Todo`

- [ ] T005 [US4] **Test Update**: Run the `update` command to change the todo's title.
  - **Command**: `python -m src.cli.main update --id 1 --title "My Updated Todo"`
  - **Expected Output**: `Todo 1 updated.`

- [ ] T006 [US4] **Verify Update**: Run the `list` command again to see the updated title.
  - **Command**: `python -m src.cli.main list`
  - **Expected Output**: `[✔] 1: My Updated Todo`

- [ ] T007 [US5] **Test Delete**: Run the `delete` command to remove the todo.
  - **Command**: `python -m src.cli.main delete --id 1`
  - **Expected Output**: `Todo 1 deleted.`

- [ ] T008 [US5] **Verify Delete**: Run the `list` command a final time to ensure the list is empty.
  - **Command**: `python -m src.cli.main list`
  - **Expected Output**: `No todos yet.`

---

## Phase 2: Automated Testing

**Purpose**: To run the full suite of automated tests to ensure all functionality works correctly and there are no regressions.

- [ ] T009 **Run All Tests**: Execute the `pytest` command from the root of the project. This will discover and run all tests in the `tests/` directory.
  - **Command**: `pytest`
  - **Expected Output**: A summary showing that all tests passed (e.g., `_..._ passed in _..._s`).

---

## Phase 3: Writing a New Automated Test

**Purpose**: To extend the test suite with a new test case. This is a good practice to cover edge cases or new functionality.

- [ ] T010 **Create a New Test Case**: Open the `tests/integration/test_cli.py` file and add a new test function to verify a specific behavior. For example, test adding a todo with a very long title.
  - **File to Edit**: `tests/integration/test_cli.py`
  - **Example Test**:
    ```python
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
    ```

- [ ] T011 **Run the New Test**: Run `pytest` again and confirm that your new test is discovered and passes along with the existing tests.
  - **Command**: `pytest`
  - **Expected Output**: A summary showing that one more test passed.
