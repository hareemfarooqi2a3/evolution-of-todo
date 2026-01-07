import argparse
from src.services.todo_service import TodoService
from typing import List, Optional

def execute_command(todo_service: TodoService, args: argparse.Namespace):
    """
    Executes the command based on the parsed arguments.
    """
    if args.command == "add":
        if not args.title.strip():
            print("Error: Title must not be empty")
            return
        todo = todo_service.add_todo(title=args.title, description=args.description)
        print(f"Created todo with ID: {todo.id} and Title: '{todo.title}'")
    elif args.command == "list":
        todos = todo_service.list_todos()
        if not todos:
            print("No todos yet.")
        else:
            for todo in todos:
                status = "[✔]" if todo.completed else "[ ]"
                print(f"{status} {todo.id}: {todo.title}")
    elif args.command == "complete":
        todo = todo_service.complete_todo(args.id)
        if todo:
            print(f"Todo {todo.id} marked as complete.")
        else:
            print(f"Todo with ID {args.id} not found.")
    elif args.command == "uncomplete":
        todo = todo_service.uncomplete_todo(args.id)
        if todo:
            print(f"Todo {todo.id} marked as incomplete.")
        else:
            print(f"Todo with ID {args.id} not found.")
    elif args.command == "update":
        todo = todo_service.update_todo(args.id, args.title, args.description)
        if todo:
            print(f"Todo {todo.id} updated.")
        else:
            print(f"Todo with ID {args.id} not found.")
    elif args.command == "delete":
        if todo_service.delete_todo(args.id):
            print(f"Todo {args.id} deleted.")
        else:
            print(f"Todo with ID {args.id} not found.")

def main(argv: Optional[List[str]] = None, todo_service: Optional[TodoService] = None):
    """
    The main entry point for the CLI application.
    """
    parser = argparse.ArgumentParser(description="A simple CLI todo application.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new todo")
    add_parser.add_argument("--title", required=True, help="The title of the todo")
    add_parser.add_argument("--description", help="The description of the todo")

    # List command
    list_parser = subparsers.add_parser("list", help="List all todos")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a todo as complete")
    complete_parser.add_argument("--id", required=True, type=int, help="The ID of the todo to mark as complete")

    # Uncomplete command
    uncomplete_parser = subparsers.add_parser("uncomplete", help="Mark a todo as incomplete")
    uncomplete_parser.add_argument("--id", required=True, type=int, help="The ID of the todo to mark as incomplete")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update an existing todo")
    update_parser.add_argument("--id", required=True, type=int, help="The ID of the todo to update")
    update_parser.add_argument("--title", help="The new title of the todo")
    update_parser.add_argument("--description", help="The new description of the todo")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a todo")
    delete_parser.add_argument("--id", required=True, type=int, help="The ID of the todo to delete")

    args = parser.parse_args(argv)

    if todo_service is None:
        todo_service = TodoService()
    
    execute_command(todo_service, args)

if __name__ == "__main__":
    main()
