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
version: "2.6.0"
license: MIT
tags:
  - task-management
  - methodology
  - agent-workflow
  - planning
platforms:
  all: true
depends_on:
  - plan-skill  # https://github.com/relunctance/plan-skill
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
| `评审计划` / `review PLAN` | → [plan-review-skill](https://github.com/relunctance/plan-review-skill) |
| `追踪目标` / `track goal` | → [target-skill](https://github.com/relunctance/target-skill) |

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

### Step 0：项目上下文感知（拆解前必做）

**如果项目目录已有内容，先理解项目再拆解：**

```markdown
## 🔍 项目上下文感知

正在分析项目结构...

**检测到的信息**：
- 技术栈：{package.json → React, requirements.txt → Python/FastAPI, go.mod → Go...}
- 项目结构：{src/, lib/, api/, docs/...}
- 现有代码模式：{existing patterns if readable}

**问题**：
1. 这个项目是 {技术栈} 的 {webapi/前端/CLI/库} 吗？
2. 现有代码有什么值得注意的模式？
3. 这次任务会影响哪些现有模块？

请告诉我以上信息是否准确，或纠正我的理解。
```

**项目上下文检测清单：**

| 检测项 | 命令/方法 | 说明 |
|--------|---------|------|
| 技术栈 | `package.json` / `requirements.txt` / `go.mod` / `Cargo.toml` / `pom.xml` | 识别主要技术栈 |
| 项目结构 | `ls` 根目录 | 识别 src/, lib/, api/, docs/ 等 |
| 框架 | 读 `package.json` 的 dependencies | React/Vue/Express 等 |
| 代码模式 | 抽检 2-3 个现有文件 | 了解项目规范 |
| 配置 | `.env.example` / `config/` | 了解配置模式 |

**如果项目为空（新目录）：**

```markdown
## 🔍 项目上下文感知

这是一个新项目。请告诉我：
1. 主要技术栈是什么？（Python/FastAPI, Node/Express, Go, etc.）
2. 项目类型？（Web API, CLI 工具, 前端应用, 库/SDK...）
3. 有特殊项目规范吗？
```

### Step 1：澄清问题

```markdown
## 澄清问题（必须先问）

基于对项目的理解，请回答：

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

### Step 0：项目上下文感知（与快速模式相同）

在读取 PLAN.md 前，先了解项目当前状态：

```markdown
## 🔍 项目上下文感知

正在分析项目结构...

**检测到的信息**：
- 技术栈：{package.json → React, requirements.txt → Python/FastAPI...}
- 项目结构：{src/, lib/, api/, docs/...}

**问题**：
1. 这个项目是 {技术栈} 的 {webapi/前端/CLI/库} 吗？
2. 现有代码有什么值得注意的模式？

请告诉我以上信息是否准确。
```

### Step 0.5：锚点识别（可选）

如果用户指定了锚点（如「拆解 M2」「拆解 M1-3」），先识别锚点：

```
1. 解析锚点：M2 / M1-3 / #架构 等
2. 定位锚点区域：
   - M2 → 找 milestones 表格 M2 行
   - M1-3 → 找 M1 + M2 + M3 行
   - #架构 → 找 "## 架构" 章节
3. 提取锚点覆盖的内容：
   - 里程碑的验收标准
   - 里程碑的交付物
   - 里程碑的截止日期
4. 确定拆解范围：只拆锚点覆盖的内容
5. 在输出中标记「来源锚点：M2」
```

**锚点解析规则**：
- `M1` → milestones 表格第 N 行
- `M1-3` → M1 + M2 + M3 行的验收标准
- `#架构` → `## 架构` 章节内容
- `表:交付物` → 标题含"交付物"的表格

**锚点拆解 vs 整文件拆解**：

| 场景 | 行为 |
|------|------|
| 用户说「拆解 M2」 | 进入锚点拆解，只拆 M2 范围 |
| 用户说「拆解整个计划」 | 进入整文件拆解 |
| 用户没说范围 | 询问「要拆解哪个范围？」 |

### Step 0.6：验收标准 L3 检查与自动转换

读取 PLAN.md 里程碑的验收标准后，检查是否为 L3（可测试命令）。

```
读取 PLAN.md milestones 表格的验收标准
    ↓
检查是否为 L3：
├── L3（有具体命令）→ ✅ 直接使用
├── L2（模糊表述）→ 自动转换为 L3：
│   「demo3 全流程跑通」
│   → 「python -m expert_teams team create --id demo --flow demo3
│       && python -m expert_teams flow advance demo
│       && python -m expert_teams flow advance demo
│       && python -m expert_teams team status demo」
└── L1（无）→ 🔴 拒绝执行，要求补充：
    「subTask【{task}】缺少验收标准，请补充后再拆解」
```

**L3 转换模板**：

| 原始表述 | L3 转换示例 |
|---------|------------|
| 「全流程跑通」 | `cmd1 && cmd2 && cmd3 && cmd4` |
| 「配置合理」 | `grep 'keyword' config.toml` |
| 「代码规范」 | `ruff check src/; echo $? 输出 0` |
| 「文档完整」 | `grep -E '安装|快速开始|API' README.md` |

**判断标准**：
- ✅ L3：有具体命令（`python xxx`, `pytest xxx`, `grep xxx`）
- ⚠️ L2：模糊表述（「跑通」「合理」「完整」）
- ❌ L1：无任何验收条件

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

|| ID | sub-task | 验收标准 | 优先级 |
||----|---------|---------|---------|
|| M1-1 | {任务} | {标准} | P0 |
|| M1-2 | {任务} | {标准} | P1 |
```

### Step 2.5：验收标准必须为 L3（可测试命令）

**规则**：每个 subTask 的验收标准必须是 L3（可测试命令）。

| 等级 | 定义 | 例子 | 行为 |
|------|------|------|------|
| L3 可测试 | 有确定性命令，返回明确结果 | `pytest tests/ -v` 返回 PASSED | ✅ 合格 |
| L2 模糊 | 有验收条件但无法自动判断 | 「配置合理」「代码规范」 | ❌ 不合格 |
| L1 无 | 无任何验收条件 | 「完成开发」「完善功能」 | ❌ 不合格 |

**常见 L3 验收标准模板**：

| subTask 类型 | L3 验收标准模板 | 示例 |
|-------------|----------------|------|
| CLI 命令 | `{命令}; echo $? 输出 0` | `ruff check src/; echo $? 输出 0` |
| 文件存在 | `test -f {path}` | `test -f flows/demo3.toml` |
| 配置内容 | `grep '{keyword}' {path}` | `grep 'plan\|implement\|test' flows/demo3.toml` |
| JSON 字段 | `{命令} 输出包含 {field}` | `team status demo 输出包含 current_phase` |
| 测试通过 | `pytest {path} -v` | `pytest tests/ -v` |
| 端到端 | `{完整流程} 返回 {预期}` | `create → advance × 2 → status 返回 current_phase=test` |

**判断 SOP**：

```
生成验收标准后
    ↓
检查是否为 L3：
├── 有具体命令 → ✅ 合格
└── 无命令或模糊 → ❌ 拒绝，输出：
    「验收标准【{模糊内容}】不可测试。建议改为：{L3模板}」
```

### Step 3：输出 milestone + subTask

如果使用了锚点拆解，在输出中标记来源：

```markdown
## 拆解结果（锚点拆解）

> **来源锚点**：M2
> **覆盖范围**：M2 验收标准 + 交付物

### milestone: M2

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

1. **开始执行** — 使用 [target-skill](https://github.com/relunctance/target-skill) 追踪
2. **修改拆解** — 告诉我需要调整哪些任务
3. **添加任务** — 告诉我需要在哪个 milestone 下添加
```

**用户选择「开始执行」后：**

1. **写 `.task-split.json`**：将 milestone + subTask 写入项目根目录
2. **提示用户**：可以输入「开始执行」触发 [target-skill](https://github.com/relunctance/target-skill)

```markdown
## ✅ 拆解结果已保存

**文件**：`{项目根目录}/.task-split.json`

**下一步**：
1. 输入「开始执行」— 触发 target-skill 追踪
2. 输入「修改拆解」— 调整任务
```

### .task-split.json 格式

```json
{
  "version": "1.0",
  "goal": "{项目目标}",
  "source": "PLAN.md",
  "createdAt": "YYYY-MM-DDTHH:mm:ss+08:00",
  "milestones": [
    {
      "id": "M1",
      "title": "{标题}",
      "status": "pending",
      "subTasks": [
        {
          "id": "M1-1",
          "title": "{任务}",
          "status": "pending",
          "priority": "P0",
          "acceptanceCriteria": "{验收标准}"
        }
      ]
    }
  ]
}
```

**注意**：`.task-split.json` 是 task-split-skill 的输出，target-skill 读取后可转换为 `.target-state.json`。两个文件可以共存。

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

### 与 [plan-review-skill](https://github.com/relunctance/plan-review-skill) 的关系

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

## 边界情况处理

### 常见错误与处理

| 边界情况 | 识别方法 | 处理方式 |
|---------|---------|---------|
| PLAN.md 表格损坏 | 解析失败 | 提示用户「PLAN.md 格式有误，请检查表格」 |
| .task-split.json 被手动修改 | JSON 无效 | 提示用户「.task-split.json 格式错误，请重新拆解」 |
| milestone ID 重复 | 解析时发现重复 | 重命名为 M1a, M1b |
| subTask ID 缺少 milestone 前缀 | ID 不匹配 | 自动补充前缀（如 1 → M1-1） |
| 用户跳过 Step 0 直接拆解 | 未执行上下文感知 | 提示「建议先执行 Step 0 了解项目」 |

### 错误提示模板

```markdown
## ⚠️ PLAN.md 解析失败

**问题**：无法解析里程碑表格

**原因**：表格格式不正确或缺少必需列

**修复**：请检查 docs/PLAN.md 中的里程碑表格：
- 必须包含列：ID, 里程碑, 验收标准
- 每行必须有 ID（如 M1, M2）

请修正后重新执行「拆解任务」。
```

```markdown
## ⚠️ .task-split.json 格式错误

**问题**：JSON 解析失败

**原因**：文件内容不是有效的 JSON

**修复**：
1. 输入「修改拆解」重新生成
2. 或手动修正 JSON 格式

请修正后重新执行「开始执行」。
```

```markdown
## ⚠️ 缺少项目上下文

**问题**：未执行 Step 0 项目上下文感知

**建议**：建议先了解项目再拆解，这样任务更准确。

输入「继续拆解」跳过此步骤，
或告诉我项目的基本信息。
```

### 依赖检测

```markdown
## 🔍 依赖检测

拆解前检查以下文件是否存在：

| 文件 | 需要性 | 状态 |
|------|--------|------|
| docs/PLAN.md | 可选 | ✅ 存在 / ❌ 不存在 |
| package.json | 可选 | ✅ 存在 / ❌ 不存在 |
| requirements.txt | 可选 | ✅ 存在 / ❌ 不存在 |

**下一步**：
1. 如果有 PLAN.md → 进入「完整拆分」模式
2. 如果无 PLAN.md 但有其他文件 → 执行 Step 0 后进入「快速拆解」模式
3. 如果无任何文件 → 新项目，执行 Step 0 后进入「快速拆解」模式
```

---

## 版本字段

| 文件 | 版本字段 | 位置 |
|------|---------|------|
| `docs/PLAN.md` | `version` | frontmatter |

---

## 参考资料

- [subTask 验收标准规范](references/subtask-acceptance-standard.md) — L3/L2/L1 分级，合格/不合格示例，与 target-skill v3 的契约

## 安装

```bash
git clone https://github.com/relunctance/task-split-skill.git ~/repos/task-split-skill
```
