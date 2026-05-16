---
name: task-split-skill
description: AI Agent 任务拆解方法论 — 将模糊需求拆解为可执行、可追踪、可验证的工作计划，支持读取 PLAN.md 生成 milestone + subTask
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
updated: 2026-05-17
version: "2.0.0"
license: MIT
tags:
  - task-management
  - methodology
  - agent-workflow
  - planning
platforms:
  all: true
depends_on:
  - plan-skill
---

# task-split-skill

## Overview

Task Decomposition Methodology — AI Agent 将模糊需求变成可执行、可追踪、可验证的工作计划的系统化方法。

**两种拆解模式：**
- **快速拆解**：无 PLAN.md 时，扁平任务列表
- **完整拆分**：有 PLAN.md 时，在 milestone 下拆 sub-task

---

## 核心原则：复述 + 人工确认

**所有关键信息必须经过「复述 + 用户确认」流程，LLM 自己理解的不算数。**

---

## 触发条件

| 触发词 | 说明 |
|--------|------|
| `任务拆解` / `拆解任务` | 核心触发 |
| `拆解成` / `分解成` | 带目标句式 |
| `工作分解` / `WBS` | 专业术语 |
| `开始执行` / `执行计划` | 触发完整拆分 |

**不触发：**

| 不触发 | 原因 |
|--------|------|
| `制定计划` / `写 PLAN` | → PLAN skill |
| `评审计划` / `review PLAN` | → plan-review-skill |
| `追踪目标` / `track goal` | → target-skill |

---

## 两种拆解模式

### 模式判断

```
拆解前检查 docs/PLAN.md 是否存在：
├── 存在 → 进入「完整拆分」模式
└── 不存在 → 进入「快速拆解」模式
```

---

## 快速拆解模式（无 PLAN.md）

### Step 1：澄清问题

```markdown
## 澄清问题（必须先问）

1. 最终交付物是什么？
2. 成功标准是什么？
3. 限制条件有哪些？
4. MVP vs 完整版？
```

### Step 2：识别交付物

每个子任务必须有验收标准。

### Step 3：分解排序

按依赖关系排序，识别并行分支。

### Step 4：风险预判

识别最可能的失败点。

### Step 5：输出任务列表

```markdown
## 拆解结果

**项目**：{目标}
**模式**：快速拆解

### 任务列表

| ID | 任务 | 验收标准 | 优先级 | 依赖 |
|----|------|---------|--------|------|
| 1 | {任务} | {标准} | P0 | — |
| 2 | {任务} | {标准} | P1 | #1 |
```

---

## 完整拆分模式（有 PLAN.md）

### Step 1：读取 PLAN.md + 复述确认

```markdown
## 我对 PLAN.md 的理解

**目标**：{LLM 理解的目标}

**里程碑**：
- M1：{标题} — 验收标准：{标准}
- M2：{标题} — 验收标准：{标准}

**交付物**：{交付物列表}

请确认以上理解是否正确，如有出入请告诉我。
```

### Step 2：在 milestone 下拆 sub-task

```markdown
### M1：{标题}

| ID | sub-task | 验收标准 | 优先级 |
|----|---------|---------|--------|
| M1-1 | {任务} | {标准} | P0 |
| M1-2 | {任务} | {标准} | P1 |
```

### Step 3：输出 milestone + subTask

```markdown
## 拆解结果

**项目**：{目标}
**模式**：完整拆分（基于 PLAN.md）

### Milestone + Sub-task

**M1：{标题}**
| ID | sub-task | 验收标准 | 优先级 | 状态 |
|----|---------|---------|--------|------|
| M1-1 | {任务} | {标准} | P0 | pending |
| M1-2 | {任务} | {标准} | P1 | pending |

**M2：{标题}**
| ID | sub-task | 验收标准 | 优先级 | 状态 |
|----|---------|---------|--------|------|
| M2-1 | {任务} | {标准} | P0 | pending |
```

### Step 4：后续选项

```markdown
### 下一步

1. **开始执行** — 使用 target-skill 追踪
2. **修改拆解** — 告诉我需要调整哪些任务
3. **添加任务** — 告诉我需要在哪个 milestone 下添加
```

---

## 与其他 Skill 的关系

### 与 PLAN skill 的关系

```
PLAN skill 生成 docs/PLAN.md
          ↓
task-split-skill 读取 docs/PLAN.md
          ↓
拆解任务
```

### 与 plan-review-skill 的关系

```
plan-review-skill 评审通过
          ↓
task-split-skill 拆解任务
```

### 与 target-skill 的关系

```
task-split-skill 拆解完成
          ↓
用户说「开始执行」
          ↓
target-skill 追踪 milestone + sub-task
```

---

## 版本字段

| 文件 | 版本字段 | 位置 |
|------|---------|------|
| `docs/PLAN.md` | `version` | frontmatter |

---

## 安装

```bash
git clone https://github.com/relunctance/task-split-skill.git ~/repos/task-split-skill
```
