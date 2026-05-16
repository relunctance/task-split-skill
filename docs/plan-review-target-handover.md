# plan-review-skill × task-split-skill × target-skill 三 Skill 联动设计方案

> 核心原则：代码最少化。plan-review 评审 → task-split 拆解 → target-skill 追踪，三者各司其职。

---

## 一、现状评估

### 1.1 plan-review-skill 产出格式

**PLAN.md frontmatter（结构化数据）：**
```yaml
---
status: draft
version: 1.0
author: 张三
last_updated: 2026-05-17
---
```

**PLAN.md 章节（半结构化）：**
```markdown
# 项目愿景
构建用户认证系统

# 需求约束
- MVP：登录、注册、登出
- 技术栈：FastAPI + PostgreSQL

# 里程碑
| ID | 里程碑 | 验收标准 | 状态 |
|----|--------|---------|------|
| M1 | 数据库设计 | schema 已评审 | pending |
| M2 | API 实现 | 单元测试通过 | pending |

# 交付物
| 交付物 | 负责人 | 截止日期 |
|--------|--------|---------|
| API 接口文档 | 张三 | 2026-05-20 |
| 测试报告 | 李四 | 2026-05-22 |

# 风险预判
| 风险 | 影响 | 概率 | 应对 |
|------|------|------|------|
| 数据库连接池配置复杂 | 高 | 中 | 使用连接池库 |
```

### 1.2 评估：能否支撑复杂研发需求

**✅ 能支撑的理由：**
- 里程碑已有 ID、标题、验收标准、状态
- 交付物已有名称、负责人、截止日期
- 风险预判已有应对方案

**⚠️ 需要增强的点：**
- 里程碑状态只有 `pending`，没有 `active/done/blocked`
- 没有 sub-task（task-split-skill 产出分散，没有统一追踪）
- 没有阻塞管理（blocker）
- 没有进度可见性（用户在执行中看不到当前状态）

**结论：PLAN.md 格式够用，不需要改格式。target-skill 增强后可以直接读取现有格式。**

---

## 二、架构设计

### 2.1 三 Skill 职责分工

|| Skill | 职责 | 输出 |
|-------|------|------|
| **plan-review-skill** | 评审规划 | PLAN.md + `.target-trigger` |
| **task-split-skill** | 拆解任务 | milestone + subTask → `.target-state.json` |
| **target-skill** | 追踪执行 | 持续追踪 milestone/subTask 状态 |

### 2.2 交接协议

```
plan-review-skill 评审通过
    ↓ 【写触发文件】
.target-trigger
    ↓ 【target-skill 启动时检查】
读取 PLAN.md
    ↓ 【发现 milestone 需要拆解】
触发 task-split-skill
    ↓ 【在 milestone 下拆 sub-task】
.task-state.json（milestone + subTask）
    ↓ 【task-split 输出后】
target-skill 接管追踪
    ↓ 【持续追踪 milestone/subTask 状态】
执行完成
```

```
plan-review-skill 评审通过
    ↓ 【写触发文件】
.target-trigger（已批准标记）
    ↓ 【target-skill 启动时检查】
读取 docs/PLAN.md
    ↓ 【LLM 解析】
初始化 .target-state.json
    ↓ 【激活追踪】
持续追踪 milestone / sub-task / blocker 状态
```

### 2.2 目标：代码最少化

| 组件 | 做法 | 代码量 |
|------|------|--------|
| `.target-trigger` 写入 | plan-review-skill 改动 1 处 | ~5 行 |
| `.target-state.json` 读写 | target-track.py（只做序列化/反序列化） | ~60 行 |
| 进度报告生成 | LLM 驱动，按 SOP 输出 | 0 行代码 |
| 交接协议解析 | LLM 驱动，读 PLAN.md 输出报告 | 0 行代码 |

### 2.3 无 plan-review-skill 时的兼容

```
情况A：有 plan-review-skill（装了 dev-skill）
  评审通过 → 写 .target-trigger → target-skill 读取 → 自动激活追踪

情况B：没有 plan-review-skill（只装了 base-skill）
  用户手动「设定目标」
    → LLM 按 target-skill SKILL.md 的 SOP 生成 .target-state.json
    → 正常追踪（完全独立，不依赖任何外部 skill）
```

