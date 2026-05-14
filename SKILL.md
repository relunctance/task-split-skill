---
name: task-split
description: AI Agent task decomposition methodology for breaking complex requests into executable, trackable, verifiable work plans
description_zh: AI Agent 任务拆解方法论 — 将模糊需求拆解为可执行、可追踪、可验证的工作计划
triggers:
  - 任务拆解
  - task decomposition
  - 拆解任务
  - 任务规划
  - task planning
  - 子任务
  - 工作分解
  - WBS
category: methodology
author: relunctance
created: 2026-05-14
updated: 2026-05-14
version: "1.0.0"
tags:
  - task-management
  - methodology
  - agent-workflow
  - planning
platforms:
  openclaw: true
  claude_code: true
  hermes: true
---

# task-split

## Overview

Task Decomposition Methodology — a systematic approach for AI Agents to break down vague user requests into executable, trackable, and verifiable work plans.

任务拆解方法论 — AI Agent 将模糊需求变成可执行、可追踪、可验证的工作计划的系统化方法。

## Triggers

- 任务拆解 / task decomposition
- 拆解任务 / 拆解
- 任务规划 / task planning
- 子任务 / 工作分解 / WBS

## Content

### 1. Why Task Decomposition

| Problem | Without | With |
|---------|---------|------|
| Wrong direction | Discover misalignment after completion | Expose ambiguity during decomposition |
| Opaque progress | User waits for final result | Visible progress at every step |
| Risk accumulation | Errors compound at the end | Each step validated independently |
| Context loss | Start over after interruption | Resume from task list seamlessly |
| Parallelism | Only serial execution | Independent subtasks run concurrently |

### 2. Five-Step Decomposition Flow

```
User Request (vague)
    │
    ▼
┌─────────────────────────┐
│ Step 1: Understand       │  → What is the core goal?
│         & Clarify        │  → Hidden constraints or preferences?
│                          │  → Need Plan Mode?
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│ Step 2: Identify         │  → What files/features to deliver?
│         Deliverables     │  → What are acceptance criteria?
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│ Step 3: Break Down       │  → Order by dependency (topological)
│         & Order          │  → Identify parallel branches
│                          │  → Each task < 15 min ideal
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│ Step 4: Risk Assessment  │  → Which steps might fail?
│         & Defense        │  → Where does user confirmation needed?
│                          │  → What is Plan B?
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│ Step 5: Create Task List │  → TaskCreate for each item
│         & Track          │  → Mark dependencies (addBlockedBy)
│                          │  → Execute + real-time status update
└─────────────────────────┘
```

### 3. Granularity Principles

#### When to Decompose

```
✅ Must decompose:
├── Modifying 3+ files
├── Clear sequential dependencies (A before B)
├── Uncertain factors (needs research first)
├── Execution time > 5 minutes
├── Multiple possible approaches (needs decision)
└── User needs to see intermediate progress

❌ Skip decomposition:
├── Single-line fix (typo)
├── Pure information lookup (read file, check docs)
├── Simple formatting adjustment
└── User explicitly says "just do it" for simple tasks
```

#### Granularity Reference

| Level | Example | Use Case |
|-------|---------|----------|
| **Atomic** | "Fix STATUS.md regex `[a-z]` → `[a-z][^|]+`" | Specific code change |
| **Composite** | "Implement README update in create_role.py" | One logical unit |
| **Milestone** | "Complete CLI scaffold (template→validate→update docs)" | Deliverable feature |

#### Golden Rule

> **A task description should be executable by another Agent without additional context.**

```
❌ Bad: "Improve documentation"
✅ Good: "Append new role row to docs/STATUS.md table, format: | role-name | description | ✅ |"

❌ Bad: "Handle config file"
✅ Good: "Replace name: my-role with user-specified role name in templates/role-template/config.yaml"
```

Task description template:
```
[verb] + [object] + [specific detail] + [acceptance criteria]
```

### 4. Dependency Modeling

