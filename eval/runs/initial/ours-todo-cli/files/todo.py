#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

DB = Path("todos.json")


def load():
    if DB.exists():
        return json.loads(DB.read_text())
    return []


def save(todos):
    DB.write_text(json.dumps(todos, indent=2))


def next_id(todos):
    return max((t["id"] for t in todos), default=0) + 1


def cmd_add(args):
    todos = load()
    todo = {"id": next_id(todos), "text": args.text, "done": False}
    todos.append(todo)
    save(todos)
    print(f"Added #{todo['id']}: {todo['text']}")


def cmd_list(args):
    todos = load()
    if not todos:
        print("No todos.")
        return
    for t in todos:
        status = "✓" if t["done"] else "○"
        print(f"  {status} [{t['id']}] {t['text']}")


def cmd_done(args):
    todos = load()
    for t in todos:
        if t["id"] == args.id:
            t["done"] = True
            save(todos)
            print(f"Done: [{t['id']}] {t['text']}")
            return
    print(f"No todo with id {args.id}.", file=sys.stderr)
    sys.exit(1)


def cmd_rm(args):
    todos = load()
    remaining = [t for t in todos if t["id"] != args.id]
    if len(remaining) == len(todos):
        print(f"No todo with id {args.id}.", file=sys.stderr)
        sys.exit(1)
    save(remaining)
    print(f"Removed #{args.id}.")


def main():
    parser = argparse.ArgumentParser(prog="todo", description="Tiny todo CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Add a new todo")
    p_add.add_argument("text", help="Todo text")

    sub.add_parser("list", help="List all todos")

    p_done = sub.add_parser("done", help="Mark a todo as done")
    p_done.add_argument("id", type=int, help="Todo ID")

    p_rm = sub.add_parser("rm", help="Remove a todo")
    p_rm.add_argument("id", type=int, help="Todo ID")

    args = parser.parse_args()
    {"add": cmd_add, "list": cmd_list, "done": cmd_done, "rm": cmd_rm}[args.cmd](args)


if __name__ == "__main__":
    main()