---

## 三、文件设计

### 3.1 `.target-trigger`（新增）

**创建者**：plan-review-skill（评审通过时）
**读者**：target-skill（启动时）

```json
{
  "version": "1.0",
  "planFile": "docs/PLAN.md",
  "approvedAt": "2026-05-17T12:00:00+08:00",
  "approvedBy": "张三",
  "goal": "构建用户认证系统"
}
```

**生命周期**：
- 创建：plan-review-skill 批准时
- 读取：target-skill 启动追踪时（一次性读取，不锁定）
- 删除：用户主动关闭追踪时（LLM 按 SOP 删除）

### 3.2 `.target-state.json`（增强现有格式）

**在现有格式基础上新增字段，向后兼容：**

```json
{
  "goal": "构建用户认证系统",
  "phase": "active",
  "source": "plan-review",
  "planFile": "docs/PLAN.md",
  "createdAt": "2026-05-17T12:00:00+08:00",
  "milestones": [
    {
      "id": "M1",
      "title": "数据库设计",
      "status": "done",
      "completedAt": "2026-05-17T14:00:00+08:00",
      "subTasks": [
        {
          "id": "M1-1",
          "title": "设计用户表 schema",
          "status": "done",
          "completedAt": "2026-05-17T13:00:00+08:00"
        }
      ]
    },
    {
      "id": "M2",
      "title": "API 实现",
      "status": "active",
      "completedAt": null,
      "subTasks": [
        {
          "id": "M2-1",
          "title": "实现登录 API",
          "status": "blocked",
          "blockedAt": "2026-05-17T15:00:00+08:00",
          "blocker": "等待数据库连接池配置完成"
        },
        {
          "id": "M2-2",
          "title": "实现注册 API",
          "status": "pending"
        }
      ]
    }
  ],
  "deliverables": [
    {
      "id": "D1",
      "title": "API 接口文档",
      "status": "pending",
      "linkedTask": "M2-1"
    }
  ],
  "blockers": [
    {
      "id": "B1",
      "taskId": "M2-1",
      "description": "数据库连接池配置未完成",
      "createdAt": "2026-05-17T15:00:00+08:00",
      "resolved": false
    }
  ],
  "changeLog": [
    {
      "time": "2026-05-17T12:00:00+08:00",
      "action": "接管 plan-review 追踪",
      "detail": "来源: docs/PLAN.md"
    },
    {
      "time": "2026-05-17T15:00:00+08:00",
      "action": "sub-task 进入 blocked",
      "detail": "M2-1: 等待数据库连接池"
    }
  ]
}
```

**新增字段说明：**

| 字段 | 位置 | 说明 |
|------|------|------|
| `source` | 顶层 | `"manual" \| "plan-review"` |
| `planFile` | 顶层 | 关联的 PLAN.md 路径 |
| `status` | subTask | `pending \| active \| blocked \| done` |
| `blockedAt` | subTask | 进入 blocked 的时间 |
| `blocker` | subTask | 阻塞原因描述 |
| `deliverables` | 顶层 | 交付物列表（从 PLAN.md 读取） |
| `blockers` | 顶层 | 阻塞问题列表 |

---

## 四、plan-review-skill 改动

### 4.1 改动范围

**只改 1 处**：`scripts/plan-review.py` 的 `cmd_approve()` 函数

**当前逻辑**：
```python
def cmd_approve(plan_file: Path) -> None:
    update_status(plan_file, "approved")
    save_snapshot(plan_file)
```

**改动后**：
```python
def cmd_approve(plan_file: Path) -> None:
    update_status(plan_file, "execution")
    save_snapshot(plan_file)
    _write_target_trigger(plan_file)  # ← 新增 1 行
```

**新增函数（约 15 行）**：
```python
def _write_target_trigger(plan_file: Path) -> None:
    """评审通过后，写 .target-trigger 触发文件"""
    import json, datetime
    trigger = {
        "version": "1.0",
        "planFile": str(plan_file),
        "approvedAt": datetime.datetime.now().isoformat(),
        "goal": _extract_goal(plan_file)
    }
    trigger_file = plan_file.parent.parent / ".target-trigger"
    trigger_file.write_text(json.dumps(trigger, ensure_ascii=False, indent=2))
    print(f"  [TRIGGER] {trigger_file}")
```

