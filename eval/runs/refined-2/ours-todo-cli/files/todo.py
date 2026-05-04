#!/usr/bin/env python3
import argparse
import json
import os
import sys

DB_FILE = "todos.json"


def load():
    if not os.path.exists(DB_FILE):
        return {"next_id": 1, "todos": []}
    with open(DB_FILE) as f:
        return json.load(f)


def save(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


def cmd_add(text):
    data = load()
    todo = {"id": data["next_id"], "text": text, "done": False}
    data["todos"].append(todo)
    data["next_id"] += 1
    save(data)
    print(f"Added #{todo['id']}: {text}")


def cmd_list():
    data = load()
    if not data["todos"]:
        print("No todos yet.")
        return
    for t in data["todos"]:
        mark = "✓" if t["done"] else "○"
        print(f"  {mark} {t['id']:3d}  {t['text']}")


def cmd_done(id_):
    data = load()
    for t in data["todos"]:
        if t["id"] == id_:
            t["done"] = not t["done"]
            state = "done" if t["done"] else "undone"
            save(data)
            print(f"Marked #{id_} {state}.")
            return
    sys.exit(f"Error: no todo with id {id_}")


def cmd_rm(id_):
    data = load()
    before = len(data["todos"])
    data["todos"] = [t for t in data["todos"] if t["id"] != id_]
    if len(data["todos"]) == before:
        sys.exit(f"Error: no todo with id {id_}")
    save(data)
    print(f"Removed #{id_}.")


def main():
    p = argparse.ArgumentParser(prog="todo", description="Tiny todo list")
    sub = p.add_subparsers(dest="cmd", required=True)

    add_p = sub.add_parser("add", help="Add a new todo")
    add_p.add_argument("text", nargs="+", help="Todo text (no quotes needed)")

    sub.add_parser("list", help="List all todos")

    done_p = sub.add_parser("done", help="Mark a todo as done")
    done_p.add_argument("id", type=int)

    rm_p = sub.add_parser("rm", help="Remove a todo")
    rm_p.add_argument("id", type=int)

    args = p.parse_args()

    if args.cmd == "add":
        cmd_add(" ".join(args.text))
    elif args.cmd == "list":
        cmd_list()
    elif args.cmd == "done":
        cmd_done(args.id)
    elif args.cmd == "rm":
        cmd_rm(args.id)


if __name__ == "__main__":
    main()
