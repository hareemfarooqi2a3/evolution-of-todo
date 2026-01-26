import argparse
from .services import TodoService

def main():
    """Main function to run the CLI todo application."""
    parser = argparse.ArgumentParser(description="A simple command-line todo application.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 'add' command
    add_parser = subparsers.add_parser("add", help="Add a new todo")
    add_parser.add_argument("--title", type=str, required=True, help="The title of the todo.")
    add_parser.add_argument("--description", type=str, help="The description of the todo.")

    # 'list' command
    list_parser = subparsers.add_parser("list", help="List all todos")

    # 'update' command
    update_parser = subparsers.add_parser("update", help="Update a todo")
    update_parser.add_argument("--id", type=int, required=True, help="The ID of the todo to update.")
    update_parser.add_argument("--title", type=str, help="The new title of the todo.")
    update_parser.add_argument("--description", type=str, help="The new description of the todo.")
    update_parser.add_argument("--completed", type=bool, help="The new completion status of the todo.")

    # 'delete' command
    delete_parser = subparsers.add_parser("delete", help="Delete a todo")
    delete_parser.add_argument("--id", type=int, required=True, help="The ID of the todo to delete.")
    
    # 'complete' command
    complete_parser = subparsers.add_parser("complete", help="Mark a todo as complete")
    complete_parser.add_argument("--id", type=int, required=True, help="The ID of the todo to complete.")

    # 'uncomplete' command
    uncomplete_parser = subparsers.add_parser("uncomplete", help="Mark a todo as uncomplete")
    uncomplete_parser.add_argument("--id", type=int, required=True, help="The ID of the todo to uncomplete.")

    args = parser.parse_args()
    service = TodoService()

    if args.command == "add":
        todo = service.create_todo(args.title, args.description)
        print(f"Added todo: {todo}")
    elif args.command == "list":
        todos = service.get_all_todos()
        for todo in todos:
            print(todo)
    elif args.command == "update":
        todo = service.update_todo(args.id, args.title, args.description, args.completed)
        if todo:
            print(f"Updated todo: {todo}")
        else:
            print(f"Todo with ID {args.id} not found.")
    elif args.command == "delete":
        if service.delete_todo(args.id):
            print(f"Deleted todo with ID {args.id}.")
        else:
            print(f"Todo with ID {args.id} not found.")
    elif args.command == "complete":
        todo = service.update_todo(args.id, completed=True)
        if todo:
            print(f"Completed todo: {todo}")
        else:
            print(f"Todo with ID {args.id} not found.")
    elif args.command == "uncomplete":
        todo = service.update_todo(args.id, completed=False)
        if todo:
            print(f"Un-completed todo: {todo}")
        else:
            print(f"Todo with ID {args.id} not found.")


if __name__ == "__main__":
    main()
