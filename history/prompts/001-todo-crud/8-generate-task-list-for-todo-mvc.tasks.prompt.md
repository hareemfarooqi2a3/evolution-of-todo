---
id: 8
title: Generate Task List for Todo MVC
stage: tasks
date: 2026-01-03
surface: agent
model: gemini-cli
feature: 001-todo-crud
branch: 001-todo-crud
user: 
command: 
labels: [tasks, generation]
links:
  spec: specs/001-todo-crud/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-todo-crud/tasks.md
tests:

---

## Prompt

Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts.

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Task Generation Rules

**CRITICAL**: Tasks MUST be organized by user story to enable independent implementation and testing.

**Tests are OPTIONAL**: Only generate test tasks if explicitly requested in the feature specification or if user requests TDD approach.

### Checklist Format (REQUIRED)

Every task MUST strictly follow this format:

` - [ ] [TaskID] [P?] [Story?] Description with file path `

**Format Components**:

1. **Checkbox**: ALWAYS start with `- [ ]` (markdown checkbox)
2. **Task ID**: Sequential number (T001, T002, T003...) in execution order
3. **[P] marker**: Include ONLY if task is parallelizable (different files, no dependencies on incomplete tasks)
4. **[Story] label**: REQUIRED for user story phase tasks only
   - Format: [US1], [US2], [US3], etc. (maps to user stories from spec.md)
   - Setup phase: NO story label
   - Foundational phase: NO story label  
   - User Story phases: MUST have story label
   - Polish phase: NO story label
5. **Description**: Clear action with exact file path

**Examples**:

- ✅ CORRECT: `- [ ] T001 Create project structure per implementation plan`
- ✅ CORRECT: `- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py`
- ✅ CORRECT: `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
- ✅ CORRECT: `- [ ] T014 [US1] Implement UserService in src/services/user_service.py`
- ❌ WRONG: `- [ ] Create User model` (missing ID and Story label)
- ❌ WRONG: `T001 [US1] Create model` (missing checkbox)
- ❌ WRONG: `- [ ] [US1] Create User model` (missing Task ID)
- ❌ WRONG: `- [ ] T001 [US1] Create model` (missing file path)

### Task Organization

1. **From User Stories (spec.md)** - PRIMARY ORGANIZATION:
   - Each user story (P1, P2, P3...) gets its own phase
   - Map all related components to their story:
     - Models needed for that story
     - Services needed for that story
     - Endpoints/UI needed for that story
     - If tests requested: Tests specific to that story
   - Mark story dependencies (most stories should be independent)

2. **From Contracts**:
   - Map each contract/endpoint → to the user story it serves
   - If tests requested: Each contract → contract test task [P] before implementation in that story's phase

3. **From Data Model**:
   - Map each entity to the user story(ies) that need it
   - If entity serves multiple stories: Put in earliest story or Setup phase
   - Relationships → service layer tasks in appropriate story phase

4. **From Setup/Infrastructure**:
   - Shared infrastructure → Setup phase (Phase 1)
   - Foundational/blocking tasks → Foundational phase (Phase 2)
   - Story-specific setup → within that story's phase

### Phase Structure

- **Phase 1**: Setup (project initialization)
- **Phase 2**: Foundational (blocking prerequisites - MUST complete before user stories)
- **Phase 3+**: User Stories in priority order (P1, P2, P3...)
  - Within each story: Tests (if requested) → Models → Services → Endpoints → Integration
  - Each phase should be a complete, independently testable increment
- **Final Phase**: Polish & Cross-Cutting Concerns

## Response snapshot

I have generated the `tasks.md` file with 31 tasks, organized by user story, and including setup, foundational, and testing tasks. The file is located at `specs/001-todo-crud/tasks.md`.

## Outcome

- ✅ Impact: The `tasks.md` file was created, providing a clear and actionable plan for implementing the feature.
- 🧪 Tests: Test tasks were included for each user story.
- 📁 Files: `specs/001-todo-crud/tasks.md` was created.
- 🔁 Next prompts: The next step would be to start implementing the tasks in `tasks.md`.
- 🧠 Reflection: The process of generating tasks from design documents is a good way to ensure all requirements are met.

## Evaluation notes (flywheel)

- Failure modes observed: The initial attempt to run the `check-prerequisites.ps1` script failed because the feature name was not specified. The attempt to run the bash script on Windows also failed.
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): A better way to determine the feature name could be implemented in the scripts.
