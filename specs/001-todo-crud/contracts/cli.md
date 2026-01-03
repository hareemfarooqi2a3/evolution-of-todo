# CLI Contracts: Todo MVC

## `todo` command

### `add` subcommand

-   **Description**: Adds a new todo.
-   **Usage**: `python -m src.cli.main add --title <title> [--description <description>]`
-   **Arguments**:
    -   `--title`: The title of the todo (required).
    -   `--description`: The description of the todo (optional).

### `list` subcommand

-   **Description**: Lists all todos.
-   **Usage**: `python -m src.cli.main list`

### `update` subcommand

-   **Description**: Updates an existing todo.
-   **Usage**: `python -m src.cli.main update --id <id> [--title <title>] [--description <description>]`
-   **Arguments**:
    -   `--id`: The ID of the todo to update (required).
    -   `--title`: The new title of the todo (optional).
    -   `--description`: The new description of the todo (optional).

### `complete` subcommand

-   **Description**: Marks a todo as complete.
-   **Usage**: `python -m src.cli.main complete --id <id>`
-   **Arguments**:
    -   `--id`: The ID of the todo to mark as complete (required).

### `uncomplete` subcommand

-   **Description**: Marks a todo as incomplete.
-   **Usage**: `python -m src.cli.main uncomplete --id <id>`
-   **Arguments**:
    -   `--id`: The ID of the todo to mark as incomplete (required).

### `delete` subcommand

-   **Description**: Deletes a todo.
-   **Usage**: `python -m src.cli.main delete --id <id>`
-   **Arguments**:
    -   `--id`: The ID of the todo to delete (required).
