---
description: "Task list for Todo MVC feature implementation"
---

# Tasks: Todo MVC

**Input**: Design documents from `/specs/001-todo-crud/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure (`src`, `tests`) per implementation plan
- [ ] T002 Create empty Python files for model, service, and CLI (`src/models/todo.py`, `src/services/todo_service.py`, `src/cli/main.py`)
- [ ] T003 Create empty test files (`tests/unit/test_todo_model.py`, `tests/unit/test_todo_service.py`, `tests/integration/test_cli.py`)
- [ ] T004 Initialize `pyproject.toml` with `pytest` dependency.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data model that MUST be complete before ANY user story can be implemented

- [ ] T005 [US1] Implement the `Todo` data model in `src/models/todo.py` with fields: `id`, `title`, `description`, `completed`.
- [ ] T006 [US1] Write a unit test for the `Todo` model in `tests/unit/test_todo_model.py` to verify its attributes.

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 & 2 - Add and View Todos (Priority: P1) 🎯 MVP

**Goal**: As a user, I want to add a new todo and see it in my list.

**Independent Test**: A user can run `python -m cli.main add --title "My Task"` and then `python -m cli.main list` to see the new task.

### Implementation for User Story 1 & 2

- [ ] T007 [US1] Implement the `TodoService` class in `src/services/todo_service.py`.
- [ ] T008 [US1] In `TodoService`, implement the `add_todo()` method.
- [ ] T009 [US2] In `TodoService`, implement the `list_todos()` method.
- [ ] T010 [US1,US2] Write unit tests for `add_todo()` and `list_todos()` in `tests/unit/test_todo_service.py`.
- [ ] T011 [US1] Implement the `add` command in `src/cli/main.py`.
- [ ] T012 [US2] Implement the `list` command in `src/cli/main.py`.
- [ ] T013 [US1,US2] Write an integration test in `tests/integration/test_cli.py` to verify the `add` and `list` commands work together.

**Checkpoint**: At this point, User Stories 1 & 2 should be fully functional and testable.

---

## Phase 4: User Story 3 - Mark a todo as complete/incomplete (Priority: P2)

**Goal**: As a user, I want to mark a todo item as complete or incomplete to track my progress.

**Independent Test**: A user can run `python -m cli.main complete --id 1` and see the status change in the `list` command output.

### Implementation for User Story 3

- [ ] T014 [US3] In `TodoService`, implement `get_todo_by_id()`, `complete_todo()`, and `uncomplete_todo()` methods in `src/services/todo_service.py`.
- [ ] T015 [US3] Write unit tests for `complete_todo()` and `uncomplete_todo()` in `tests/unit/test_todo_service.py`.
- [ ] T016 [US3] Implement the `complete` and `uncomplete` commands in `src/cli/main.py`.
- [ ] T017 [US3] Write an integration test in `tests/integration/test_cli.py` for the `complete` and `uncomplete` commands.

**Checkpoint**: User Story 3 should be fully functional and testable.

---

## Phase 5: User Story 4 - Update a todo (Priority: P2)

**Goal**: As a user, I want to edit the title and description of a todo item.

**Independent Test**: A user can run `python -m cli.main update --id 1 --title "New Title"` and see the updated title in the `list` command output.

### Implementation for User Story 4

- [ ] T018 [US4] In `TodoService`, implement the `update_todo()` method in `src/services/todo_service.py`.
- [ ] T019 [US4] Write a unit test for `update_todo()` in `tests/unit/test_todo_service.py`.
- [ ] T020 [US4] Implement the `update` command in `src/cli/main.py`.
- [ ] T021 [US4] Write an integration test in `tests/integration/test_cli.py` for the `update` command.

**Checkpoint**: User Story 4 should be fully functional and testable.

---

## Phase 6: User Story 5 - Delete a todo (Priority: P3)

**Goal**: As a user, I want to delete a todo item.

**Independent Test**: A user can run `python -m cli.main delete --id 1`, and the todo will no longer appear in the `list` command output.

### Implementation for User Story 5

- [ ] T022 [US5] In `TodoService`, implement the `delete_todo()` method in `src/services/todo_service.py`.
- [ ] T023 [US5] Write a unit test for `delete_todo()` in `tests/unit/test_todo_service.py`.
- [ ] T024 [US5] Implement the `delete` command in `src/cli/main.py`.
- [ ] T025 [US5] Write an integration test in `tests/integration/test_cli.py` for the `delete` command.

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories.

- [ ] T026 Add error handling for invalid todo IDs in `src/cli/main.py`.
- [ ] T027 Add validation for empty titles in the `add` command in `src/cli/main.py`.
- [ ] T028 Review and refine all console output for clarity.

---

## Dependencies & Execution Order

- **Setup (Phase 1)** must be completed before all other phases.
- **Foundational (Phase 2)** depends on Setup completion.
- **User Stories (Phases 3-6)** depend on the Foundational phase. They can be implemented sequentially or in parallel.
- **Polish (Phase 7)** should be done after all user stories are complete.