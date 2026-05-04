#!/usr/bin/env python3
"""Tiny todo-list CLI. Persists to todos.json in the current directory."""

import argparse
import json
import sys
from pathlib import Path

DB = Path("todos.json")


# ── persistence ──────────────────────────────────────────────────────────────

def load() -> list[dict]:
    if DB.exists():
        return json.loads(DB.read_text())
    return []


def save(todos: list[dict]) -> None:
    DB.write_text(json.dumps(todos, indent=2))


# ── commands ──────────────────────────────────────────────────────────────────

def cmd_add(text: str) -> None:
    todos = load()
    next_id = max((t["id"] for t in todos), default=0) + 1
    todos.append({"id": next_id, "text": text, "done": False})
    save(todos)
    print(f"Added  #{next_id}: {text}")


def cmd_list() -> None:
    todos = load()
    if not todos:
        print("No todos yet. Add one with:  todo add <text>")
        return
    for t in todos:
        status = "✓" if t["done"] else "○"
        strike = "\x1b[9m" if t["done"] else ""  # strikethrough when done
        reset  = "\x1b[0m" if t["done"] else ""
        print(f"  {status}  [{t['id']:>3}]  {strike}{t['text']}{reset}")


def cmd_done(todo_id: int) -> None:
    todos = load()
    for t in todos:
        if t["id"] == todo_id:
            if t["done"]:
                print(f"#{todo_id} was already done.")
            else:
                t["done"] = True
                save(todos)
                print(f"Marked #{todo_id} as done: {t['text']}")
            return
    sys.exit(f"Error: no todo with id {todo_id}")


def cmd_rm(todo_id: int) -> None:
    todos = load()
    remaining = [t for t in todos if t["id"] != todo_id]
    if len(remaining) == len(todos):
        sys.exit(f"Error: no todo with id {todo_id}")
    removed = next(t for t in todos if t["id"] == todo_id)
    save(remaining)
    print(f"Removed #{todo_id}: {removed['text']}")


# ── CLI wiring ────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="todo",
        description="A tiny todo-list CLI.",
    )
    sub = parser.add_subparsers(dest="cmd", metavar="<command>")
    sub.required = True

    # add
    p_add = sub.add_parser("add", help="Add a new todo")
    p_add.add_argument("text", help="Todo text")

    # list
    sub.add_parser("list", help="List all todos")

    # done
    p_done = sub.add_parser("done", help="Mark a todo as done")
    p_done.add_argument("id", type=int, metavar="<id>")

    # rm
    p_rm = sub.add_parser("rm", help="Remove a todo")
    p_rm.add_argument("id", type=int, metavar="<id>")

    args = parser.parse_args()

    match args.cmd:
        case "add":  cmd_add(args.text)
        case "list": cmd_list()
        case "done": cmd_done(args.id)
        case "rm":   cmd_rm(args.id)


if __name__ == "__main__":
    main()
