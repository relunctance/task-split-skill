# target-skill v2 改造文档

> 改造后的 target-skill 接收来自 task-split-skill 的 milestone + subTask 结构，进行追踪。

---

## 1. 改造原则

### 1.1 改造后的职责

**只负责追踪，不负责拆解。**

| | 改造前 | 改造后 |
|--|--------|--------|
| **职责** | 拆解 + 追踪 | 只追踪 |
| **拆解** | 自己从 PLAN.md 解析 | 交给 task-split-skill |
| **数据来源** | 解析 PLAN.md 或手动设定 | 接收 task-split-skill 的输出 |

### 1.2 改造后的工作流

```
用户说「追踪目标」/「开始执行」
    ↓
检查 .target-state.json 是否存在
    ├── 存在 → 读取状态，继续追踪
    └── 不存在 → 检查 .target-trigger
                ├── .target-trigger 存在 → 从 PLAN.md 解析 milestone
                └── .target-trigger 不存在 → 提示用户先拆解
```

---

## 2. 触发条件

### 2.1 触发词

| 触发词 | 说明 |
|--------|------|
| `追踪目标` / `追踪执行` | 核心触发 |
| `开始执行` / `启动追踪` | 启动追踪 |
| `当前进度` / `执行进度` | 查看进度 |
| `目标是什么` / `当前目标` | 查看目标 |
| `继续追踪` | 恢复追踪 |

### 2.2 不触发

| 不触发 | 原因 |
|--------|------|
| `制定计划` | → PLAN skill |
| `拆解任务` | → task-split-skill |
| `评审计划` | → plan-review-skill |

---

## 3. 三种启动方式

### 3.1 从 task-split-skill 接管（推荐）

```
task-split-skill 拆解完成
    ↓
用户说「开始执行」/「追踪」
    ↓
target-skill 接收 milestone + subTask 结构
    ↓
写入 .target-state.json
    ↓
开始追踪
```

### 3.2 从 .target-trigger 接管

```
plan-review-skill 批准后写 .target-trigger
    ↓
用户说「追踪目标」
    ↓
target-skill 检测到 .target-trigger
    ↓
读取 PLAN.md（LLM 解析）
    ↓
发现有 milestone 无 subTask → 提示用户「请先用 task-split 拆解」
```

### 3.3 手动设定目标

```
用户说「设定目标」
    ↓
按现有 SOP 设定目标
    ↓
写入 .target-state.json
    ↓
开始追踪
```

---

## 4. 状态管理

### 4.1 .target-state.json 格式

```json
{
  "goal": "项目愿景",
  "phase": "active",
  "source": "task-split",
  "createdAt": "YYYY-MM-DDTHH:mm:ss+08:00",
  "lastUpdated": "YYYY-MM-DDTHH:mm:ss+08:00",
  "milestones": [
    {
      "id": "M1",
      "title": "里程碑标题",
      "status": "active",
      "completedAt": null,
      "subTasks": [
        {
          "id": "M1-1",
          "title": "子任务标题",
          "status": "done",
          "completedAt": "YYYY-MM-DDTHH:mm:ss+08:00"
        },
        {
          "id": "M1-2",
          "title": "子任务标题",
          "status": "pending"
        }
      ]
    },
    {
      "id": "M2",
      "title": "里程碑2标题",
      "status": "pending",
      "completedAt": null,
      "subTasks": []
    }
  ],
  "changeLog": [
    {
      "time": "YYYY-MM-DDTHH:mm:ss+08:00",
      "action": "接管 milestone + subTask",
      "detail": "来源: task-split-skill"
    }
  ]
}
```

### 4.2 状态字段说明

| 字段 | 说明 |
|------|------|
| `source` | `"task-split"` 或 `"manual"` |
| `milestones[].status` | `pending` / `active` / `done` |
| `subTasks[].status` | `pending` / `active` / `blocked` / `done` |