#### Serial Dependency (most common)

```
[Research API docs] → [Design data model] → [Implement backend] → [Build frontend]
       ①                    ②                    ③                  ④
```

Use `addBlockedBy`: Task ② is blocked by ①, Task ③ by ②.

#### Parallel Branches (efficiency key)

```
         ┌→ [Build page A] ─┐
[Design] ┤                   ├→ [Integration test]
         └→ [Build page B] ─┘
```

Independent tasks can launch multiple Agents in parallel.

#### Diamond Dependency

```
[Backend API dev] ──┐
                    ├──→ [Frontend-Backend integration]
[Frontend dev]    ──┘
```

Two branches converge at an integration point. Either branch failure blocks convergence.

### 5. Dynamic Adjustment During Execution

#### Task State Flow

```
pending → in_progress → completed
                        → pending (rollback & redo)
                        → deleted (no longer needed)
```

#### Common Adjustment Scenarios

| Scenario | Action |
|----------|--------|
| Discover prerequisite | Pause current task, insert new prerequisite |
| Task no longer needed | Mark deleted, unblock downstream |
| Better approach found | Record new approach in description, continue |
| Over-decomposed | Merge related tasks to reduce switching |
| Blocked (need user input) | Pause task, use AskUserQuestion |

### 6. Relationship with Skills

```
User Request
    │
    ▼
Task Decomposition (thinking process)
    │
    ├── Subtask A ──→ Match existing Skill?
    │                 ├── ✅ Invoke directly (instant)
    │                 └── ❌ Manual execution
    │
    ├── Subtask B ──→ Match existing Skill?
    │                 ├── ✅ Invoke directly
    │                 └── ❌ Manual execution
    │
    └── After completion → Is this flow reusable?
                            ├── ✅ Extract as new Skill
                            └── ❌ Update Memory only
```

**Key distinctions:**
- **Task Decomposition** = "Thinking process" that runs every time (never skip)
- **Skill** = "Shortcut" for decomposition results (use if available)
- **Memory** = "Notebook" of lessons learned (reference next time)

### 7. Cheatsheet

```
┌─────────────────────────────────────────────────┐
│         TASK DECOMPOSITION CHEATSHEET            │
├─────────────────────────────────────────────────┤
│                                                  │
│  After receiving a request, ask:                 │
│  ├── What is the final deliverable?              │
│  ├── How many files need changes?                │
│  ├── Any uncertainty to confirm first?           │
│  └── Which steps can run in parallel?            │
│                                                  │
│  Task description template:                      │
│  [verb] + [object] + [detail] + [criteria]      │
│                                                  │
│  Granularity:                                    │
│  ├── Simple: no split (< 3 steps)                │
│  ├── Medium: 3-8 subtasks                        │
│  └── Complex: 8+ subtasks + milestone groups     │
│                                                  │
│  Execution rhythm:                               │
│  ├── Research/confirm first, then implement      │
│  ├── Core logic first, then edge cases           │
│  ├── Feature first, then docs                    │
│  └── Update status immediately after each task   │
│                                                  │
└─────────────────────────────────────────────────┘
```

## Pitfalls

| Issue | Solution |
|-------|----------|
| Over-decomposition into micro-tasks | Merge tasks that share the same file/context |
| Under-decomposition (vague tasks) | Apply golden rule: description must be self-contained |
| Missing dependencies | Always ask "what must finish before this?" |
| Not updating status | Treat status update as part of the task, not optional |
| Ignoring parallel opportunities | Always check "can any of these run simultaneously?" |
| Skipping risk assessment | At minimum, identify the 1-2 most likely failure points |

## Installation

### OpenClaw
```bash
clawhub install task-split
```

### Claude Code
```bash
mkdir -p ~/claude/skills/task-split
cp SKILL.md ~/claude/skills/task-split/
```

### Hermes
```bash
mkdir -p ~/.hermes/skills/task-split
cp SKILL.md ~/.hermes/skills/task-split/
```