### 4.2 验证用例

```bash
# 准备测试
mkdir -p /tmp/test-handover/docs
cat > /tmp/test-handover/docs/PLAN.md << 'EOF'
---
status: draft
---
# 项目愿景
构建认证系统
EOF

# 执行批准
python3 scripts/plan-review.py approve /tmp/test-handover/docs/PLAN.md

# 验证
grep "execution" /tmp/test-handover/docs/PLAN.md     # 状态应为 execution
cat /tmp/test-handover/.target-trigger               # 应为合法 JSON
echo "✅ 批准测试通过"
```

---

## 五、target-skill 改动

### 5.1 改动范围

| 文件 | 改动量 |
|------|--------|
| `SKILL.md` | 新增触发词 + 交接协议章节 + 增强追踪 SOP（约 80 行文档） |
| `scripts/target-track.py` | 新增（约 60 行，只做文件读写） |

### 5.2 新增触发条件

SKILL.md 新增触发词（放在 metadata.triggers 或文档中）：

```
批准了规划、开始执行、执行追踪、当前进度
有什么被阻塞了、切换到执行模式
```

### 5.3 新增章节：交接协议（SKILL.md）

```markdown
## 交接协议

### 从 plan-review-skill 接管

**触发条件**：存在 `.target-trigger` 文件

**LLM 操作步骤**（按顺序执行）：

1. **读取触发文件**
   检查项目根目录是否存在 `.target-trigger`

2. **解析 PLAN.md**
   从 `docs/PLAN.md` 读取：
   - 项目愿景 → goal
   - 里程碑表格 → milestones
   - 交付物表格 → deliverables

3. **初始化追踪状态**
   生成 `.target-state.json`，状态全部初始化为 `pending`

4. **激活追踪**
   向用户输出：
   ```
   📌 检测到已批准的规划：{goal}
   已从 {planFile} 恢复 {N} 个里程碑
   开始执行追踪...
   ```

### 读取 PLAN.md 的 SOP

当需要从 PLAN.md 解析 milestone 时：

1. 在 PLAN.md 中找到「里程碑」表格
2. 提取每行的：ID、标题、验收标准
3. 映射到 `.target-state.json` 的 milestones 数组
4. 同样的方式处理「交付物」表格

**注意**：LLM 直接解析 markdown 表格，不需要额外脚本。
```

### 5.4 进度报告 SOP（LLM 驱动，0 行代码）

当用户问「当前进度」时，按以下 SOP 输出：

```markdown
## 📊 执行进度

**目标**: {goal}
**总体进度**: {X}%
**进行中**: {N} 个任务
**已完成**: {N} 个任务
**被阻塞**: {N} 个任务

### Milestone 状态

| Milestone | 状态 | 进度 |
|-----------|------|------|
| {M1} | ✅ 完成 | 100% |
| {M2} | 🔵 进行中 | 60% |
| {M3} | ⬜ 待开始 | 0% |

### 当前任务

🔵 正在做：{当前 active 的 sub-task}
⚠️ 被阻塞：{blocked 的 sub-task}（原因: {blocker}）

### 阻塞问题

| # | 任务 | 阻塞原因 | 时长 |
|---|------|---------|------|
| B1 | {task} | {reason} | {duration} |

### 交付物

| 交付物 | 状态 | 关联任务 |
|--------|------|---------|
| {D1} | ⏳ | {task} |
```

### 5.5 target-track.py（新增，最小化）

**只做 3 件事**：
1. 读取 `.target-state.json`
2. 写入 `.target-state.json`（LLM 构造好数据后调用）
3. 从 `.target-trigger` 读取 planFile 路径

**不做的**：
- 不解析 PLAN.md（LLM 做）
- 不生成报告（LLM 按 SOP 做）
- 不做状态计算（LLM 判断）

**脚本内容（约 60 行）**：

