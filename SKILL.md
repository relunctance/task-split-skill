---
name: task-split-skill
description: AI Agent task decomposition methodology for breaking complex requests into executable, trackable, verifiable work plans
description_zh: AI Agent 任务拆解方法论 — 将模糊需求拆解为可执行、可追踪、可验证的工作计划
triggers:
  - 任务拆解
  - 拆解任务
  - 拆解成
  - 分解成
  - 工作分解
  - WBS
  - task decomposition
  - task split
category: methodology
author: relunctance
created: 2026-05-14
updated: 2026-05-15
version: "1.2.0"
license: MIT
tags:
  - task-management
  - methodology
  - agent-workflow
  - planning
platforms:
  openclaw: true
  claude_code: true
  hermes: true
  cursor: true
metadata:
  scripts:
    - scripts/task-list.py
    - scripts/setup.sh
---

# task-split-skill

## Overview

Task Decomposition Methodology — a systematic approach for AI Agents to break down vague user requests into executable, trackable, and verifiable work plans.

任务拆解方法论 — AI Agent 将模糊需求变成可执行、可追踪、可验证的工作计划的系统化方法。

## Triggers

> **⚠️ 与 OpenSpec 的触发边界**：OpenSpec 由 `/opsx:` 命令触发，task-split 由自然语言触发。两者互不冲突，OpenSpec 管「开发规范」，task-split 管「任务拆解」。

| 触发词 | 说明 |
|--------|------|
| `任务拆解` / `拆解任务` | 核心触发词 |
| `拆解成` / `分解成` | 带目标句式，如「拆解成 N 个子任务」 |
| `工作分解` / `WBS` | 专业术语 |
| `task decomposition` / `task split` | 英文触发 |

**不触发**（这些是 OpenSpec 或其他 skill 的领域）：
- `/opsx:` 开头的命令 → OpenSpec
- `制定开发规范` / `写 SPEC` → OpenSpec
- `目标追踪` / `目标管理` → target-skill

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
│ Step 1: Clarify Questions │  ← 必须先问清楚，不清楚不拆解
│         (Question Template)│
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│ Step 2: Identify         │  → What files/features to deliver?
│         Deliverables     │  → Acceptance criteria for each (MANDATORY)
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
│ Step 5: Create Task List │  → task-list.py create for each item
│         & Track          │  → --depends for dependencies
│                          │  → Execute + real-time status update
└─────────────────────────┘
```

### 3. Clarify Question Template (Step 1 必填)

> **每任务拆解前必须完成 Step 1 的 4 个问题，未澄清前不进入 Step 2。**

```
## 澄清问题（每任务必答）

1. 最终交付物是什么？
   → 文件 / 功能模块 / 文档 / API endpoint / 配置项
   → 具体路径或位置（如：src/auth/login.ts）

2. 成功标准是什么？
   → 可运行 / 可部署 / 评审通过
   → 具体可检查的指标（如：登录成功返回 200，失败返回 401）

3. 限制条件有哪些？
   → 技术栈限制 / 时间限制 / 兼容性要求 / 安全约束
   → 如无限制，明确写「无特殊限制」

4. MVP 范围 vs 完整版范围？
   → 必须有的（MVP）：...
   → 可以有的（后续迭代）：...
   → 绝对不能有的：...
```

**什么时候可以跳过 Step 1？**
- 用户需求已经非常具体（不超过 2 句话，包含明确动词+对象）
- 示例：「把 users.ts 里的 `getUserById` 改成 async/await」→ 直接拆解

### 4. Deliverables & Acceptance Criteria (Step 2 强制)

> **每个子任务必须有验收标准，无验收标准则任务不完整。**

```markdown
## 交付物清单

### 交付物 1：[具体名称]
**文件/位置**：
**验收标准**：
- [ ] 标准 1（具体、可执行检查）
- [ ] 标准 2（包含预期结果）
- [ ] 标准 3（边界条件）
```

```
❌ Bad: "功能正常运行"
✅ Good: "POST /api/login 返回 200 + token 字段；空 body 返回 400；密码错误返回 401"

❌ Bad: "完善文档"
✅ Good: "README.md 包含：安装步骤（3步）、快速开始（2个命令）、troubleshooting（4个常见问题）"
```

### 5. Granularity Principles

#### When to Decompose

```
✅ Must decompose:
├── Modifying 3+ files
├── Clear sequential dependencies (A before B)
├── Uncertain factors (needs research first)
├── Execution time > 5 minutes
├── Multiple possible approaches (needs decision)
└── User needs to see intermediate progress

