# AGENTS.md - AI Agent Instructions

## Purpose

This project uses **Spec-Driven Development (SDD)** - a workflow where **no agent is allowed to write code until the specification is complete and approved**.

All AI agents (Claude, Copilot, Gemini, local LLMs, etc.) must follow the **Spec-Kit lifecycle**:

> **Specify -> Plan -> Tasks -> Implement**

This prevents "vibe coding," ensures alignment across agents, and guarantees that every implementation step maps back to an explicit requirement.

---

## How Agents Must Work

Every agent in this project MUST obey these rules:

1. **Never generate code without a referenced Task ID.**
2. **Never modify architecture without updating `specs/001-todo-crud/plan.md`.**
3. **Never propose features without updating specification files (WHAT).**
4. **Never change approach without updating `.specify/memory/constitution.md` (Principles).**
5. **Every code file must contain a comment linking it to the Task and Spec sections.**

If an agent cannot find the required spec, it must **stop and request it**, not improvise.

---

## Spec-Kit Workflow (Source of Truth)

### 1. Constitution (WHY - Principles & Constraints)

File: `.specify/memory/constitution.md`

Defines the project's non-negotiables: architecture values, security rules, tech stack constraints, performance expectations, and patterns allowed.

Agents must check this before proposing solutions.

---

### 2. Specify (WHAT - Requirements, Journeys & Acceptance Criteria)

File: `specs/001-todo-crud/spec.md`

Contains:
- User journeys
- Requirements
- Acceptance criteria
- Domain rules
- Business constraints

Agents must not infer missing requirements - they must request clarification or propose specification updates.

---

### 3. Plan (HOW - Architecture, Components, Interfaces)

File: `specs/001-todo-crud/plan.md`

Includes:
- Component breakdown
- APIs & schema diagrams
- Service boundaries
- System responsibilities
- High-level sequencing

All architectural output MUST be generated from the Specify file.

---

### 4. Tasks (BREAKDOWN - Atomic, Testable Work Units)

File: `specs/001-todo-crud/tasks.md`

Each Task must contain:
- Task ID
- Clear description
- Preconditions
- Expected outputs
- Artifacts to modify
- Links back to Specify + Plan sections

Agents **implement only what these tasks define**.

---

### 5. Implement (CODE - Write Only What the Tasks Authorize)

Agents now write code, but must:
- Reference Task IDs
- Follow the Plan exactly
- Not invent new features or flows
- Stop and request clarification if anything is underspecified

> The golden rule: **No task = No code.**

---

## Agent Behavior in This Project

### When generating code:

Agents must reference:
```
[Task]: T-001
[From]: specs/001-todo-crud/spec.md Section 2.1, plan.md Section 3.4
```

### When proposing architecture:

Agents must reference:
```
Update required in specs/001-todo-crud/plan.md -> add component X
```

### When proposing new behavior or a new feature:

Agents must reference:
```
Requires update in specs/001-todo-crud/spec.md (WHAT)
```

### When changing principles:

Agents must reference:
```
Modify .specify/memory/constitution.md -> Principle #X
```

---

## Agent Failure Modes (What Agents MUST Avoid)

Agents are NOT allowed to:
- Freestyle code or architecture
- Generate missing requirements
- Create tasks on their own
- Alter stack choices without justification
- Add endpoints, fields, or flows that aren't in the spec
- Ignore acceptance criteria
- Produce "creative" implementations that violate the plan

If a conflict arises between spec files, the **Constitution > Specify > Plan > Tasks** hierarchy applies.

---

## Developer-Agent Alignment

Humans and agents collaborate, but the **spec is the single source of truth**.

Before every session, agents should re-read:
1. `.specify/memory/constitution.md`
2. `specs/001-todo-crud/spec.md`
3. `specs/001-todo-crud/tasks.md`

This ensures predictable, deterministic development.

---

## Project-Specific Agent Tools

### Spec-Kit Plus Commands

Agents with MCP access can use:
- `specifyplus specify` - Create/update specifications
- `specifyplus plan` - Generate technical plans
- `specifyplus tasks` - Break plans into tasks
- `specifyplus implement` - Execute implementations

### File References

Use `@` prefix to reference files:
- `@specs/001-todo-crud/spec.md`
- `@.specify/memory/constitution.md`
- `@CLAUDE.md`

---

## Hackathon Phase Requirements

| Phase | Key Technologies | Status |
|-------|-----------------|--------|
| I | Python CLI, argparse | Complete |
| II | Next.js, FastAPI, Better Auth, Neon DB | Complete |
| III | OpenAI Assistants, MCP, ChatKit | Complete |
| IV | Docker, Helm, Minikube | Complete |
| V | Kafka, Dapr, DigitalOcean | In Progress |

---

## Governance

This AGENTS.md file supersedes all other agent practices. Amendments require documentation and approval. All AI-generated code must verify compliance with this file.

**Version**: 1.0.0 | **Created**: 2026-02-06
