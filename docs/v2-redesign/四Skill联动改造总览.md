# 四 Skill 联动改造总览

> PLAN skill + task-split-skill + plan-review-skill + target-skill

---

## 1. 改造总览

### 1.1 四 Skill 职责分工

| Skill | 职责 | 输入 | 输出 |
|-------|------|------|------|
| **PLAN skill** | 生成标准计划 | 用户需求 | `docs/PLAN.md` |
| **plan-review-skill** | 评审计划 | `docs/PLAN.md` | `.target-trigger` |
| **task-split-skill** | 拆解任务 | `docs/PLAN.md`（如存在） | milestone + subTask |
| **target-skill** | 追踪执行 | milestone + subTask | 持续追踪 |

### 1.2 完整工作流

```
用户需求
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ PLAN skill                                                  │
│ 生成标准 PLAN.md                                             │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ plan-review-skill                                           │
│ 评审计划 → approved                                         │
│ 写 .target-trigger                                          │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ task-split-skill                                            │
│ 读取 PLAN.md → 在 milestone 下拆 sub-task                    │
│ 输出 milestone + subTask                                     │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ target-skill                                                │
│ 接收 milestone + subTask                                    │
│ 持续追踪 milestone / subTask 状态                            │
│ 抗偏移 + 歧义确认                                           │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
执行完成
```

---

## 2. 文件流转

```
docs/PLAN.md
    │ 由 PLAN skill 生成
    ▼
plan-review-skill 读取
    │ 评审通过后
    ▼
.target-trigger
    │ 触发 target-skill
    ▼
target-skill 检查
    │ 发现无 .target-state.json 且无 milestone
    ▼
task-split-skill 读取 PLAN.md
    │ 拆解完成
    ▼
.target-state.json（milestone + subTask）
    │ target-skill 读写
    ▼
target-skill 持续追踪
```

---

## 3. 状态字段说明

### 3.1 PLAN.md status

| 状态 | 说明 |
|------|------|
| `draft` | 草稿，未评审 |
| `pending_review` | 待评审 |
| `approved` | 已批准 |
| `rejected` | 已驳回 |
| `obsolete` | 已废弃 |

### 3.2 .target-trigger

```json
{
  "version": "1.0",
  "planFile": "docs/PLAN.md",
  "approvedAt": "{时间}",
  "approvedBy": "{用户}",
  "goal": "{项目愿景}"
}
```

### 3.3 .target-state.json

```json
{
  "goal": "{项目愿景}",
  "phase": "active",
  "source": "task-split",
  "createdAt": "{时间}",
  "lastUpdated": "{时间}",
  "milestones": [
    {
      "id": "M1",
      "title": "{标题}",
      "status": "active",
      "completedAt": null,
      "subTasks": [
        {
          "id": "M1-1",
          "title": "{标题}",
          "status": "pending",
          "completedAt": null
        }
      ]
    }
  ],
  "changeLog": []
}
```

---

## 4. 触发关系

### 4.1 触发链

```
用户说「制定计划」
    → PLAN skill

用户说「评审计划」
    → plan-review-skill

用户说「拆解任务」/「开始执行」
    → task-split-skill

用户说「追踪目标」
    → target-skill
```

### 4.2 自动触发

```
PLAN skill 生成 PLAN.md
    → 提示用户「可评审/可拆解」

plan-review-skill 批准
    → 自动写 .target-trigger

task-split-skill 拆解完成
    → 提示用户「可追踪」
```

---

## 5. 各 Skill 边界

### 5.1 边界定义

| 场景 | 负责方 |
|------|--------|
| 用户说「制定计划」 | PLAN skill |
| 用户说「评审计划」 | plan-review-skill |
| 用户说「拆解任务」 | task-split-skill |
| 用户说「追踪目标」 | target-skill |
| 用户说「制定计划并拆解」 | PLAN skill → task-split-skill（分两步） |

### 5.2 不互相替代

