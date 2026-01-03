<!--
Sync Impact Report:
- Version change: 0.1.0 -> 1.0.0
- List of modified principles:
  - All principles replaced with new structure.
- Added sections:
  - Core Principle
  - Decision Hierarchy
  - Allowed Actions
  - Forbidden Actions
  - Coding Standards
  - Error Handling
  - Review Rules
  - Evolution Constraint
- Removed sections:
  - All template sections removed.
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md
  - ✅ .specify/templates/spec-template.md
  - ✅ .specify/templates/tasks-template.md
- Follow-up TODOs:
  - None
-->

# AI Constitution – Evolution of Todo Project

## Core Principle
This project follows strict spec-driven, agentic development.
No code may be written unless explicitly derived from an approved specification.

## Decision Hierarchy
1. Specification files (Spec-Kit Plus) – highest authority
2. Constitution.md
3. Claude.md instructions
4. README.md
5. AI-generated plans and tasks
6. Code implementation

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

## Forbidden Actions
- No manual coding by humans
- No speculative features
- No hardcoding outside defined specs
- No external dependencies unless explicitly specified

## Coding Standards
- Python 3.13+
- Type hints required
- Single responsibility principle
- Clear separation of:
  - Models
  - Services
  - CLI interface
- Deterministic behavior (no randomness)

## Error Handling
- Fail fast
- User-facing CLI errors must be readable
- Internal errors must raise exceptions

## Review Rules
- Every phase must include:
  - Spec history
  - Plan
  - Tasks
  - Implementation
- If spec conflicts exist, STOP and request clarification

## Evolution Constraint
Design decisions must not block future evolution into:
- Persistent storage
- APIs
- Distributed systems
- Event-driven architecture

## Governance
This constitution supersedes all other practices. Amendments require documentation and approval. All pull requests and reviews must verify compliance with this constitution.

**Version**: 1.0.0 | **Ratified**: 2026-01-02 | **Last Amended**: 2026-01-02