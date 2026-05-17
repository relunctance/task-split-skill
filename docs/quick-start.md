# 四 Skill 联动 - 快速启动示例

> 这是一个完整对话示例，展示了四 Skill 联动的典型使用流程。

---

## 示例场景

**用户**：帮我做一个用户登录功能

---

## 完整对话流程

### 第一步：制定计划

**用户**：帮我做一个用户登录功能

**AI**（检测到 PLAN skill）：
> 请先制定计划。正在加载 PLAN skill...

**AI**（PLAN skill）：
> ## 🔍 项目上下文感知
>
> 这是一个新项目。请告诉我：
> 1. 主要技术栈是什么？（Python/FastAPI, Node/Express, Go, etc.）
> 2. 项目类型？（Web API, CLI 工具, 前端应用, 库/SDK...）

**用户**：FastAPI 后端项目

**AI**（PLAN skill）：
> ## 复述确认
>
> **项目类型**：FastAPI 后端 Web API
>
> 请确认是否正确。

**用户**：对的

**AI**（PLAN skill）：
> ## 澄清问题
>
> 请回答以下问题：
>
> **1. 最终交付物是什么？**
> > （用户输入）
>
> **2. 成功标准是什么？**
> > （用户输入）
>
> ...

**用户**：（回答了所有问题）

**AI**（PLAN skill）：
> ## ✅ PLAN.md 已生成
>
> **文件位置**：`docs/PLAN.md`
>
> ### 项目愿景
> {项目愿景}
>
> ### 里程碑（3 个）
> | ID | 里程碑 | 验收标准 |
> |----|--------|---------|
> | M1 | 数据库设计 | users 表创建完成 |
> | M2 | 登录 API | POST /api/login 返回 token |
> | M3 | Token 验证 | 中间件验证有效 |
>
> ### 下一步
> 1. **评审计划** — 触发 plan-review-skill
> 2. **开始拆解** — 触发 task-split-skill
> 3. **修改计划** — 调整内容

---

### 第二步：评审计划

**用户**：评审计划

**AI**（检测到 plan-review-skill）：
> 正在加载 plan-review-skill...

**AI**（plan-review-skill）：
> ## 🔍 正在评审 PLAN.md
>
> **检查清单**：
> - [ ] 项目愿景清晰具体
> - [ ] 每个里程碑有验收标准
> - [ ] 交付物与里程碑对应
> - [ ] 风险预判充分
>
> **分析结果**：
> - 愿景：✅ 清晰
> - 里程碑：✅ M1/M2/M3 验收标准明确
> - 风险：⚠️ 建议补充「Token 过期策略」
>
> ### 建议
> 在「风险预判」中添加一行：
> - 风险：Token 过期策略
> - 影响：中
> - 应对：固定 7 天，后续优化

**用户**：好的，补充一下

**AI**（plan-review-skill）：
> ✅ 风险已补充。PLAN.md 更新完成。

**用户**：确认评审通过

**AI**（plan-review-skill）：
> ## ✅ 评审通过
>
> **文件**：`.target-trigger` 已写入
>
> ### 下一步
> 1. **拆解任务** — 触发 task-split-skill
> 2. **修改计划** — 调整 PLAN.md 内容

---

### 第三步：拆解任务

**用户**：拆解任务

**AI**（检测到 task-split-skill）：
> 正在加载 task-split-skill...

**AI**（task-split-skill）：
> ## 🔍 项目上下文感知
>
> 检测到项目为 FastAPI 后端
>
> **技术栈**：FastAPI + SQLAlchemy + Pydantic
> **项目结构**：app/, models/, schemas/, api/
>
> **确认**：这是 FastAPI 后端 Web API 项目吗？

**用户**：是的

**AI**（task-split-skill）：
> ## 📋 我对 PLAN.md 的理解
>
> **目标**：实现用户登录功能
>
> **里程碑**：
> - M1：数据库设计 — users 表
> - M2：登录 API — POST /api/login
> - M3：Token 验证 — JWT 中间件
>
> **交付物**：
> - users 表 + migration
> - /api/login 接口
> - auth 中间件
>
> 请确认以上理解是否正确。

**用户**：对的

**AI**（task-split-skill）：
> 正在拆解任务...
>
> ## ✅ 拆解完成
>
> **文件**：`.task-split.json` 已写入
>
> ### Milestone + Sub-task
>
> **M1：数据库设计**
> | ID | sub-task | 验收标准 | 优先级 |
> |----|---------|---------|--------|
> | M1-1 | 创建 users 表 migration | users 表包含 id/username/password_hash | P0 |
> | M1-2 | 创建 User 模型 | SQLAlchemy 模型可 CRUD | P0 |
>
> **M2：登录 API**
> | ID | sub-task | 验收标准 | 优先级 |
> |----|---------|---------|--------|
> | M2-1 | 实现 /api/login | 成功返回 200+token，失败 401 | P0 |
> | M2-2 | 密码哈希验证 | bcrypt 验证 | P0 |
> | M2-3 | JWT Token 生成 | 有效期 7 天 | P0 |
>
> ### 下一步
> 1. **开始执行** — 触发 target-skill 追踪
> 2. **修改拆解** — 调整任务
> 3. **添加任务** — 在 milestone 下添加

---

### 第四步：开始执行

**用户**：开始执行

**AI**（检测到 target-skill）：
> 正在加载 target-skill...

**AI**（target-skill）：
> ## 🎯 检测到进行中的目标
>
> **大目标**：实现用户登录功能
> **状态**：🟡 进行中
> **来源**：task-split-skill
> **子目标**：9 个任务
>
> ### 当前任务
>
> **M1：数据库设计**（3 个 sub-task）
> | ID | 任务 | 状态 |
> |----|------|------|
> | M1-1 | 创建 users 表 migration | ⬜ 待开始 |
> | M1-2 | 创建 User 模型 | ⬜ 待开始 |
> | M1-3 | 编写数据库初始化脚本 | ⬜ 待开始 |
>
> ### 下一步
> 1. **开始 M1-1** — 推进第一个任务
> 2. **查看全部** — 显示所有任务
> 3. **调整目标** — 修改目标或任务

---

## 快速参考

### 触发词

| 阶段 | 触发词 | Skill |
|------|--------|-------|
| 制定计划 | `制定计划` / `写 PLAN` | PLAN skill |
| 评审计划 | `评审计划` / `review PLAN` | plan-review-skill |
| 拆解任务 | `拆解任务` / `task split` | task-split-skill |
| 开始执行 | `开始执行` / `追踪目标` | target-skill |

### 关键文件

| 文件 | 创建者 | 说明 |
|------|--------|------|
| `docs/PLAN.md` | PLAN skill | 项目计划 |
| `.target-trigger` | plan-review-skill | 评审通过标记 |
| `.task-split.json` | task-split-skill | 任务拆解结果 |
| `.target-state.json` | target-skill | 追踪状态 |

### 三条流程路径

**路径1（推荐）**：PLAN → 评审 → 拆解 → 执行
**路径2（快速）**：PLAN → 拆解 → 执行（跳过评审）
**路径3（直接）**：直接拆解 → 手动设定目标（无 PLAN）