❌ MUST NOT decompose (skip decomposition entirely):
├── Single-line fix (typo, missing semicolon)
├── Pure information lookup (read file, check docs, grep)
├── Simple formatting adjustment (prettier, lint fix)
├── User explicitly says "just do it" for simple tasks
├── Output is a single command or API call
└── Task is already a single atomic action (< 2 min)
```

#### Granularity Reference

| Level | Example | Use Case |
|-------|---------|----------|
| **Atomic** | "Fix STATUS.md regex `[a-z]` → `[a-z][^\|]+`" | Specific code change |
| **Composite** | "Implement README update in create_role.py" | One logical unit |
| **Milestone** | "Complete CLI scaffold (template→validate→update docs)" | Deliverable feature |

#### Golden Rule

> **A task description should be executable by another Agent without additional context.**

```
❌ Bad: "Improve documentation"
✅ Good: "Append new role row to docs/STATUS.md table, format: | role-name | description | ✅ |"

❌ Bad: "Handle config file"
✅ Good: "Replace name: my-role with user-specified role name in templates/role-template/config.yaml"

❌ Bad: "Add error handling"
✅ Good: "Add try/catch around db.query() in src/db/user.go; on exception log error and return ErrDatabase"
```

Task description template:
```
[verb] + [object] + [specific file/path] + [exact change] + [acceptance criteria]
```

### 6. Dependency Modeling

#### Serial Dependency (most common)

```
[Research API docs] → [Design data model] → [Implement backend] → [Build frontend]
       ①                    ②                    ③                  ④
```

Use `task-list.py create "title" --depends 1,2` to establish dependencies.

#### Parallel Branches (efficiency key)

```
         ┌→ [Build page A] ─┐
[Design] ┤                   ├→ [Integration test]
         └→ [Build page B] ─┘
```

Independent tasks can launch multiple Agents in parallel using `task-list.py tree` to visualize.

#### Diamond Dependency

```
[Backend API dev] ──┐
                    ├──→ [Frontend-Backend integration]
[Frontend dev]    ──┘
```

Two branches converge at an integration point. Either branch failure blocks convergence.

### 7. Dynamic Adjustment During Execution

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

### 8. Relationship with Other Skills

#### 与 OpenSpec 的边界

| Skill | 职责 | 触发方式 |
|-------|------|---------|
| **task-split** | 将需求拆解为可执行子任务 | 自然语言 |
| **OpenSpec** | 定义开发规范和标准 | `/opsx:` 命令 |
| **target-skill** | 追踪长期目标，抗偏移 | 用户主动开启追踪 |

**协作建议**：
- 大需求 → 先 task-split 拆解 → 对核心模块用 OpenSpec 定义规范
- task-split 的输出（子任务列表）可以作为 target-skill 的输入
- 如果 target-skill 标记某个目标为 P3，但 task-split 拆出 P0 子任务 → **以 task-split 的优先级为准**，但提醒用户目标与任务的优先级不一致

#### 与 skill-created 的关系

```
User Request
    │
    ▼
Task Decomposition
    │
    ├── Subtask A ──→ Match existing Skill?
    │                 ├── ✅ Invoke directly (instant)
    │                 └── ❌ Manual execution
    │
    └── After completion → Is this flow reusable?
                            ├── ✅ Use skill-created to extract as new Skill
                            └── ❌ Update Memory only
```

**Key distinctions:**
- **Task Decomposition** = "Thinking process" that runs every time (never skip)
- **Skill** = "Shortcut" for decomposition results (use if available)
- **Memory** = "Notebook" of lessons learned (reference next time)

### 9. Priority Definitions

| Priority | Meaning | Response |
|----------|---------|----------|
| **P0** | 阻断性问题，必须立即解决 | 停下手头所有工作，先处理 P0 |
| **P1** | 核心功能，影响主流程 | 尽快完成，不阻塞其他 P1 |
| **P2** | 重要但不紧急 | 按正常流程完成 |
| **P3** | 增强/优化 | 有余力再做 |

**Decision rule**: If you can't decide between P0 and P1, ask the user.

### 10. task-list.py CLI Reference

> **依赖建模和任务追踪的唯一工具**。每个子任务创建后必须用 task-list.py 管理，不允许用其他方式追踪。

#### 安装脚本

```bash
# 自动安装（推荐）
bash ~/repos/task-split-skill/scripts/setup.sh

# 或手动同步
python3 ~/repos/skill-sync/scripts/sync-hermes-skills.py task-split-skill
```

#### 命令行接口

```bash
# 创建任务（依赖用逗号分隔的 ID）
python task-list.py create "任务标题" --priority P0 --depends 1,2

# 列举任务（可选：按状态/优先级过滤）
python task-list.py list                          # 所有任务
python task-list.py list --status pending         # 仅待完成
python task-list.py list --priority P0            # 仅 P0

