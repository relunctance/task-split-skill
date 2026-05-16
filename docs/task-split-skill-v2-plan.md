# task-split-skill v2 调整方案

> 核心原则：代码最少化，无 PLAN.md 时独立工作，有 PLAN.md 时对接 target-skill。

## 三 Skill 定位对比

| Skill | 核心功能 | 输出 | 状态管理 |
|-------|---------|------|---------|
| **plan-review-skill** | 规划评审 | PLAN.md + `.target-trigger` | PLAN.md frontmatter |
| **task-split-skill** | 任务拆解 | milestone + subTask 或扁平列表 | task-list.py |
| **target-skill** | 目标追踪 | milestone + subTask 追踪 | `.target-state.json` |

## 调整后的 workflow

```
plan-review-skill（评审通过）
    ↓ 写 .target-trigger
target-skill（启动）
    ↓ 读取 PLAN.md
    ↓ 发现 milestone 需要拆解
    ↓ 触发 task-split-skill
task-split-skill（在 milestone 下拆 sub-task）
    ↓ 输出 milestone + subTask
target-skill（接管追踪）
```

## 核心调整

### 读取 PLAN.md

**如果 `docs/PLAN.md` 存在**：
- 读取「项目愿景」作为目标
- 读取「里程碑」表格继承 milestone
- 在每个 milestone 下拆 sub-task
- 不再重复问 Step 1 的 4 个澄清问题

**如果 `docs/PLAN.md` 不存在**：
- 保留原有 Step 1 澄清流程（向后兼容）

### 两种输出模式

| 模式 | 触发条件 | 输出 |
|------|---------|------|
| 快速拆解 | 用户说「拆解一下」（无 PLAN.md） | 扁平任务列表（维持现状） |
| 完整拆分 | 用户说「开始执行」（有 PLAN.md） | milestone + subTask 结构（对接 target-skill） |

### 输出格式（对标 .target-state.json）

```json
{
  "goal": "项目愿景",
  "source": "plan-review",
  "milestones": [
    {
      "id": "M1",
      "title": "数据库设计",
      "status": "pending",
      "subTasks": [
        {
          "id": "M1-1",
          "title": "设计用户表 schema",
          "status": "pending"
        }
      ]
    }
  ]
}
```

## 改动范围

| 文件 | 改动 |
|------|------|
| SKILL.md | 新增「与 PLAN.md 协同」章节 + 两种输出模式 |
| learns/ | 记录本次调整的踩坑 |

**无代码改动。**

## 与 base-skill 的兼容性

**原则**：始终检查 `docs/PLAN.md` 是否存在，不检查 plan-review-skill 是否安装。

| 情况 | 行为 |
|------|------|
| `docs/PLAN.md` 存在且格式正确 | 读取 milestone，在其下拆 sub-task |
| `docs/PLAN.md` 存在但格式混乱 | **忽略 PLAN.md，走原有 Step 1**（不报错，不卡住） |
| `docs/PLAN.md` 不存在 | 走原有 Step 1 澄清流程 |
| plan-review-skill 未安装 | 不影响，PLAN.md 可以是用户手动创建的 |

> 格式错误时 fallback 到 Step 1，不需要用户修复，不需要 PLAN skill。

## 判断规则

拆解前检查项目根目录是否存在 `docs/PLAN.md`：
- **存在** → 尝试读取 milestone
  - 成功 → 在 milestone 下拆 sub-task
  - **失败（格式混乱）→ 走原有 Step 1**
- **不存在** → 走原有 Step 1 澄清流程

## 实施顺序

Phase 1: plan-review-skill（先做）→ 写 `.target-trigger`
Phase 2: task-split-skill（第二）→ 读取 PLAN.md + 输出 milestone + subTask
Phase 3: target-skill（第三）→ 从 `.target-state.json` 接管追踪