```python
#!/usr/bin/env python3
"""
target-track.py — 目标追踪状态读写

用法：
  python3 target-track.py read [项目路径]      # 读取当前状态
  python3 target-track.py write [项目路径]    # 写入状态（从 stdin 读 JSON）
  python3 target-track.py trigger [项目路径]   # 检查 trigger，返回 planFile
"""

import json, sys
from pathlib import Path

def read_state(project: Path) -> dict | None:
    f = project / ".target-state.json"
    if f.exists():
        return json.loads(f.read_text())
    return None

def write_state(project: Path, data: dict) -> None:
    (project / ".target-state.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2)
    )

def get_trigger(project: Path) -> dict | None:
    f = project / ".target-trigger"
    if f.exists():
        return json.loads(f.read_text())
    return None

if __name__ == "__main__":
    cmd, *args = sys.argv[1:] or ["read"]
    project = Path(args[0]) if args else Path.cwd()

    if cmd == "read":
        print(json.dumps(read_state(project), ensure_ascii=False, indent=2))
    elif cmd == "write":
        data = json.load(sys.stdin)
        write_state(project, data)
    elif cmd == "trigger":
        print(json.dumps(get_trigger(project), ensure_ascii=False, indent=2))
```

### 5.6 target-skill 改动验证用例

```bash
# 准备环境
mkdir -p /tmp/test-target/{docs,docs/reviews}
cat > /tmp/test-target/docs/PLAN.md << 'EOF'
---
status: approved
---
# 项目愿景
构建认证系统

# 里程碑
| ID | 里程碑 | 验收标准 | 状态 |
|----|--------|---------|------|
| M1 | 数据库设计 | schema 已评审 | done |
| M2 | API 实现 | 单元测试通过 | active |

# 交付物
| 交付物 | 负责人 | 截止日期 |
|--------|--------|---------|
| API 文档 | 张三 | 2026-05-20 |
EOF

cat > /tmp/test-target/.target-trigger << 'EOF'
{
  "version": "1.0",
  "planFile": "docs/PLAN.md",
  "approvedAt": "2026-05-17T12:00:00+08:00",
  "goal": "构建认证系统"
}
EOF

# 验证 trigger 读取
python3 scripts/target-track.py trigger /tmp/test-target
# 预期：输出 JSON

# 验证 state 读写
echo '{}' | python3 scripts/target-track.py write /tmp/test-target
cat /tmp/test-target/.target-state.json
# 预期：写入成功

echo "✅ target-track.py 测试通过"
```

---

## 六、task-split-skill 调整（核心改动）

### 6.1 问题：原设计跳过了 task-split

原设计：
```
plan-review-skill → target-skill 直连
                  ↑
         target-skill 自己拆 sub-task
```

**问题**：target-skill 自己从 PLAN.md 解析 milestone 后，还要自己拆 sub-task。
这不符合职责分离原则——拆解应该是 task-split 的职责。

### 6.2 调整后的 workflow

```
plan-review-skill（评审通过）
    ↓ 写 .target-trigger
target-skill（启动，检测到 trigger）
    ↓ 读取 PLAN.md
    ↓ 发现 milestone 有 sub-task 需要拆解
    ↓ 触发 task-split-skill
task-split-skill（在 milestone 下拆 sub-task）
    ↓ 输出 milestone + subTask 到 .target-state.json
target-skill（接管追踪）
    ↓ 持续追踪 milestone/subTask 状态
```

### 6.3 task-split-skill 的改动

**新增能力：读取 PLAN.md + 输出对标 .target-state.json**

#### 与 base-skill 的兼容性

**原则**：始终检查 `docs/PLAN.md` 是否存在，不检查 plan-review-skill 是否安装。

| 情况 | 行为 |
|------|------|
| `docs/PLAN.md` 存在且格式正确 | 读取 milestone，在其下拆 sub-task，输出 milestone + subTask |
| `docs/PLAN.md` 存在但格式混乱 | **忽略 PLAN.md，走原有 Step 1**（不报错，不卡住） |
| `docs/PLAN.md` 不存在 | 走原有 Step 1 澄清流程，输出扁平列表 |
| plan-review-skill 未安装 | 不影响，PLAN.md 可以是用户手动创建的 |

> 注意：PLAN.md 的来源不重要，只需要检查文件是否存在。
> 格式错误时 fallback 到 Step 1，不需要用户修复。

### 判断规则

拆解前检查项目根目录是否存在 `docs/PLAN.md`：
- **存在** → 尝试读取 milestone
  - 成功 → 在 milestone 下拆 sub-task
  - **失败（格式混乱）→ 走原有 Step 1**
