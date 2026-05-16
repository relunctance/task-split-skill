# 四 Skill 联动 - 联调测试报告

> 测试时间：2026-05-17
> 测试目的：验证四 Skill 联动流程可落地使用
> 测试结果：✅ 3 个场景全部通过

---

## 一、测试场景

| 场景 | 描述 | 对应流程 |
|------|------|---------|
| 场景1 | 完整流程（有PLAN → 评审 → 拆解 → 执行） | 路径1（推荐） |
| 场景2 | 快速流程（有PLAN → 直接拆解，跳过评审） | 路径2 |
| 场景3 | 无PLAN，直接拆解（快速模式） | 路径3 |

---

## 二、场景1：完整流程

### 2.1 测试数据

**项目目标**：实现用户登录功能，包含用户名密码验证、Token 发放、会话管理

**测试目录**：`/tmp/scenario1-test/`

### 2.2 流程执行

```
用户: 制定计划
  → PLAN skill: 生成 docs/PLAN.md
  ✅ 生成的 PLAN.md 包含：
     - frontmatter (status, version, author, created, updated)
     - 项目愿景
     - 需求约束（MVP / 可砍掉 / 技术约束）
     - 里程碑表格（M1/M2/M3，完整验收标准）
     - 交付物表格
     - 风险预判

用户: 评审计划
  → plan-review-skill: 评审 docs/PLAN.md
  ✅ 评审检查清单覆盖：
     - 项目愿景（清晰具体）
     - 里程碑（验收标准明确）
     - 交付物（与里程碑对应）
     - 风险预判（充分）

用户: 拆解任务
  → task-split-skill: 读取 docs/PLAN.md，写入 .task-split.json
  ✅ .task-split.json 包含：
     - 3 个 milestone
     - 9 个 subTask（M1-1~M1-3, M2-1~M2-4, M3-1~M3-2）
     - 每个 subTask 有 id/title/status/priority/acceptanceCriteria

用户: 开始执行
  → target-skill: 读取 .task-split.json，转换为 .target-state.json
  ✅ .target-state.json 包含：
     - goal（项目愿景）
     - phase: active
     - source: task-split
     - 3 个 milestone（status: pending）
     - 9 个 subTask（status: pending）
     - changeLog
```

### 2.3 验证结果

| 验证项 | 结果 |
|--------|------|
| PLAN.md 格式完整（frontmatter + 5个章节） | ✅ |
| milestone 表格格式正确（ID/里程碑/验收标准/状态/截止日期） | ✅ |
| .task-split.json 有效 JSON | ✅ |
| subTask ID 格式正确（M1-1, M1-2...） | ✅ |
| .task-split.json → .target-state.json 转换数据完整 | ✅ |
| 9 个 subTask 全部保留 | ✅ |

---

## 三、场景2：快速流程（跳过评审）

### 3.1 测试数据

**项目目标**：搭建 CI/CD 流水线，自动化构建、测试、部署

**测试目录**：`/tmp/scenario2-test/`

### 3.2 流程执行

```
用户: 制定计划
  → PLAN skill: 生成 docs/PLAN.md
  ✅ 生成的 PLAN.md 包含完整结构

用户: 拆解任务（跳过评审）
  → task-split-skill 检测到 docs/PLAN.md 存在
  ✅ 进入「完整拆分」模式
  ✅ 直接读取 docs/PLAN.md，不依赖 .target-trigger

用户: 开始执行
  → target-skill: 从 .task-split.json 接管
  ✅ 与场景1相同流程
```

### 3.3 验证结果

| 验证项 | 结果 |
|--------|------|
| task-split-skill 正确识别「完整拆分」模式 | ✅ |
| task-split-skill 直接读取 docs/PLAN.md | ✅ |
| 不需要 .target-trigger 即可拆解 | ✅ |
| 跳过评审不影响 task-split-skill 执行 | ✅ |

---

## 四、场景3：无PLAN（快速模式）

### 4.1 测试数据

**项目目标**：用户随机需求，无 PLAN.md

**测试目录**：`/tmp/scenario3-test/`

### 4.2 流程执行

```
用户: 拆解任务（无 PLAN.md）
  → task-split-skill 检测到 docs/PLAN.md 不存在
  ✅ 进入「快速拆解」模式
  ✅ 执行澄清问题流程（4个必问）

用户: 设定目标
  → target-skill: 手动设定目标
  ✅ 使用「方式3：手动设定目标」
  ✅ 扁平任务列表，无 milestone 结构
```

### 4.3 验证结果

| 验证项 | 结果 |
|--------|------|
| task-split-skill 正确识别「快速拆解」模式 | ✅ |
| 快速拆解输出扁平任务列表 | ✅ |
| target-skill 可用手动设定接收 | ✅ |
| 快速模式不经过 .task-split.json | ✅ |

---

## 五、三条流程路径

### 路径1（推荐）：完整流程

