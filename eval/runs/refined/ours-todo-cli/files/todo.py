import argparse
import json
import sys
from pathlib import Path

TODO_FILE = Path("todos.json")


def load() -> list:
    if TODO_FILE.exists():
        return json.loads(TODO_FILE.read_text())
    return []


def save(todos: list) -> None:
    tmp = TODO_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(todos, indent=2))
    tmp.replace(TODO_FILE)


def cmd_add(args) -> None:
    todos = load()
    next_id = max((t["id"] for t in todos), default=0) + 1
    todos.append({"id": next_id, "text": " ".join(args.text), "done": False})
    save(todos)
    print(f"Added #{next_id}")


def cmd_list(args) -> None:
    todos = load()
    if not todos:
        print("No todos.")
        return
    for t in todos:
        mark = "✓" if t["done"] else " "
        print(f"[{mark}] {t['id']}. {t['text']}")


def cmd_done(args) -> None:
    todos = load()
    for t in todos:
        if t["id"] == args.id:
            t["done"] = True
            save(todos)
            print(f"Marked #{args.id} done.")
            return
    print(f"No todo with id {args.id}.", file=sys.stderr)
    sys.exit(1)


def cmd_rm(args) -> None:
    todos = load()
    new_todos = [t for t in todos if t["id"] != args.id]
    if len(new_todos) == len(todos):
        print(f"No todo with id {args.id}.", file=sys.stderr)
        sys.exit(1)
    save(new_todos)
    print(f"Removed #{args.id}.")


def main() -> None:
    parser = argparse.ArgumentParser(prog="todo", description="A tiny todo CLI.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Add a new todo")
    p_add.add_argument("text", nargs="+", help="Todo text")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List all todos")
    p_list.set_defaults(func=cmd_list)

    p_done = sub.add_parser("done", help="Mark a todo as done")
    p_done.add_argument("id", type=int, help="Todo ID")
    p_done.set_defaults(func=cmd_done)

    p_rm = sub.add_parser("rm", help="Remove a todo")
    p_rm.add_argument("id", type=int, help="Todo ID")
    p_rm.set_defaults(func=cmd_rm)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
