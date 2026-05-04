#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

DB = Path("todo.json")


def load() -> dict:
    try:
        return json.loads(DB.read_text())
    except FileNotFoundError:
        return {"next_id": 1, "todos": []}


def save(data: dict) -> None:
    DB.write_text(json.dumps(data, indent=2))


def cmd_add(args, data):
    todo = {"id": data["next_id"], "text": args.text, "done": False}
    data["todos"].append(todo)
    data["next_id"] += 1
    save(data)
    print(f"Added #{todo['id']}: {todo['text']}")


def cmd_list(args, data):
    if not data["todos"]:
        print("No todos.")
        return
    for t in data["todos"]:
        status = "x" if t["done"] else " "
        print(f"  [{status}] #{t['id']}  {t['text']}")


def cmd_done(args, data):
    for t in data["todos"]:
        if t["id"] == args.id:
            t["done"] = True
            save(data)
            print(f"Marked #{t['id']} done.")
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
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Add a new todo")
    p_add.add_argument("text", nargs="+")

    sub.add_parser("list", help="List all todos")

    p_done = sub.add_parser("done", help="Mark a todo complete")
    p_done.add_argument("id", type=int)

    p_rm = sub.add_parser("rm", help="Remove a todo")
    p_rm.add_argument("id", type=int)

    args = parser.parse_args()
    # join multi-word add text
    if args.cmd == "add":
        args.text = " ".join(args.text)

    data = load()
    {"add": cmd_add, "list": cmd_list, "done": cmd_done, "rm": cmd_rm}[args.cmd](args, data)


if __name__ == "__main__":
    main()
