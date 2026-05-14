#!/bin/bash
# task-split-skill setup script
# 推荐使用 skill-sync 同步：python3 ~/repos/skill-sync/scripts/sync-hermes-skills.py

set -e

echo "Setting up task-split-skill..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

# Hermes（推荐方式）
if [ -f ~/repos/skill-sync/scripts/sync-hermes-skills.py ]; then
    echo "[Hermes] 使用 skill-sync 同步..."
    python3 ~/repos/skill-sync/scripts/sync-hermes-skills.py task-split-skill
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
echo "推荐：python3 ~/repos/skill-sync/scripts/sync-hermes-skills.py"