- PLAN skill 不评审（plan-review-skill 的职责）
- plan-review-skill 不生成（PLAN skill 的职责）
- task-split-skill 不追踪（target-skill 的职责）
- target-skill 不拆解（task-split-skill 的职责）

---

## 6. 兼容性设计

### 6.1 无 PLAN.md 时的降级

```
task-split-skill
    ↓
无 docs/PLAN.md
    ↓
走快速拆解模式（扁平任务列表）
    ↓
不卡住，不要求用户先创建 PLAN
```

### 6.2 无 .target-trigger 时的启动

```
target-skill
    ↓
无 .target-state.json
    ↓
检查 .target-trigger
    ├── 存在 → 从 PLAN.md 解析
    └── 不存在 → 询问用户「设定目标」或「拆解任务」
```

### 6.3 无其他 Skill 时的独立工作

```
PLAN skill：完全独立，不依赖其他 Skill
plan-review-skill：依赖 PLAN.md（可由用户手动创建）
task-split-skill：可独立工作（无 PLAN.md 时走快速拆解）
target-skill：可独立工作（用户手动设定目标）
```

---

## 7. 实施顺序

### Phase 1：PLAN skill（新建）

**目标**：建立公共计划生成能力

**产出**：
- `PLAN-skill/SKILL.md`
- `PLAN-skill/README.md`
- `PLAN-skill/learns/`

**验证**：
```bash
# 测试 PLAN skill 生成标准 PLAN.md
```

### Phase 2：plan-review-skill 改造（第二）

**目标**：移除生成计划的能力，专注评审

**改动**：
- SKILL.md：移除生成 SOP，新增前置检查
- learns/

**验证**：
```bash
# 测试评审标准 PLAN.md
```

### Phase 3：task-split-skill 改造（第三）

**目标**：读取 PLAN.md，输出 milestone + subTask

**改动**：
- SKILL.md：新增两种模式，新增读取 PLAN.md SOP
- learns/

**验证**：
```bash
# 测试有 PLAN.md 时的完整拆分
# 测试无 PLAN.md 时的快速拆解
```

### Phase 4：target-skill 改造（第四）

**目标**：接收 task-split-skill 的 milestone + subTask

**改动**：
- SKILL.md：新增三种启动方式，新增 milestone + subTask 状态管理
- learns/

**验证**：
```bash
# 测试从 task-split-skill 接管
# 测试手动设定目标
```

---

## 8. 设计原则

1. **各司其职** — 每个 Skill 有且只有一个核心职责
2. **最小化依赖** — Skill 可独立工作，不强制依赖其他 Skill
3. **用户确认后才执行** — 所有关键操作需要用户确认
4. **中间产物必须留存** — PLAN.md、.target-trigger、.target-state.json 都必须写入文件
5. **不替用户做决定** — 里程碑、验收标准等关键信息必须用户填
6. **LLM 不可靠的地方用确认机制** — 解析 Markdown 表格 → 复述 + 确认

---

## 9. 文件清单

```
PLAN-skill/
├── SKILL.md              # 新建
├── README.md             # 新建
└── learns/              # 新建

plan-review-skill/
├── SKILL.md              # 改造
├── README.md             # 更新（如需要）
└── learns/              # 新增

task-split-skill/
├── SKILL.md              # 改造
├── README.md             # 更新（如需要）
└── learns/              # 新增

target-skill/
├── SKILL.md              # 改造
├── README.md             # 更新（如需要）
└── learns/              # 新增
```

---

## 10. 风险与缓解

| 风险 | 缓解 |
|------|------|
| 四 Skill 同时改造，容易出错 | 按 Phase 顺序，每次只改一个 |
| 各 Skill 边界理解不一致 | 设计原则 + 边界定义章节 |
| 改造后数据格式不兼容 | 定义清晰的 JSON 格式 |
| 用户不按流程走 | 每个 Skill 可独立工作，降级设计 |
