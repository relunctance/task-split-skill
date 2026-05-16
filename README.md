<div align="center">

# task-split-skill

AI Agent 任务拆解方法论 — 将模糊需求拆解为可执行、可追踪、可验证的工作计划

</div>

---

## 核心特性

| 特性 | 说明 |
|------|------|
| 🧩 **五步拆解法** | 澄清 → 交付物识别 → 分解排序 → 风险预判 → 执行追踪 |
| ❓ **澄清问题模板** | Step 1 必填 4 问，不澄清不拆解 |
| ✅ **验收标准强制** | 每个子任务必须有可检查的验收条件 |
| 📐 **粒度控制** | 原子/组合/里程碑三级粒度 + 明确反例 |
| 🔗 **依赖建模** | 串行、并行分支、菱形依赖 + task-list.py 工具支撑（树/统计由 LLM 直接读 JSON） |
| ⚡ **动态调整** | 执行中实时响应变化，插入/合并/删除任务 |
| 🔄 **Skill 协同** | 拆解是思考过程，Skill 是快捷方式，Memory 是笔记本 |

---

## 触发条件

> ⚠️ 与 OpenSpec 边界清晰：OpenSpec 由 `/opsx:` 命令触发，task-split 由自然语言触发。

| 触发词 | 说明 |
|--------|------|
| `任务拆解` / `拆解任务` / `拆解成` | 核心触发 |
| `工作分解` / `WBS` | 专业术语 |
| `task decomposition` / `task split` | 英文触发 |

**不触发**： `/opsx:` → OpenSpec | `目标追踪` → target-skill

---

## 快速开始

```bash
# 安装（推荐方式）
bash ~/repos/task-split-skill/scripts/setup.sh

# 或手动复制
mkdir -p ~/.hermes/skills/task-split
cp SKILL.md ~/.hermes/skills/task-split/
```

---

## 五步拆解流程

```
用户需求（模糊）
    │
    ▼
Step 1: 澄清问题（4 个必填问题）
    │
    ▼
Step 2: 识别交付物 + 验收标准（每个任务必填）
    │
    ▼
Step 3: 分解 & 排序（依赖建模）
    │
    ▼
Step 4: 风险预判
    │
    ▼
Step 5: task-list.py 创建 + 执行追踪
```

---

## Step 1 — 澄清问题模板（必填）

```
## 澄清问题

1. 最终交付物是什么？（具体文件/功能/路径）
2. 成功标准是什么？（可运行/可部署/具体指标）
3. 限制条件有哪些？（技术栈/兼容性/安全）
4. MVP 范围 vs 完整版？
```

---

## Step 2 — 验收标准示例

```
❌ Bad: "功能正常运行"
✅ Good: "POST /api/login 返回 200 + token；空 body 返回 400；密码错误返回 401"

❌ Bad: "完善文档"
✅ Good: "README.md 包含：安装步骤（3步）、快速开始（2个命令）、troubleshooting（4个问题）"
```

---

## 依赖建模示例

```bash
# 创建任务并建立依赖
python task-list.py create "调研 API" --priority P1
python task-list.py create "设计模型" --priority P1 --depends 1
python task-list.py create "实现后端" --priority P1 --depends 2
python task-list.py create "前端开发" --priority P2 --depends 2
python task-list.py create "集成测试" --priority P1 --depends 3,4

# 查看任务列表（LLM 直接读 .task-list.json 描述依赖关系）
python task-list.py list
```

---

## 粒度原则

| 场景 | 决策 |
|------|------|
| > 5 分钟 / 3+ 文件 / 多个方案 | ✅ 必须拆解 |
| 单行 fix / 纯查询 / 用户说"just do it" | ❌ 不拆解 |

---

## 与其他 Skill 的关系

| Skill | 职责 | 触发 |
|--------|------|------|
| **task-split** | 任务拆解 | 自然语言 |
| **OpenSpec** | 开发规范 | `/opsx:` 命令 |
| **target-skill** | 目标追踪 | 用户主动开启 |

---

## 平台支持

| 平台 | 状态 | 安装 |
|------|------|------|
| OpenClaw | ✅ | `clawhub install task-split` |
| Claude Code | ✅ | 复制 SKILL.md 到 `~/claude/skills/task-split/` |
| Codex | ✅ | 复制 SKILL.md 到 `~/.codex/skills/task-split/` |
| Hermes | ✅ | `bash scripts/setup.sh` |
| Cursor | ✅ | 复制到 `.cursor/rules/` |

---

## 目录结构

```
task-split-skill/
├── SKILL.md          # 完整 Skill 定义（方法论 + CLI 参考 + 踩坑）
├── README.md         # 本文档
├── LICENSE           # MIT
├── scripts/
│   ├── task-list.py # 任务列表管理 CLI（创建/开始/完成/依赖/树/统计）
│   └── setup.sh     # 多平台安装脚本
```

---

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.2.0 | 2026-05-15 | Step 1 澄清模板强制化；验收标准每任务必填；task-list.py CLI 完整参考；trigger 去冲突；与 OpenSpec/target-skill 边界定义 |
| 1.1.0 | 2026-05-15 | 初版发布 |

---

<div align="center">

MIT License © [relunctance](https://github.com/relunctance)

</div>
