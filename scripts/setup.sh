#!/bin/bash
# task-split-skill setup script
# 使用 skill-sync 同步：python3 $(repos_root)/skill-sync/scripts/sync-hermes-skills.py

set -e

echo "Setting up task-split-skill..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
SKILL_SYNC="$REPO_DIR/skill-sync/scripts/sync-hermes-skills.py"

# ─── 前置依赖 ───────────────────────────────────────────────────
# platform-detect: Hermes 内置模块，非 Hermes 环境需安装
if python3 -c "import platform_detect" 2>/dev/null; then
    echo "[deps] platform-detect ✅"
else
    echo "[deps] platform-detect ❌ 未安装，尝试安装..."
    pip install platform-detect -q && echo "[deps] platform-detect ✅ 安装成功" || echo "[deps] platform-detect ⚠️ 安装失败，请手动: pip install platform-detect"
fi

# ─── Skill 安装 ─────────────────────────────────────────────────
if [ -f "$SKILL_SYNC" ]; then
    echo "[Hermes] 使用 skill-sync 同步..."
    python3 "$SKILL_SYNC" task-split-skill
else
    echo "[Hermes] skill-sync 未找到，使用手动安装..."
    mkdir -p ~/.hermes/skills/task-split
    cp "$REPO_DIR/SKILL.md" ~/.hermes/skills/task-split/
fi

# OpenClaw
if command -v clawhub &> /dev/null; then
    echo "[OpenClaw] installing..."
    clawhub install task-split 2>/dev/null || echo "[OpenClaw] skipped (not configured)"
fi

# Claude Code
if [ -d ~/claude/skills ]; then
    mkdir -p ~/claude/skills/task-split
    cp "$REPO_DIR/SKILL.md" ~/claude/skills/task-split/
    echo "[Claude Code] installed"
fi

# Codex
if [ -d ~/codex/skills ]; then
    mkdir -p ~/codex/skills/task-split
    cp "$REPO_DIR/SKILL.md" ~/codex/skills/task-split/
    echo "[Codex] installed"
fi

echo ""
echo "Done! task-split-skill ready."
