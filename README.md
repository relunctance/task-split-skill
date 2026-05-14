<div align="center">

![task-split-skill](assets/banner.svg)

</div>

<p align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Supported-blueviolet)](https://github.com/openclaw)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-green)](https://claude.ai)
[![Codex](https://img.shields.io/badge/Codex-Compatible-orange)](https://github.com)
[![Hermes](https://img.shields.io/badge/Hermes-Agent-blue)](https://github.com)

</p>

<div align="center">

# task-split-skill

AI Agent 任务拆解方法论 — 将模糊需求拆解为可执行、可追踪、可验证的工作计划

</div>

---

## 核心特性

| 特性 | 说明 |
|------|------|
| 🧩 **五步拆解法** | 理解澄清 → 交付物识别 → 分解排序 → 风险预判 → 执行追踪 |
| 📐 **粒度控制** | 原子任务 / 组合任务 / 里程碑任务三级粒度 |
| 🔗 **依赖建模** | 串行、并行分支、菱形依赖三种模式 |
| ⚡ **动态调整** | 执行中实时响应变化，插入/合并/删除任务 |
| 🔄 **与 Skill 协同** | 拆解是思考过程，Skill 是快捷方式，Memory 是笔记本 |

---

## 快速开始

```bash
# Hermes
mkdir -p ~/.hermes/skills/task-split
cp SKILL.md ~/.hermes/skills/task-split/

# Claude Code
mkdir -p ~/claude/skills/task-split
cp SKILL.md ~/claude/skills/task-split/
```

---

## 触发条件

- 任务拆解 / task decomposition
- 拆解任务 / 拆解
- 任务规划 / task planning
- 子任务 / 工作分解 / WBS

---

## 方法论概览

### 五步拆解流程

```
用户需求（模糊）
    │
    ▼
Step 1: 理解 & 澄清 → 核心目标？隐含约束？需要 Plan Mode？
    │
    ▼
Step 2: 识别交付物 → 最终产出什么？验收标准是什么？
    │
    ▼
Step 3: 分解 & 排序 → 按依赖排列，识别并行分支
    │
    ▼
Step 4: 风险预判 → 哪里可能出错？Plan B 是什么？
    │
    ▼
Step 5: 执行追踪 → TaskCreate + addBlockedBy + 实时状态更新
```

### 黄金法则

> **一个任务的描述应该让另一个 Agent 看了就能直接执行，不需要额外上下文。**

```
❌ 差: "完善文档"
✅ 好: "在 docs/STATUS.md 的角色表格中追加新行，格式为 | 角色名 | 描述 | ✅ |"
```

### 依赖关系模式

```
串行: [调研] → [设计] → [实现] → [测试]

并行:       ┌→ [页面 A] ─┐
     [设计] ┤             ├→ [集成测试]
             └→ [页面 B] ─┘

菱形: [后端] ──┐
               ├──→ [联调]
       [前端] ──┘
```

---

## 平台支持

| 平台 | 状态 | 安装方式 |
|------|------|---------|
| OpenClaw | ✅ 支持 | `clawhub install task-split` |
| Claude Code | ✅ 支持 | 复制 SKILL.md 到 `~/claude/skills/task-split/` |
| Codex | ✅ 支持 | 复制 SKILL.md 到 `~/.codex/skills/task-split/` |
| Hermes | ✅ 支持 | 复制 SKILL.md 到 `~/.hermes/skills/task-split/` |

---

## 详见

完整的 SKILL.md 定义、参数说明和踩坑记录请查阅 [SKILL.md](SKILL.md)。

---

<div align="center">

MIT License © [relunctance](https://github.com/relunctance)

</div>
