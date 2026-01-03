# Quickstart: Todo MVC

## Setup

1.  Clone the repository.
2.  Install Python 3.13+.

## Running the application

### Add a new todo

```bash
python -m src.cli.main add --title "My first todo" --description "This is a test."
```

### List all todos

```bash
python -m src.cli.main list
```

### Update a todo

```bash
python -m src.cli.main update --id 1 --title "My updated todo"
```

### Mark a todo as complete

```bash
python -m src.cli.main complete --id 1
```

### Mark a todo as incomplete

```bash
python -m src.cli.main uncomplete --id 1
```

### Delete a todo

```bash
python -m src.cli.main delete --id 1
```