# 开始任务（自动检查依赖是否完成）
python task-list.py start 1

# 完成任务
python task-list.py done 1

# 阻塞任务（标记依赖）
python task-list.py block 3 --by 1,2

# 解除阻塞
python task-list.py unblock 3

# 删除任务
python task-list.py delete 3

# 依赖树视图
python task-list.py tree

# 统计面板
python task-list.py stats
```

#### 典型工作流

```bash
# 1. 拆解完成后，创建所有任务
python task-list.py create "调研 API 文档" --priority P1
python task-list.py create "设计数据模型" --priority P1 --depends 1
python task-list.py create "实现后端 API" --priority P1 --depends 2
python task-list.py create "开发前端页面" --priority P2 --depends 2
python task-list.py create "集成测试" --priority P1 --depends 3,4

# 2. 查看依赖树
python task-list.py tree

# 3. 开始 P0/P1 任务（被依赖阻塞的会自动报错）
python task-list.py start 1

# 4. 完成后标记
python task-list.py done 1
python task-list.py start 2

# 5. 查看进度
python task-list.py stats
```

### 11. Cheatsheet

```
┌──────────────────────────────────────────────────────────┐
│              TASK DECOMPOSITION CHEATSHEET               │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Triggers (自然语言触发):                                 │
│  ├── 任务拆解 / 拆解任务 / 拆解成                         │
│  ├── 工作分解 / WBS                                      │
│  └── task decomposition / task split                    │
│  ⚠️ 不触发：/opsx: 命令 → OpenSpec                       │
│                                                          │
│  ─────────────────────────────────────────────────────   │
│                                                          │
│  5-Step Flow:                                            │
│  ① 澄清问题 → ② 识别交付物 → ③ 分解排序                 │
│  ④ 风险预判 → ⑤ 执行追踪                                 │
│                                                          │
│  ─────────────────────────────────────────────────────   │
│                                                          │
│  Step 1 必填（4个问题）：                                 │
│  ① 最终交付物是什么？                                     │
│  ② 成功标准是什么？                                       │
│  ③ 限制条件有哪些？                                       │
│  ④ MVP vs 完整版？                                       │
│                                                          │
│  ─────────────────────────────────────────────────────   │
│                                                          │
│  Step 2 必填（每个子任务）：                               │
│  ## 验收标准                                            │
│  - [ ] 具体条件1                                         │
│  - [ ] 具体条件2                                         │
│                                                          │
│  ─────────────────────────────────────────────────────   │
│                                                          │
│  Task description:                                       │
│  [verb] + [object] + [file/path] + [exact change]      │
│                                                          │
│  Priority:                                               │
│  P0 = 阻断优先 | P1 = 核心尽快 | P2/P3 = 有余力           │
│                                                          │
│  ─────────────────────────────────────────────────────   │
│                                                          │
│  task-list.py:                                          │
│  create "title" --priority P0 --depends 1,2             │
│  list --status pending --priority P0                    │
│  start / done / block / unblock / delete <id>           │
│  tree | stats                                            │
│                                                          │
│  Granularity:                                            │
│  ✅ > 5min / 3+ files / 多个方案 → 必须拆解               │
│  ❌ 单行fix / 纯查询 / "just do it" → 不拆解             │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Pitfalls

| Issue | Solution |
|-------|----------|
| Over-decomposition into micro-tasks | Merge tasks that share the same file/context |
| Under-decomposition (vague tasks) | Apply golden rule: description must be self-contained |
| Missing dependencies | Always ask "what must finish before this?" |
| Skipping Step 1 Clarify | Treat Clarify as mandatory for anything beyond 2 sentences |
| No acceptance criteria | Reject the decomposition until every task has checkable criteria |
| Not updating status | Treat status update as part of the task, not optional |
| Ignoring parallel opportunities | Always check "can any of these run simultaneously?" |
| Skipping risk assessment | At minimum, identify the 1-2 most likely failure points |
| Trigger conflict with OpenSpec | OpenSpec uses `/opsx:` — if user doesn't use that prefix, use task-split |

## Installation

### Hermes
```bash
mkdir -p ~/.hermes/skills/task-split
cp SKILL.md ~/.hermes/skills/task-split/
# 安装依赖脚本（可选）
bash scripts/setup.sh
```

### OpenClaw
```bash
clawhub install task-split
```

### Claude Code
```bash
mkdir -p ~/claude/skills/task-split
cp SKILL.md ~/claude/skills/task-split/
```

### Cursor
```bash
mkdir -p .cursor/rules
cp SKILL.md .cursor/rules/task-split.md
```
