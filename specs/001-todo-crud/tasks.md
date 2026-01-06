# Tasks: Todo MVC

**Feature**: `001-todo-crud`
**Spec**: [spec.md](spec.md)
**Plan**: [plan.md](plan.md)

## Phase 1: Setup

- [ ] T001 Create the basic project structure: `src/models`, `src/services`, `src/cli`, `tests/unit`, `tests/integration`.
- [ ] T002 Implement the `Todo` model in `src/models/todo.py`.
- [ ] T003 Implement the `TodoService` in `src/services/todo_service.py`.

## Phase 2: Core Features

- [ ] T004 [US1] Implement the "add" command in `src/cli/main.py`.
- [ ] T005 [US2] Implement the "list" command in `src/cli/main.py`.
- [ ] T006 [US3] Implement the "update" command in `src/cli/main.py`.
- [ ] T007 [US4] Implement the "delete" command in `src/cli/main.py`.
- [ ] T008 [US5] Implement the "complete" and "uncomplete" commands in `src/cli/main.py`.

## Phase 3: Testing

- [ ] T009 Create unit tests for the `Todo` model in `tests/unit/test_todo_model.py`.
- [ ] T010 Create unit tests for the `TodoService` in `tests/unit/test_todo_service.py`.
- [ ] T011 Create integration tests for the CLI in `tests/integration/test_cli.py`.
