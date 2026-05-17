<div align="center">

# task-split-skill

AI Agent 任务拆解方法论 v2.4 — 支持锚点拆解（拆解 M1、拆解 M2），将模糊需求拆解为可执行、可追踪、可验证的工作计划

</div>

---

## 核心特性

| 特性 | 说明 |
|------|------|
| 🔍 **Step 0 项目感知** | 拆解前先了解项目技术栈和结构 |
| ❓ **复述确认** | LLM 理解必须用户确认才视为有效 |
| 📋 **milestone + subTask** | 支持在里程碑下拆分子任务 |
| ✅ **验收标准强制** | 每个子任务必须有可检查的验收条件 |
| 🔄 **双模式** | 快速拆解（无PLAN）/ 完整拆分（有PLAN） |
| 🎯 **锚点拆解** | 支持拆解局部范围（拆解 M1、拆解 M2） |

## 触发条件

| 触发词 | 说明 |
|--------|------|
| `任务拆解` / `拆解任务` | 核心触发 |
| `拆解 M1` / `拆解 M1-3` | 锚点拆解，拆解指定里程碑 |

---

## 触发条件

| 触发词 | 说明 |
|--------|------|
| `任务拆解` / `拆解任务` / `拆解成` | 核心触发 |
| `工作分解` / `WBS` | 专业术语 |
| `开始执行` / `执行计划` | 触发完整拆分 |

**不触发**：`制定计划` → PLAN skill | `评审计划` → plan-review-skill | `追踪目标` → target-skill

---

## 快速开始

```bash
# 克隆到本地
git clone https://github.com/relunctance/task-split-skill.git ~/repos/task-split-skill

# 复制到 Hermes skills 目录
mkdir -p ~/.hermes/skills/task-split-skill
cp ~/repos/task-split-skill/SKILL.md ~/.hermes/skills/task-split-skill/
```

---

## 两种拆解模式

### 模式判断

```
拆解前检查 docs/PLAN.md 是否存在：
├── 存在 → 进入「完整拆分」模式
└── 不存在 → 进入「快速拆解」模式
```

### 完整拆分模式（有 PLAN.md）

```
Step 0: 项目上下文感知
Step 1: 读取 PLAN.md + 复述确认
Step 2: 在 milestone 下拆 sub-task
Step 3: 输出 milestone + subTask
Step 4: 写 .task-split.json
```

### 快速拆解模式（无 PLAN.md）

```
Step 0: 项目上下文感知
Step 1: 澄清问题（4个必问）
Step 2: 识别交付物
Step 3: 分解排序
Step 4: 风险预判
Step 5: 输出扁平任务列表
```

---

## 关键文件

| 文件 | 说明 |
|------|------|
| `docs/PLAN.md` | PLAN skill 生成的计划文档 |
| `.task-split.json` | task-split-skill 输出的任务拆解结果 |
| `.target-state.json` | target-skill 使用的追踪状态 |

---

## 与其他 Skill 的关系

```
PLAN skill → docs/PLAN.md
    ↓
task-split-skill → 读取 PLAN.md → .task-split.json
    ↓
target-skill → 读取 .task-split.json → .target-state.json
```

---

## 安装

```bash
git clone https://github.com/relunctance/task-split-skill.git ~/repos/task-split-skill
mkdir -p ~/.hermes/skills/task-split-skill
cp ~/repos/task-split-skill/SKILL.md ~/.hermes/skills/task-split-skill/
```

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.3.0 | 2026-05-17 | 新增Step0项目感知 + 边界情况处理 |
| 2.0.0 | 2026-05-17 | v2改造——支持读取PLAN.md生成milestone+subTask |
| 1.2.0 | 2026-05-15 | 初版发布 |

---

<div align="center">

MIT License © [relunctance](https://github.com/relunctance)

</div>
