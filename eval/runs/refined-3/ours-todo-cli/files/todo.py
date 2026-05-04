#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

DB = Path("todos.json")


def load():
    if DB.exists():
        return json.loads(DB.read_text())
    return {"next_id": 1, "todos": []}


def save(data):
    DB.write_text(json.dumps(data, indent=2))


def cmd_add(args, data):
    todo = {"id": data["next_id"], "text": args.text, "done": False}
    data["todos"].append(todo)
    data["next_id"] += 1
    save(data)
    print(f"Added #{todo['id']}: {todo['text']}")


def cmd_list(args, data):
    todos = data["todos"]
    if not todos:
        print("No todos.")
        return
    for t in todos:
        status = "✓" if t["done"] else "·"
        print(f"  {status} [{t['id']}] {t['text']}")


def cmd_done(args, data):
    for t in data["todos"]:
        if t["id"] == args.id:
            t["done"] = True
            save(data)
            print(f"Marked #{args.id} done.")
            return
    print(f"No todo with id {args.id}.", file=sys.stderr)
    sys.exit(1)


def cmd_rm(args, data):
    before = len(data["todos"])
    data["todos"] = [t for t in data["todos"] if t["id"] != args.id]
    if len(data["todos"]) == before:
        print(f"No todo with id {args.id}.", file=sys.stderr)
        sys.exit(1)
    save(data)
    print(f"Removed #{args.id}.")


def main():
    parser = argparse.ArgumentParser(prog="todo", description="Tiny todo CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new todo")
    p_add.add_argument("text", help="Todo text")

    sub.add_parser("list", help="List all todos")

    p_done = sub.add_parser("done", help="Mark a todo as done")
    p_done.add_argument("id", type=int, help="Todo ID")

    p_rm = sub.add_parser("rm", help="Remove a todo")
    p_rm.add_argument("id", type=int, help="Todo ID")

    args = parser.parse_args()
    data = load()
    {"add": cmd_add, "list": cmd_list, "done": cmd_done, "rm": cmd_rm}[args.command](args, data)


if __name__ == "__main__":
    main()
