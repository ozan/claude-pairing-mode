#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

DB = Path("todos.json")


def load() -> dict:
    if DB.exists():
        return json.loads(DB.read_text())
    return {"next_id": 1, "items": {}}


def save(db: dict) -> None:
    DB.write_text(json.dumps(db, indent=2))


def cmd_add(args, db):
    tid = str(db["next_id"])
    db["items"][tid] = {"text": args.text, "done": False}
    db["next_id"] += 1
    save(db)
    print(f"Added #{tid}: {args.text}")


def cmd_list(args, db):
    if not db["items"]:
        print("No todos.")
        return
    for tid, item in sorted(db["items"].items(), key=lambda x: int(x[0])):
        status = "✓" if item["done"] else "○"
        print(f"  {status} #{tid}  {item['text']}")


def cmd_done(args, db):
    tid = str(args.id)
    if tid not in db["items"]:
        sys.exit(f"No todo with id {tid}")
    db["items"][tid]["done"] = True
    save(db)
    print(f"Marked #{tid} done.")


def cmd_rm(args, db):
    tid = str(args.id)
    if tid not in db["items"]:
        sys.exit(f"No todo with id {tid}")
    text = db["items"].pop(tid)["text"]
    save(db)
    print(f"Removed #{tid}: {text}")


def main():
    parser = argparse.ArgumentParser(prog="todo")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Add a todo")
    p_add.add_argument("text", help="Todo text")

    sub.add_parser("list", help="List todos")

    p_done = sub.add_parser("done", help="Mark a todo done")
    p_done.add_argument("id", type=int)

    p_rm = sub.add_parser("rm", help="Remove a todo")
    p_rm.add_argument("id", type=int)

    args = parser.parse_args()
    db = load()

    {"add": cmd_add, "list": cmd_list, "done": cmd_done, "rm": cmd_rm}[args.cmd](args, db)


if __name__ == "__main__":
    main()
