# plan-review-skill v2 改造文档

> 改造后的 plan-review-skill 只负责评审，不负责生成计划。

---

## 1. 改造原则

### 1.1 改造后的职责

**只负责评审，不负责生成计划。**

| | 改造前 | 改造后 |
|--|--------|--------|
| **职责** | 生成计划 + 评审计划 | 只评审计划 |
| **计划生成** | 内置 | 交给 PLAN skill |
| **与 PLAN.md 关系** | 假设已存在 | 假设已由 PLAN skill 生成 |

### 1.2 改造后的工作流

```
用户说「评审计划」
    ↓
检查 docs/PLAN.md 是否存在
    ↓
不存在 → 提示用户「请先用 PLAN skill 生成计划」
    ↓
存在 → 执行评审流程
    ↓
评审通过 → 写 .target-trigger
评审驳回 → 更新 status → draft
```

---

## 2. 触发条件

### 2.1 触发词

| 触发词 | 说明 |
|--------|------|
| `评审计划` / `review PLAN` / `评审 PLAN` | 核心触发 |
| `批准 PLAN` / `approve PLAN` | 批准操作 |
| `驳回 PLAN` / `reject PLAN` | 驳回操作 |
| `PLAN diff` / `变更分析` | diff 操作 |

### 2.2 不触发

| 不触发 | 原因 |
|--------|------|
| `制定计划` / `写 PLAN` | → PLAN skill |
| `拆解任务` / `task split` | → task-split-skill |
| `追踪目标` | → target-skill |

---

## 3. 前置检查

### 3.1 检查 PLAN.md 是否存在

```markdown
## ⚠️ 未找到 PLAN.md

请先使用 PLAN skill 生成计划：
> 「制定计划」/「写 PLAN」/「规划一下」
```

### 3.2 校验 PLAN.md 格式

调用 PLAN skill 的格式校验：

```markdown
## 格式校验

检查 docs/PLAN.md 格式：
├── 通过 → 进入评审流程
└── 不通过 → 提示用户「PLAN.md 格式不正确，请修正后再评审」
```

---

## 4. 评审流程

### 4.1 完整评审流程

```
Step 1: 检查 PLAN.md 存在性和格式
Step 2: 读取 PLAN.md 内容
Step 3: 执行评审检查清单
Step 4: 输出评审结论
        ├── 批准 → 更新 status → approved，写 .target-trigger
        └── 驳回 → 更新 status → draft，输出驳回原因
```

### 4.2 评审检查清单

```markdown
## 评审检查清单

请逐项检查：

### 1. 项目愿景
- [ ] 目标是否清晰可衡量？
- [ ] 是否有明确的成功标准？

### 2. 需求约束
- [ ] MVP 范围是否明确？
- [ ] 技术约束是否可行？
- [ ] 是否有遗漏的约束？

### 3. 里程碑
- [ ] 每个里程碑是否有明确的验收标准？
- [ ] 里程碑之间是否有合理的依赖关系？
- [ ] 里程碑数量是否适中（不宜过多/过少）？

### 4. 交付物
- [ ] 交付物是否与里程碑对应？
- [ ] 负责人是否明确？
- [ ] 截止日期是否合理？

### 5. 风险预判
- [ ] 风险识别是否充分？
- [ ] 应对措施是否可行？
```

---

## 5. 批准流程

### 5.1 批准操作

```markdown
## ✅ 评审通过

**PLAN.md 状态**：approved
**评审时间**：{YYYY-MM-DD HH:mm}

### 评审结论

| 检查项 | 结果 |
|--------|------|
| 项目愿景 | ✅ 通过 |
| 需求约束 | ✅ 通过 |
| 里程碑 | ✅ 通过 |
| 交付物 | ✅ 通过 |
| 风险预判 | ✅ 通过 |

### 下一步

1. **开始拆解** — 触发 task-split-skill
2. **追踪执行** — 触发 target-skill
3. **修改计划** — 如需调整，修改后重新评审
```

### 5.2 批准时的状态更新

```
1. 更新 PLAN.md frontmatter：status: approved
2. 生成评审记录：docs/reviews/PLAN-review-YYYY-MM-DD-approved.md
3. 写 .target-trigger（触发 target-skill）
4. 提示用户下一步选项
```

