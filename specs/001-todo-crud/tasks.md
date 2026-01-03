# Tasks: Todo MVC

**Input**: Design documents from `specs/001-todo-crud/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/

**Tests**: Test tasks are included as per the TDD approach.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in `src/` and `tests/` directories.
- [x] T002 Initialize `pytest` configuration in `pyproject.toml`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T003 [P] Create `Todo` model in `src/models/todo.py`.
- [x] T004 [P] Create unit tests for `Todo` model in `tests/unit/test_todo_model.py`.
- [x] T005 Implement `TodoService` in `src/services/todo_service.py` for in-memory storage.
- [x] T006 Create unit tests for `TodoService` in `tests/unit/test_todo_service.py`.

---

## Phase 3: User Story 1 - Add a new todo (Priority: P1) 🎯 MVP

**Goal**: As a user, I want to add a new todo item to my list so that I can keep track of my tasks.

**Independent Test**: The user can add a new todo and see it in the list.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T007 [US1] Add integration test for the `add` command in `tests/integration/test_cli.py`.

### Implementation for User Story 1

- [x] T008 [US1] Implement the `add` command in `src/cli/main.py`.

---

## Phase 4: User Story 2 - View the list of todos (Priority: P1)

**Goal**: As a user, I want to see all my todo items so that I know what I need to do.

**Independent Test**: The user can see all their todos.

### Tests for User Story 2 ⚠️

- [x] T009 [US2] Add integration test for the `list` command in `tests/integration/test_cli.py`.

### Implementation for User Story 2

- [x] T010 [US2] Implement the `list` command in `src/cli/main.py`.

---

## Phase 5: User Story 3 - Mark a todo as complete/incomplete (Priority: P2)

**Goal**: As a user, I want to mark a todo item as complete or incomplete so that I can track my progress.

**Independent Test**: The user can toggle the completion status of a todo.

### Tests for User Story 3 ⚠️

- [x] T011 [US3] Add integration tests for the `complete` and `uncomplete` commands in `tests/integration/test_cli.py`.

### Implementation for User Story 3

- [x] T012 [US3] Implement the `complete` command in `src/cli/main.py`.
- [x] T013 [US3] Implement the `uncomplete` command in `src/cli/main.py`.

---

## Phase 6: User Story 4 - Update a todo (Priority: P2)

**Goal**: As a user, I want to be able to edit the title and description of a todo item, so that I can correct typos or add more details.

**Independent Test**: The user can edit a todo and see the updated information.

### Tests for User Story 4 ⚠️

- [x] T014 [US4] Add integration test for the `update` command in `tests/integration/test_cli.py`.

### Implementation for User Story 4

- [x] T015 [US4] Implement the `update` command in `src/cli/main.py`.

---

## Phase 7: User Story 5 - Delete a todo (Priority: P3)

**Goal**: As a user, I want to delete a todo item so that I can remove completed or unnecessary tasks from my list.

**Independent Test**: The user can delete a todo, and it will be removed from the list.

### Tests for User Story 5 ⚠️

- [x] T016 [US5] Add integration test for the `delete` command in `tests/integration/test_cli.py`.

### Implementation for User Story 5

- [x] T017 [US5] Implement the `delete` command in `src/cli/main.py`.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T018 [P] Add docstrings to all functions and classes.
- [x] T019 [P] Add type hints to all function signatures.
- [x] T020 Run `quickstart.md` validation.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion

### User Story Dependencies

- User stories can be implemented in any order after the Foundational phase is complete.

### Within Each User Story

- Tests MUST be written and FAIL before implementation.

### Parallel Opportunities

- Tasks marked with [P] can be run in parallel.
- All user story phases can be worked on in parallel by different team members after the Foundational phase is complete.

---

## Implementation Strategy

### MVP First (User Story 1 & 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. Complete Phase 4: User Story 2
5. **STOP and VALIDATE**: Test User Story 1 and 2 independently.
6. Deploy/demo if ready.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 & 2 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 3 & 4 → Test independently → Deploy/Demo
4. Add User Story 5 → Test independently → Deploy/Demo