### 4.3 状态转换规则

```
milestone.status:
  pending → active（第一个 subTask 开始）
  active → done（所有 subTask done）
  active → blocked（所有 subTask blocked）

subTask.status:
  pending → active（开始执行）
  active → done（完成）
  active → blocked（被依赖阻塞）
  blocked → active（依赖完成）
```

---

## 5. 关键改动说明

### 5.1 删除的内容

| 删除内容 | 原因 |
|---------|------|
| 从 PLAN.md 自己解析 milestone | 交给 task-split-skill |
| 自己拆解 sub-task | 交给 task-split-skill |
| 与 plan-review-skill 的复杂联动 | 简化为只读 .target-trigger |

### 5.2 新增的内容

| 新增内容 | 说明 |
|---------|------|
| 接收 task-split-skill 输出的结构 | milestone + subTask |
| 从 .target-trigger 启动时的判断 | 如果无 subTask，提示用户先拆解 |
| source 字段 | 标识数据来源 |

### 5.3 保留的内容

| 保留内容 | 说明 |
|---------|------|
| 目标追踪 + 抗偏移 | 核心功能 |
| 健康度评分 | 追踪质量 |
| 歧义确认 | 决策权归用户 |
| 手动设定目标 | 向后兼容 |

---

## 6. 与其他 Skill 的关系

### 6.1 与 task-split-skill 的关系

```
task-split-skill 拆解完成
    ↓
输出 milestone + subTask
    ↓
target-skill 接收
    ↓
写入 .target-state.json
    ↓
开始追踪
```

### 6.2 与 plan-review-skill 的关系

```
plan-review-skill 批准时写 .target-trigger
    ↓
target-skill 读取 .target-trigger
    ↓
发现 milestone 但无 subTask
    ↓
提示用户「请先用 task-split 拆解」
```

### 6.3 与 PLAN skill 的关系

```
PLAN skill 生成 docs/PLAN.md
    ↓
plan-review-skill 评审
    ↓
task-split-skill 拆解
    ↓
target-skill 追踪
```

---

## 7. SKILL.md 改动清单

### 7.1 新增章节

| 章节 | 行数 |
|------|------|
| 接收 task-split-skill 输出的 SOP | ~40 行 |
| 三种启动方式 | ~30 行 |
| milestone + subTask 状态管理 | ~30 行 |

### 7.2 删除内容

| 删除内容 | 行数 |
|---------|------|
| 从 PLAN.md 自己解析 milestone | ~40 行 |
| 与 plan-review-skill 的复杂联动 | ~30 行 |

### 7.3 改动统计

| 类型 | 行数 |
|------|------|
| 新增 | ~100 行 |
| 删除 | ~70 行 |
| 修改 | ~30 行 |

---

## 8. 改动后的 SKILL.md 结构

```
SKILL.md
├── (保留) frontmatter
├── (保留) Overview
├── (新增) 三种启动方式
│   ├── 从 task-split-skill 接管（推荐）
│   ├── 从 .target-trigger 接管
│   └── 手动设定目标
├── (修改) 接收 milestone + subTask 的 SOP
├── (保留) 目标追踪 + 抗偏移
├── (保留) 健康度评分
├── (保留) 歧义确认
├── (保留) 每次回复前的对齐检查
├── (新增) milestone + subTask 状态管理
├── (保留) 目标达成
├── (保留) 目标放弃
├── (修改) 与 task-split-skill 的联动（改为接收）
├── (修改) 与 plan-review-skill 的联动（简化）
└── (保留) 安装
```

---

## 9. learns 记录

本次改造的踩坑点：

| 踩坑 | 记录 |
|------|------|
| task-split-skill 输出格式不标准 | 定义清晰的 milestone + subTask JSON 格式 |
| .target-trigger 有 milestone 无 subTask | 提示用户先拆解，不卡住 |
| source 字段丢失 | 追踪数据来源，便于调试 |
