#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

DB = Path("todos.json")


def load():
    if DB.exists():
        try:
            return json.loads(DB.read_text())
        except json.JSONDecodeError as e:
            print(f"Error: {DB} is corrupt ({e}).", file=sys.stderr)
            print("Fix or delete the file manually.", file=sys.stderr)
            sys.exit(1)
    return {"next_id": 1, "items": []}


def save(data):
    DB.write_text(json.dumps(data, indent=2))


def cmd_add(args, data):
    item = {"id": data["next_id"], "text": args.text, "done": False}
    data["items"].append(item)
    data["next_id"] += 1
    save(data)
    print(f"Added #{item['id']}: {item['text']}")


def cmd_list(args, data):
    if not data["items"]:
        print("No todos.")
        return
    for item in data["items"]:
        status = "✓" if item["done"] else "·"
        print(f"  {status} {item['id']:>3}  {item['text']}")


def cmd_done(args, data):
    for item in data["items"]:
        if item["id"] == args.id:
            item["done"] = True
            save(data)
            print(f"Done #{item['id']}: {item['text']}")
            return
    print(f"No item with id {args.id}", file=sys.stderr)
    sys.exit(1)


def cmd_rm(args, data):
    for i, item in enumerate(data["items"]):
        if item["id"] == args.id:
            data["items"].pop(i)
            save(data)
            print(f"Removed #{item['id']}: {item['text']}")
            return
    print(f"No item with id {args.id}", file=sys.stderr)
    sys.exit(1)


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
    data = load()

    if args.cmd == "add":
        cmd_add(args, data)
    elif args.cmd == "list":
        cmd_list(args, data)
    elif args.cmd == "done":
        cmd_done(args, data)
    elif args.cmd == "rm":
        cmd_rm(args, data)


if __name__ == "__main__":
    main()