### 5.3 .target-trigger 格式

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

## 6. 驳回流程

### 6.1 驳回操作

```markdown
## ❌ 评审驳回

**PLAN.md 状态**：draft（已更新）
**驳回时间**：{YYYY-MM-DD HH:mm}

### 驳回原因

{具体说明哪些问题需要修订}

### 需要修订的项

| 检查项 | 问题 |
|--------|------|
| 项目愿景 | {问题描述} |
| 里程碑 | {问题描述} |
| ... | ... |
```

### 6.2 驳回时的状态更新

```
1. 更新 PLAN.md frontmatter：status: draft
2. 生成评审记录：docs/reviews/PLAN-review-YYYY-MM-DD-rejected.md
3. 提示用户修订后重新提交评审
```

---

## 7. 关键改动说明

### 7.1 删除的内容

| 删除内容 | 原因 |
|---------|------|
| 生成 PLAN.md 的 SOP | 交给 PLAN skill |
| 澄清问题流程 | PLAN skill 的职责 |
| 创建 docs/PLAN.md 目录的逻辑 | 假设 PLAN.md 已存在 |

### 7.2 新增的内容

| 新增内容 | 说明 |
|---------|------|
| 前置检查（PLAN.md 存在性和格式） | 确保评审前有计划可评 |
| 提示用户使用 PLAN skill | 无 PLAN.md 时的引导 |

### 7.3 保留的内容

| 保留内容 | 说明 |
|---------|------|
| 状态机 | draft → pending_review → approved/rejected |
| 评审检查清单 | 核心评审逻辑 |
| 评审记录生成 | 留存评审历史 |
| .target-trigger 写入 | 触发 target-skill |

---

## 8. 与其他 Skill 的关系

### 8.1 与 PLAN skill 的关系

```
PLAN skill 生成 docs/PLAN.md
          ↓
plan-review-skill 读取 docs/PLAN.md
          ↓
评审
```

### 8.2 与 task-split-skill 的关系

```
plan-review-skill 批准 PLAN.md
          ↓
task-split-skill 读取 PLAN.md
          ↓
拆解任务
```

### 8.3 与 target-skill 的关系

```
plan-review-skill 批准时写 .target-trigger
          ↓
target-skill 读取 .target-trigger
          ↓
接管追踪
```

---

## 9. SKILL.md 改动清单

### 9.1 新增章节

| 章节 | 行数 |
|------|------|
| 前置检查（PLAN.md 存在性和格式） | ~20 行 |
| 提示用户使用 PLAN skill（无 PLAN.md 时） | ~10 行 |

### 9.2 删除内容

| 删除内容 | 行数 |
|---------|------|
| 生成 PLAN.md 的 SOP | ~40 行 |
| 澄清问题流程 | ~20 行 |

### 9.3 改动统计

| 类型 | 行数 |
|------|------|
| 新增 | ~30 行 |
| 删除 | ~60 行 |
| 修改 | ~20 行 |

---

## 10. 改动后的 SKILL.md 结构

```
SKILL.md
├── (保留) frontmatter
├── (保留) Overview
├── (保留) 状态机
├── (新增) 前置检查
│   ├── 检查 PLAN.md 是否存在
│   └── 校验格式
├── (新增) 无 PLAN.md 时的引导
├── (修改) 完整评审流程
│   ├── Step 1: 前置检查
│   ├── Step 2: 读取 PLAN.md
│   ├── Step 3: 执行评审检查清单
│   └── Step 4: 输出评审结论
├── (保留) 批准流程
├── (保留) 驳回流程
├── (保留) 评审检查清单
├── (保留) 评审记录格式
├── (保留) 与 PLAN skill 的关系
├── (保留) 与 task-split-skill 的联动
├── (保留) 与 target-skill 的联动
└── (保留) 安装
```

---

## 11. learns 记录

本次改造的踩坑点：

| 踩坑 | 记录 |
|------|------|
| 假设 PLAN.md 已存在但实际不存在 | 增加前置检查，无 PLAN.md 时提示用户 |
| 评审时 PLAN.md 格式错误 | 调用 PLAN skill 的格式校验 |
