# 四 Skill 联动方案 - 最终确认版

> 确认时间：2026-05-17
> 核心原则：复述 + 人工确认 | 各司其职 | 中间产物留存 | 版本契约 | 可独立工作

---

## 一、架构概览

```
用户需求
    │
    ▼
┌─────────────────────────────────────────┐
│ PLAN skill（新建）                        │
│ 生成标准 PLAN.md                          │
│ 复述 + 用户确认后才写入                   │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ plan-review-skill（改造）                 │
│ 评审 PLAN.md → approved                  │
│ 写 .target-trigger                       │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ task-split-skill（改造）                  │
│ 读取 PLAN.md → milestone + subTask       │
│ 复述 + 用户确认                          │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ target-skill（改造）                      │
│ 接收 milestone + subTask                  │
│ 持续追踪 + 抗偏移                         │
└─────────────────────────────────────────┘
    │
    ▼
执行完成
```

---

## 二、核心原则（5条）

| 原则 | 说明 |
|------|------|
| **复述 + 确认** | LLM 理解后必须用户确认，才视为有效输入 |
| **各司其职** | 每个 Skill 有且只有一个核心职责 |
| **中间产物留存** | PLAN.md、.target-trigger、.target-state.json 必须写入文件 |
| **版本契约** | docs/schemas.md 定义所有格式版本，版本不匹配时提示用户 |
| **可独立工作** | 无其他 Skill 时可降级，不卡住 |

---

## 三、文件流转

```
docs/PLAN.md              ← PLAN skill 生成
    │
    ▼
plan-review-skill 评审通过
    │
    ▼
.target-trigger          ← plan-review-skill 写入
    │
    ▼
task-split-skill 读取 PLAN.md，拆解 subTask
    │
    ▼
.target-state.json       ← task-split-skill 生成 milestone + subTask
    │
    ▼
target-skill 追踪
```

---

## 四、各 Skill 职责

| Skill | 职责 | 输入 | 输出 |
|-------|------|------|------|
| **PLAN skill** | 生成标准计划 | 用户需求 | `docs/PLAN.md` |
| **plan-review-skill** | 评审计划 | `docs/PLAN.md` | `.target-trigger` |
| **task-split-skill** | 拆解任务 | `docs/PLAN.md`（如存在） | milestone + subTask |
| **target-skill** | 追踪执行 | milestone + subTask | 持续追踪 |

---

## 五、多版本处理

| 情况 | 处理方式 |
|------|---------|
| 只有 `PLAN.md` | 直接编辑（不另存） |
| `PLAN.md` + 历史版本 | 询问用户 |
| 多个历史版本，无 `PLAN.md` | 找最新版本，询问是否升为主版本 |
| 版本不匹配 | 提示用户，不卡住 |

**文件命名约定：**
```
docs/PLAN.md              # 始终是「当前主版本」
docs/PLAN-YYYY-MM-DD.md  # 历史版本存档
docs/PLAN-v1.0.md        # 大版本存档
```

---

## 六、多 Skill 联动机制

### 6.1 版本契约文件

**`docs/schemas.md`** — 所有 Skill 输出格式的版本定义

```markdown
# Schema 版本契约

## PLAN.md
- 版本：1.0
- 位置：`docs/PLAN.md`
- 消费者：plan-review-skill, task-split-skill

## .target-trigger
- 版本：1.0
- 位置：项目根目录
- 消费者：target-skill

## .target-state.json
- 版本：1.0
- 位置：项目根目录
- 消费者：target-skill

---

## 变更记录

| 日期 | Schema | 变更内容 | 影响范围 |
|------|--------|---------|---------|
| 2026-05-17 | .target-state.json | 新增 milestone + subTask 结构 | target-skill |
```

### 6.2 版本检查 SOP

当 Skill 读取其他 Skill 的输出时：

1. 读取输出文件的版本字段
2. 对比 `docs/schemas.md` 中的版本
3. 如果版本不匹配 → 提示用户，不卡住

### 6.3 更新 Skill 时的 SOP

```
1. 评估影响范围
   - 改了输出格式？→ 检查消费者
   - 改了输入格式？→ 检查提供者

2. 更新 docs/schemas.md
   - 追加变更记录
   - 更新版本号

3. 通知用户
   - 「此更新影响以下 Skill：xxx」

4. 在 skill 的 learns/ 记录
   - 本次变更对其他 skill 的影响
```

### 6.4 各文件版本字段

| 文件 | 版本字段 | 位置 |
|------|---------|------|
| `docs/PLAN.md` | `version` | frontmatter |
| `.target-trigger` | `version` | JSON 顶层 |
| `.target-state.json` | `schemaVersion` | JSON 顶层 |

---

## 七、base-skill 标配

```
base-skill 标配 skill 组合：
├── task-split-skill（任务拆解）
├── target-skill（目标追踪）
├── plan-review-skill（规划评审）
└── PLAN skill（计划生成）
```

---

## 八、实施顺序

| Phase | Skill | 任务 |
|-------|-------|------|
| **Phase 1** | PLAN skill | ✅ 新建完成 |
| **Phase 2** | plan-review-skill | 改造 — 移除生成，专注评审 |
| **Phase 3** | task-split-skill | 改造 — 读取 PLAN.md，输出 milestone + subTask |
| **Phase 4** | target-skill | 改造 — 接收 milestone + subTask |

---

## 九、关键决策记录

### 决策 1：PLAN skill 独立

**问题**：task-split-skill 内置生成计划的能力，与 plan-review-skill 重复。

**决策**：PLAN skill 作为独立 Skill，供 task-split-skill 和 plan-review-skill 共用。

### 决策 2：复述 + 确认原则

**问题**：LLM 解析 Markdown 表格不可靠。

**决策**：所有关键信息必须经过「复述 + 用户确认」流程，LLM 自己理解的不算数。

### 决策 3：多版本处理

**问题**：用户可能创建多个 PLAN 文件。

**决策**：约定主版本 + 历史版本，智能查找最新版本。

### 决策 4：版本契约

**问题**：一个 Skill 改了格式，其他 Skill 可能不知道。

**决策**：docs/schemas.md 定义版本契约，版本不匹配时提示用户。
