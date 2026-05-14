#!/bin/bash
# task-split-skill setup script

set -e

echo "Setting up task-split-skill..."

# OpenClaw
if command -v clawhub &> /dev/null; then
    clawhub install task-split
    echo "[OpenClaw] installed"
fi

# Claude Code
mkdir -p ~/claude/skills/task-split
cp SKILL.md ~/claude/skills/task-split/ 2>/dev/null || true
echo "[Claude Code] installed"

# Codex
mkdir -p ~/codex/skills/task-split
cp SKILL.md ~/codex/skills/task-split/ 2>/dev/null || true
echo "[Codex] installed"

# Hermes
mkdir -p ~/.hermes/skills/task-split
cp SKILL.md ~/.hermes/skills/task-split/ 2>/dev/null || true
echo "[Hermes] installed"

echo "Done! task-split-skill ready."
chmod +x "$0"
