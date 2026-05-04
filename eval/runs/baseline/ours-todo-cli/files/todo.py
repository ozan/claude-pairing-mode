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


def next_id(todos: list[dict]) -> int:
    return max((t["id"] for t in todos), default=0) + 1


# ── commands ──────────────────────────────────────────────────────────────────

def cmd_add(args: argparse.Namespace) -> None:
    todos = load()
    todo = {"id": next_id(todos), "text": args.text, "done": False}
    todos.append(todo)
    save(todos)
    print(f"Added  #{todo['id']}: {todo['text']}")


def cmd_list(args: argparse.Namespace) -> None:
    todos = load()
    if not todos:
        print("No todos yet. Use: todo add <text>")
        return
    for t in todos:
        status = "✓" if t["done"] else "○"
        strike = "\033[9m" if t["done"] else ""
        reset  = "\033[0m"  if t["done"] else ""
        print(f"  {status} {t['id']:>3}  {strike}{t['text']}{reset}")


def cmd_done(args: argparse.Namespace) -> None:
    todos = load()
    for t in todos:
        if t["id"] == args.id:
            if t["done"]:
                print(f"#{args.id} was already done.")
            else:
                t["done"] = True
                save(todos)
                print(f"Done   #{args.id}: {t['text']}")
            return
    sys.exit(f"Error: no todo with id {args.id}")


def cmd_rm(args: argparse.Namespace) -> None:
    todos = load()
    remaining = [t for t in todos if t["id"] != args.id]
    if len(remaining) == len(todos):
        sys.exit(f"Error: no todo with id {args.id}")
    removed = next(t for t in todos if t["id"] == args.id)
    save(remaining)
    print(f"Removed #{args.id}: {removed['text']}")


# ── CLI wiring ────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="todo",
        description="Tiny todo-list CLI (persists to todos.json)",
    )
    sub = p.add_subparsers(dest="cmd", metavar="<command>")
    sub.required = True

    # add
    p_add = sub.add_parser("add", help="Add a new todo")
    p_add.add_argument("text", help="Todo text")
    p_add.set_defaults(func=cmd_add)

    # list
    p_list = sub.add_parser("list", help="List all todos")
    p_list.set_defaults(func=cmd_list)

    # done
    p_done = sub.add_parser("done", help="Mark a todo as done")
    p_done.add_argument("id", type=int, help="Todo ID")
    p_done.set_defaults(func=cmd_done)

    # rm
    p_rm = sub.add_parser("rm", help="Remove a todo")
    p_rm.add_argument("id", type=int, help="Todo ID")
    p_rm.set_defaults(func=cmd_rm)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