```
用户: 制定计划
  → PLAN skill: 生成 docs/PLAN.md
用户: 评审计划
  → plan-review-skill: 评审 + 写 .target-trigger
用户: 拆解任务
  → task-split-skill: 读取 PLAN.md + 写 .task-split.json
用户: 开始执行
  → target-skill: 读取 .task-split.json + 写 .target-state.json
```

### 路径2（快速）：跳过评审

```
用户: 制定计划
  → PLAN skill: 生成 docs/PLAN.md
用户: 拆解任务
  → task-split-skill: 读取 PLAN.md + 写 .task-split.json
用户: 开始执行
  → target-skill: 读取 .task-split.json + 写 .target-state.json
```

### 路径3（直接）：无PLAN

```
用户: 拆解任务（无 PLAN.md）
  → task-split-skill: 快速拆解模式，输出扁平列表
用户: 设定目标
  → target-skill: 手动设定目标
```

---

## 六、发现并修复的问题

| 问题 | 发现场景 | 修复方案 | 修复版本 |
|------|---------|---------|---------|
| task-split-skill 输出 milestone + subTask 但不持久化 | 联调检查 | 新增 `.task-split.json` 文件写入 | v2.1 |
| target-skill 无法获取 task-split 的输出数据 | 联调检查 | 新增方式1：从 `.task-split.json` 接管 | v2.1 |
| 缺少两个文件格式的转换规则 | 联调检查 | 新增 `.task-split.json → .target-state.json` 转换规则表 | v2.1 |

---

## 七、关键文件格式

### 7.1 docs/PLAN.md（PLAN skill 输出）

```markdown
---
status: draft
version: 1.0
author: {author}
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
---

# 项目愿景

{项目目标描述}

---

# 需求约束

## MVP（必须有的）
- {功能1}
- {功能2}

## 技术约束
- 技术栈：{技术栈}
- 运行环境：{运行环境}

---

# 里程碑

| ID | 里程碑 | 验收标准 | 状态 | 截止日期 |
|----|--------|---------|------|---------|
| M1 | {标题} | {验收标准} | pending | {YYYY-MM-DD} |

---

# 交付物

| 交付物 | 负责人 | 截止日期 | 关联里程碑 |
|--------|--------|---------|-----------|
| {名称} | {负责人} | {YYYY-MM-DD} | M1 |

---

# 风险预判

| 风险 | 影响 | 概率 | 应对 |
|------|------|------|------|
| {风险描述} | 高/中/低 | 高/中/低 | {应对措施} |
```

### 7.2 .task-split.json（task-split-skill 输出）

```json
{
  "version": "1.0",
  "goal": "{项目目标}",
  "source": "docs/PLAN.md",
  "createdAt": "{YYYY-MM-DDTHH:mm:ss+08:00}",
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

### 7.3 .target-state.json（target-skill 使用）

```json
{
  "goal": "{项目目标}",
  "phase": "active",
  "source": "task-split",
  "createdAt": "{YYYY-MM-DDTHH:mm:ss+08:00}",
  "lastUpdated": "{YYYY-MM-DDTHH:mm:ss+08:00}",
  "milestones": [
    {
      "id": "M1",
      "title": "{标题}",
      "status": "pending",
      "completedAt": null,
      "subTasks": [
        {
          "id": "M1-1",
          "title": "{任务}",
          "status": "pending",
          "completedAt": null
        }
      ]
    }
  ],
  "changeLog": []
}
```

### 7.4 .target-trigger（plan-review-skill 输出）

```json
{
  "version": "1.0",
  "planFile": "docs/PLAN.md",
  "approvedAt": "{YYYY-MM-DDTHH:mm:ss+08:00}",
  "approvedBy": "{user_name}",
  "goal": "{项目愿景}"
}
```

---

## 八、版本记录

| 日期 | Skill | 版本 | 变更 |
|------|-------|------|------|
| 2026-05-17 | plan-skill | 1.0 | 新建 |
| 2026-05-17 | plan-review-skill | 3.0 | v3改造——移除PLAN生成，专注评审 |
| 2026-05-17 | task-split-skill | 2.1 | v2.1——添加.task-split.json持久化 |
| 2026-05-17 | target-skill | 2.1 | v2.1——支持从.task-split.json接管 |
| 2026-05-17 | gql-skills | - | 更新四Skill版本记录 |

---

## 九、测试环境

- OS: Ubuntu (WSL)
- Python: 3.11+
- 测试目录: `/tmp/scenario*-test/`
- 联调时间: 2026-05-17

---

## 十、结论

**✅ 四 Skill 联动流程可落地使用**

- 场景1（完整流程）：✅ 通过
- 场景2（快速流程）：✅ 通过
- 场景3（无PLAN）：✅ 通过

**关键数据流打通**：
- PLAN.md → task-split.json → target-state.json 转换无误
- 三个流程路径均能正确执行
- 各 Skill 触发词无冲突
- 文件格式兼容
