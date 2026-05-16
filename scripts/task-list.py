#!/usr/bin/env python3
"""
task-list — 任务列表管理脚本

用法：
  python task-list.py create "任务标题" --priority P0 --depends 1,2
  python task-list.py list --status pending
  python task-list.py start 1
  python task-list.py done 1
  python task-list.py block 3 --by 2
  python task-list.py tree
  python task-list.py stats

状态文件：跨平台自适应，优先用户目录，fallback 当前目录
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

# ─── 跨平台状态文件路径 ───────────────────────────────────────────
# 优先用户目录，fallback 当前目录
_USER_STATE = Path.home() / ".task-list.json"
_CWD_STATE = Path(".task-list.json")

def _get_state_file() -> Path:
    """优先使用用户目录，确保不同工作目录下共享同一状态文件。"""
    try:
        # 用户目录可写 → 用用户目录
        if os.access(Path.home(), os.W_OK):
            return _USER_STATE
    except Exception:
        pass
    # fallback 当前目录
    return _CWD_STATE

STATE_FILE = _get_state_file()
BACKUP_FILE = STATE_FILE.with_suffix(".json.bak")


# ─── 工具函数 ───────────────────────────────────────────────────

def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def load_tasks() -> list:
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return []


def save_tasks(tasks: list) -> None:
    if STATE_FILE.exists():
        shutil.copy2(STATE_FILE, BACKUP_FILE)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def next_id(tasks: list) -> int:
    return max((t["id"] for t in tasks), default=0) + 1


# ─── 状态描述 ───────────────────────────────────────────────────

STATUS_EMOJI = {
    "pending": "⬜",
    "in_progress": "🔄",
    "blocked": "🔒",
    "completed": "✅",
    "deleted": "🗑️",
}

PRIORITY_EMOJI = {
    "P0": "🔴",
    "P1": "🟡",
    "P2": "🟢",
    "P3": "⚪",
}


# ─── 子命令 ───────────────────────────────────────────────────

def cmd_create(title: str, priority: str = "P1", depends: list = None) -> str:
    tasks = load_tasks()
    tid = next_id(tasks)

    if depends is None:
        depends = []
    task = {
        "id": tid,
        "title": title,
        "priority": priority,
        "status": "pending",
        "depends": depends,
        "createdAt": now(),
        "startedAt": None,
        "completedAt": None,
    }

    # 检查依赖是否存在
    if depends:
        for d in depends:
            if not any(t["id"] == d for t in tasks):
                return f"❌ 依赖的任务 ID {d} 不存在"

    tasks.append(task)
    save_tasks(tasks)

    dep_str = f"（依赖 #{d}）" if depends else ""
    return (f"✅ 任务已创建\n\n"
            f"**[{tid}] {title}** {PRIORITY_EMOJI.get(priority, '⚪')} {priority} {dep_str}")


def cmd_list(status: str = None, priority: str = None) -> str:
    tasks = load_tasks()
    if not tasks:
        return "📌 暂无任务"

    # 默认不显示已删除的任务，但用户显式指定 --status deleted 时除外
    if status == "deleted":
        filtered = [t for t in tasks if t["status"] == "deleted"]
    else:
        filtered = [t for t in tasks if t["status"] != "deleted"]
        if status:
            filtered = [t for t in filtered if t["status"] == status]
        if priority:
            filtered = [t for t in filtered if t.get("priority") == priority]

    if not filtered:
        return "📌 没有符合条件的任务"

    lines = ["## 📋 任务列表"]
    if status or priority:
        parts = []
        if status:
            parts.append(f"状态={status}")
        if priority:
            parts.append(f"优先级={priority}")
        lines[0] += f"（{'，'.join(parts)}）"

    for t in sorted(filtered, key=lambda x: (x.get("priority", "P9"), x["id"])):
        e = STATUS_EMOJI.get(t["status"], "⬜")
        p = t.get("priority", "P1")
        pe = PRIORITY_EMOJI.get(p, "⚪")
        deps = f" ← #{','.join(str(d) for d in t.get('depends', []))}" if t.get('depends') else ""
        lines.append(f"{e} [{t['id']}] {pe} {p} {t['title']}{deps}")

    # 统计
    total = len(filtered)
    done = sum(1 for t in filtered if t["status"] == "completed")
    lines.append(f"\n进度：{done}/{total} 完成")
    return "\n".join(lines)


def cmd_start(tid: int) -> str:
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == tid:
            # 检查依赖是否全部完成
            incomplete = [d for d in t.get("depends", []) if not any(
                x["id"] == d and x["status"] == "completed" for x in tasks)]
            if incomplete:
                return (f"🔒 任务 #{tid} 被依赖阻塞\n\n"
                        f"以下前置任务尚未完成：{', '.join(f'#{d}' for d in incomplete)}\n\n"
                        f"请先完成这些任务，或用 `unblock {tid}` 解除依赖")

            t["status"] = "in_progress"
            t["startedAt"] = now()
            save_tasks(tasks)
            return f"🔄 任务 #{tid}「{t['title']}」已开始"
    return f"❌ 未找到任务 #{tid}"


def cmd_done(tid: int) -> str:
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == tid:
            t["status"] = "completed"
            t["completedAt"] = now()
            save_tasks(tasks)
            done = sum(1 for x in tasks if x["status"] == "completed")
            total = len(tasks)
            return (f"✅ 任务「{t['title']}」已完成\n\n"
                    f"总进度：{done}/{total}")
    return f"❌ 未找到任务 #{tid}"


def cmd_block(tid: int, by: list = None) -> str:
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == tid:
            if by:
                for b in (by or []):
                    if not any(x["id"] == b for x in tasks):
                        return f"❌ 阻塞任务 #{b} 不存在"
                t["depends"] = list(set(t.get("depends", [])) | set(by))
                t["status"] = "blocked"
                save_tasks(tasks)
                return f"🔒 任务 #{tid} 已被 #{', '.join(str(b) for b in by)} 阻塞"
            return f"❌ 请指定 --by <任务ID>"
    return f"❌ 未找到任务 #{tid}"


def cmd_unblock(tid: int) -> str:
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == tid:
            t["depends"] = []
            t["status"] = "pending"
            save_tasks(tasks)
            return f"🔓 任务 #{tid}「{t['title']}」已解除阻塞"
    return f"❌ 未找到任务 #{tid}"


def cmd_delete(tid: int) -> str:
    tasks = load_tasks()
    for i, t in enumerate(tasks):
        if t["id"] == tid:
            t["status"] = "deleted"
            save_tasks(tasks)
            return f"🗑️ 任务「{t['title']}」已删除"
    return f"❌ 未找到任务 #{tid}"


def cmd_tree() -> str:
    tasks = load_tasks()
    if not tasks:
        return "📌 暂无任务"

    active = [t for t in tasks if t["status"] != "deleted"]
    lines = ["## 🌲 任务依赖树"]

    # 找出没有依赖的根任务
    roots = [t for t in active if not t.get("depends")]
    completed_ids = {t["id"] for t in active if t["status"] == "completed"}

    def render(tid: int, prefix: str = "", is_last: bool = True) -> list:
        result = []
        # 找所有依赖这个任务的任务
        children = [t for t in active if tid in t.get("depends", [])]

        # 找自己
        task = next((t for t in active if t["id"] == tid), None)
        if task is None:
            return result

        e = STATUS_EMOJI.get(task["status"], "⬜")
        p = task.get("priority", "P1")
        pe = PRIORITY_EMOJI.get(p, "⚪")
        conn = "└── " if is_last else "├── "
        result.append(f"{prefix}{conn}{e} [{tid}] {pe} {p} {task['title']}")

        child_prefix = prefix + ("    " if is_last else "│   ")
        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)
            result.extend(render(child["id"], child_prefix, is_last_child))
        return result

    rendered = []
    for i, root in enumerate(roots):
        is_last_root = (i == len(roots) - 1)
        rendered.extend(render(root["id"], "", is_last_root))

    if rendered:
        lines.extend(rendered)

    # 统计
    done = sum(1 for t in active if t["status"] == "completed")
    in_prog = sum(1 for t in active if t["status"] == "in_progress")
    blocked = sum(1 for t in active if t["status"] == "blocked")
    lines.append(f"\n📊 {done} 完成 | {in_prog} 进行中 | {blocked} 阻塞 | {len(active)} 总计")
    return "\n".join(lines)


def cmd_stats() -> str:
    tasks = load_tasks()
    active = [t for t in tasks if t["status"] != "deleted"]
    if not active:
        return "📌 暂无任务"

    by_status = {}
    for t in active:
        s = t["status"]
        by_status[s] = by_status.get(s, 0) + 1

    by_priority = {}
    for t in active:
        p = t.get("priority", "P1")
        by_priority[p] = by_priority.get(p, 0) + 1

    lines = ["## 📊 任务统计"]
    lines.append(f"**总计**: {len(active)} 个任务")

    lines.append("\n按状态：")
    for s, cnt in sorted(by_status.items()):
        e = STATUS_EMOJI.get(s, "⬜")
        lines.append(f"  {e} {s}: {cnt}")

    lines.append("\n按优先级：")
    for p in ["P0", "P1", "P2", "P3"]:
        cnt = by_priority.get(p, 0)
        pe = PRIORITY_EMOJI.get(p, "⚪")
        if cnt:
            lines.append(f"  {pe} {p}: {cnt}")

    done = by_status.get("completed", 0)
    total = len(active)
    pct = int(done / total * 100) if total else 0
    lines.append(f"\n完成率：{done}/{total} ({pct}%)")

    return "\n".join(lines)


# ─── 主入口 ─────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="task-list: 任务列表管理",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    sub = parser.add_subparsers(dest="cmd")

    p_create = sub.add_parser("create", help="创建任务")
    p_create.add_argument("title", help="任务标题")
    p_create.add_argument("--priority", default="P1", help="优先级（P0/P1/P2/P3）")
    p_create.add_argument("--depends", type=lambda x: [int(d) for d in x.split(",") if d],
                         default=None, help="依赖的任务ID，逗号分隔")

    p_list = sub.add_parser("list", help="列举任务")
    p_list.add_argument("--status", default=None, help="按状态过滤（pending/in_progress/blocked/completed）")
    p_list.add_argument("--priority", default=None, help="按优先级过滤（P0/P1/P2/P3）")

    p_start = sub.add_parser("start", help="开始任务")
    p_start.add_argument("id", type=int, help="任务ID")

    p_done = sub.add_parser("done", help="完成任务")
    p_done.add_argument("id", type=int, help="任务ID")

    p_block = sub.add_parser("block", help="阻塞任务")
    p_block.add_argument("id", type=int, help="任务ID")
    p_block.add_argument("--by", type=lambda x: [int(d) for d in x.split(",") if d],
                         required=True, help="阻塞来源的任务ID")

    p_unblock = sub.add_parser("unblock", help="解除阻塞")
    p_unblock.add_argument("id", type=int, help="任务ID")

    p_delete = sub.add_parser("delete", help="删除任务")
    p_delete.add_argument("id", type=int, help="任务ID")

    sub.add_parser("tree", help="依赖树视图")
    sub.add_parser("stats", help="统计面板")

    args = parser.parse_args()

    if not args.cmd:
        print(cmd_list())
        return

    try:
        if args.cmd == "create":
            print(cmd_create(args.title, args.priority, args.depends))
        elif args.cmd == "list":
            print(cmd_list(args.status, args.priority))
        elif args.cmd == "start":
            print(cmd_start(args.id))
        elif args.cmd == "done":
            print(cmd_done(args.id))
        elif args.cmd == "block":
            print(cmd_block(args.id, args.by))
        elif args.cmd == "unblock":
            print(cmd_unblock(args.id))
        elif args.cmd == "delete":
            print(cmd_delete(args.id))
        elif args.cmd == "tree":
            print(cmd_tree())
        elif args.cmd == "stats":
            print(cmd_stats())
        else:
            parser.print_help()
    except Exception as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
