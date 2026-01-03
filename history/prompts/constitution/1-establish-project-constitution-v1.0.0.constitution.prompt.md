---
id: 1
title: Establish Project Constitution v1.0.0
stage: constitution
date: 2026-01-02
surface: agent
model: gemini
feature: none
branch: main
user: User
command: /sp.constitution
labels: [constitution, documentation]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - GEMINI.md
  - .gemini/commands/sp.plan.toml
tests:
  - none
---

## Prompt

/sp.constitution # AI Constitution – Evolution of Todo Project

## Core Principle
This project follows strict spec-driven, agentic development.
No code may be written unless explicitly derived from an approved specification.

---

## Decision Hierarchy
1. Specification files (Spec-Kit Plus) – highest authority
2. Constitution.md
3. Claude.md instructions
4. README.md
5. AI-generated plans and tasks
6. Code implementation

---

## Allowed Actions
- Claude Code MAY:
  - Generate Python code strictly from specs
  - Refactor code if specs change
  - Add docstrings and type hints
- Gemini CLI MAY:
  - Analyze repository structure
  - Validate code against specs
  - Generate task breakdowns
- Spec-Kit Plus MAY:
  - Define data models
  - Define behavior, constraints, and acceptance criteria

---

## Forbidden Actions
- No manual coding by humans
- No speculative features
- No hardcoding outside defined specs
- No external dependencies unless explicitly specified

---

## Coding Standards
- Python 3.13+
- Type hints required
- Single responsibility principle
- Clear separation of:
  - Models
  - Services
  - CLI interface
- Deterministic behavior (no randomness)

---

## Error Handling
- Fail fast
- User-facing CLI errors must be readable
- Internal errors must raise exceptions

---

## Review Rules
- Every phase must include:
  - Spec history
  - Plan
  - Tasks
  - Implementation
- If spec conflicts exist, STOP and request clarification

---

## Evolution Constraint
Design decisions must not block future evolution into:
- Persistent storage
- APIs
- Distributed systems
- Event-driven architecture

## Response snapshot

I have updated the project constitution to version 1.0.0 and ensured all dependent templates are in sync.

- **New Version**: 1.0.0 (major bump reflecting the new formalized constitution)
- **Changes**:
    - Replaced the placeholder constitution with a detailed, formal document.
    - Updated `.specify/templates/plan-template.md` to align with the new constitution's principles.
    - Updated `GEMINI.md` with the new decision hierarchy.
    - Updated `.gemini/commands/sp.plan.toml` to reflect the new constitution.
- **Commit Message**: `docs: amend constitution to v1.0.0 (principle additions + governance update)`

## Outcome

- ✅ Impact: The project now has a formal constitution that will guide development.
- 🧪 Tests: No tests were run.
- 📁 Files: 4 files were modified.
- 🔁 Next prompts: The user can now proceed with other commands, like `/sp.specify` to create a feature specification.
- 🧠 Reflection: The process of updating the constitution and ensuring consistency across templates was successful.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): n/a