- **不存在** → 走原有 Step 1 澄清流程

#### SKILL.md 改动清单

**新增章节「与 PLAN.md 协同」（~60 行）**：

```markdown
## 与 PLAN.md 协同

### 判断规则

拆解前检查项目根目录是否存在 `docs/PLAN.md`：
- **存在** → 读取 milestone，在其下拆 sub-task
- **不存在** → 走原有 Step 1 澄清流程

### 读取 PLAN.md

从 `docs/PLAN.md` 提取：

| 章节 | 提取内容 |
|------|---------|
| `# 项目愿景` | 作为大目标 |
| `| ID | 里程碑 |` 表格 | milestone 的 id + title |
| `| ID | 交付物 |` 表格 | 关联到 milestone |

### 输出格式

有 PLAN.md 时，在每个 milestone 下拆 sub-task，输出 milestone + subTask 结构。
无 PLAN.md 时，维持原有扁平任务列表。

### 触发 target-skill

用户说「开始执行」或「追踪这个计划」时：
1. 输出 milestone + subTask 结构
2. 通知用户可使用 target-skill 追踪
3. 不自动触发（target-skill 由用户主动激活）
```

#### 改动量

| 文件 | 改动 |
|------|------|
| SKILL.md | 新增「与 PLAN.md 协同」章节（~60 行） |
| learns/ | 记录本次调整踩坑（~10 行） |

**无代码改动。**

---

## 七、实施顺序

### Phase 1：plan-review-skill（先做）

**目标**：评审通过时写 `.target-trigger`

**改动**：
- `scripts/plan-review.py`：在 `cmd_approve()` 中加 `_write_target_trigger()`

**验证**：
```bash
# 见 4.2 验证用例
```

### Phase 2：task-split-skill（第二）

**目标**：读取 PLAN.md + 输出 milestone + subTask 结构

**改动**：
- `SKILL.md`：新增「与 PLAN.md 协同」章节 + 两种输出模式
- `learns/`：记录本次调整踩坑

**验证**：
```bash
# 有 PLAN.md 时输出 milestone + subTask
# 无 PLAN.md 时输出扁平列表（向后兼容）
```

### Phase 3：target-skill（第三）

**目标**：从 task-split 接管 milestone + subTask 追踪，而非自己解析 PLAN.md

**改动**：
- `SKILL.md`：从 `.target-state.json` 接管 milestone + subTask，而非自己解析 PLAN.md
- `scripts/target-track.py`：新增（60 行）

**验证**：
```bash
# 见 5.6 验证用例
```

---

## 八、向后兼容

| 场景 | 行为 |
|------|------|
| 无 `.target-trigger`，用户手动「设定目标」 | 使用现有 SOP，写入 `.target-state.json`（完全独立） |
| 有 `.target-trigger`，无旧 state | 从 trigger 读取 planFile，LLM 解析 PLAN.md 初始化 |
| 有 `.target-trigger`，有旧 state | 以 trigger 的 planFile 为准，重新从 PLAN.md 解析 |

---

## 九、文件位置汇总

|| 文件 | 位置 | 创建者 | 读者 |
|------|------|--------|-------|
| `docs/PLAN.md` | 项目/docs/ | 用户, plan-review-skill | 用户, plan-review-skill, task-split-skill（LLM 读取） |
| `.target-trigger` | 项目根目录/ | plan-review-skill | target-skill（一次性读取） |
| `.target-state.json` | 项目根目录/ | task-split-skill（输出）→ target-skill（读写） | target-skill |
| `docs/reviews/` | 项目/docs/ | plan-review-skill | 用户 |
| `docs/TODO.md` | 项目/docs/ | （可选）task-split-skill 输出草稿 | 用户, target-skill |

---

## 十、风险与边界

| 风险 | 缓解 |
|------|------|
| `.target-trigger` 被误删 | target-skill 仍可从 `.target-state.json` 恢复（向后兼容） |
| PLAN.md 结构不规范（无表格） | LLM 按实际内容解析，表格解析失败时手动补充 |
| sub-task 太多难以管理 | 进度报告只显示 `blocked` + `active` 的任务 |
| 用户同时有多个项目在进行 | 每个项目有独立的 `.target-state.json`，不影响 |
