# ours-todo-cli

- Source: `ours`
- Difficulty: `medium`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T02:57:32.565Z

---

## Turn 1

**User:**

Let's build a tiny todo-list CLI in Python. Subcommands: add <text>, list, done <id>, rm <id>. Persist to a JSON file in the cwd.

**Pair:**

Thinking: The user wants to build a todo-list CLI in Python with subcommands: add <text>, list, done <id>, rm <id>, persisting to a JSON file. Let me start with a foundational design decision to present via the propose_options tool.
  
  Let me think about the first key design decision. A good one would be how to structure the data in the JSON file. Or maybe how to handle the CLI argument parsing. Let me think about what's most instructive...
  
  A good first question could be about how to structure the CLI parsing - using `argparse` vs `sys.argv` directly. 
  
  But `argparse` is clearly better for this use case, so that's not that interesting. The more interesting question is how to structure the JSON data itself. I could ask whether to store todos as a flat list of objects with IDs, or as a dictionary keyed by ID. The list approach is simpler but creates issues when deleting items—you either have to reassign IDs or search through the entire list to find by ID. A dictionary makes lookups instant but feels less natural for a sequence of todos.
  
  Actually, I think the ID generation strategy is the real teaching moment here. If I go with a list and use sequential integers, what happens when I delete an item? Do I renumber everything, or leave gaps? A dictionary keyed by ID sidesteps this problem entirely, making it the better choice for an app where you're constantly looking up and deleting by ID. If yes, that's confusing. If no, we have gaps.
  
  Using a dict keyed by string ID lets us handle gaps naturally without confusing the user. That's my preference, but for a simple todo app, a list with stored IDs works fine too. The real question is whether to use a list of dicts or dict of dicts as the storage format.
  
  Option A (my preference): `{"next_id": 3, "todos": {"1": {"text": "...", "done": false}, "2": {...}}}` - deletion is clean and IDs never get reused. Option B (distractor): `[{"id": 1, "text": "...", "done": false}, ...]` - feels more natural but done/remove operations need linear search, and if you delete by index the IDs become misleading. Both approaches are effectively O(n) for lookup on a small list, but the dict approach handles deletions without any renumbering issues. Let me present this as the first decision and create the file after we settle on it. I'm settling on the storage format as the first structural decision to teach. I'll compare a simple list-of-dicts approach against a dict with a counter and keyed items—the second option is better because deletion becomes O(1) and IDs stay stable without gaps or collisions. I'm calling the propose_options tool to present these two approaches to the user and get their feedback on which direction to take.

Assistant: Let's kick off with the most consequential structural choice — how to store todos in the JSON file.

OPTIONS:
[A] List of objects
```diff
+++ todo.json
@@ -0,0 +1,6 @@
+[
+  {"id": 1, "text": "buy milk", "done": false},
+  {"id": 2, "text": "call dentist", "done": false}
+]
```
New ID = `max(item["id"] for item in todos) + 1` (or 1 if empty).

[B] Dict keyed by ID
```diff
+++ todo.json
@@ -0,0 +1,8 @@
+{
+  "next_id": 3,
+  "items": {
+    "1": {"text": "buy milk", "done": false},
+    "2": {"text": "call dentist", "done": false}
+  }
+}
```
New ID = `next_id`, then increment and save.

(Reply with A or B, or ask a follow-up question.)

Thinking: The tool isn't available. Let me just proceed with presenting the options in text form and asking the user to choose.

Assistant: The `mcp__pairing__propose_options` tool isn't available in this session, so I'll present the options directly.

**First design decision: JSON storage format**

---

**Option A — List of objects**
```json
[
  {"id": 1, "text": "buy milk", "done": false},
  {"id": 2, "text": "call dentist", "done": false}
]
```
New ID = `max(item["id"] for item in todos) + 1` (or 1 if empty).

---

**Option B — Dict keyed by ID**
```json
{
  "next_id": 3,
  "items": {
    "1": {"text": "buy milk", "done": false},
    "2": {"text": "call dentist", "done": false}
  }
}
```
New ID = `next_id`, then increment and save.

---

Which do you prefer, A or B?

---

## Turn 2

**User:**

I think I'd go with **Option B** — dict keyed by ID.

Here's my reasoning: We're going to be looking up todos by ID a lot (when we run `done <id>` or `rm <id>`). With Option A, that's a loop through the whole list every time. With Option B, it's just a direct dict lookup, which feels cleaner. 

Also, I like that Option B manages the next ID explicitly — there's no risk of gaps or having to scan the list to figure out what the max ID is.

Option A *feels* more natural (it's literally a list), but I think the repeated ID lookups will make Option B less annoying to code up.

Ready to start building once you agree, or should I reconsider?

**Pair:**

Thinking: The user picked Option B, which is my preference. I'll agree and start building. Let me create the initial file structure. First, let me check if the file already exists.

Assistant: Exactly right on all counts. The `max()+1` approach also has a subtle bug you didn't mention: delete the highest-ID item, add a new one — it gets the same ID as something that existed before. The explicit counter sidesteps that entirely.

Let's build it. I'll start with the skeleton — file I/O + `add` — then we'll layer in the rest.

[Glob(todo.py)]
  No files found

[Write(todo.py)]
#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

DB = Path("todos.json")


def load() -> dict:
    if DB.exists():
        return json.loads(DB.read_text())
… (66 more lines)

Assistant: Let's do a quick smoke test:

[Bash(python3 todo.py add "buy milk" && python3 todo.py add "call dentist" && python3 todo.py list && python3 todo.py done 1 && python3 todo.py list && python3 todo.py rm 2 && python3 todo.py list)]
  Added #1: buy milk
  Added #2: call dentist
    ○ #1  buy milk
    ○ #2  call dentist
  Marked #1 done.
    ✓ #1  buy milk
    ○ #2  call dentist
  Removed #2: call dentist
    ✓ #1  buy milk

Assistant: All four subcommands work. A few things worth noting in the code:

- **Dispatch table** (`{"add": cmd_add, ...}[args.cmd](args, db)`) — cleaner than a chain of `if/elif`, and it'll raise `KeyError` automatically if a new subcommand is added but not wired up.
- **`str(args.id)`** — argparse gives us an `int` for `id`, but the JSON dict keys are strings, so we coerce once at the top of each handler.
- **`sys.exit(message)`** — prints to stderr and exits with code 1; the right tool for user-facing CLI errors.

Want to add anything — priorities, due dates, filtering `list` by status, colors?

---

## Turn 3

**User:**

I think we're good! We nailed the original spec — all four subcommands work, the JSON persistence is solid, and the code is clean. I appreciate the offer to add priorities or due dates, but I want to stay focused on the problem we started with. This feels complete.

One thing I did want to understand though — why the dispatch table instead of `if/elif`? Is it just style, or does it catch bugs in a way `if/elif` wouldn't?

**Pair:**

Thinking: The user is asking about the dispatch table vs if/elif. This is a great teaching moment. Let me explain clearly and concisely.
  
  The key differences:
  1. **Exhaustiveness checking**: With if/elif, if you add a new subcommand to argparse but forget to add the elif branch, it silently does nothing (falls through). With a dispatch table, it raises a KeyError immediately — fail-fast behavior.
  2. **Style/DRY**: The dict makes it visually obvious that every subcommand maps to exactly one handler. With if/elif, you could accidentally have duplicate branches or miss one.
  3. **Open/closed**: Adding a new command is one line in the dict vs adding an elif branch somewhere else in the code.
  
  
  4. **Real-world catch**: The dispatch table catches the specific bug where you add a new subparser but forget to add its handler — that's a KeyError at runtime, whereas if/elif silently falls through without an else clause.

Assistant: Mostly style, but there's one real bug it catches.

With `if/elif` and no `else`:

```python
if args.cmd == "add":
    cmd_add(args, db)
elif args.cmd == "list":
    cmd_list(args, db)
# ... someone adds "done" to argparse but forgets the elif ...
```

If you add a new subparser to `argparse` but forget the matching `elif`, the command silently does nothing — no error, no output. That's the worst kind of bug.

With the dispatch table, the same mistake raises a `KeyError` immediately:

```python
{"add": cmd_add, "list": cmd_list}[args.cmd](args, db)
#                                   ^^^^^^^^^^ KeyError: 'done'
```

It's a **fail-fast** pattern. The dict enforces a 1-to-1 relationship between registered subcommands and handlers — if you add one without the other, you find out right away.

In a 4-subcommand script the stakes are low, but the habit matters. The same pattern at scale (a CLI with 20 subcommands, split across modules) is the difference between a silent no-op and an immediate crash pointing you straight at the gap.

---

## Turn 4 (final)

**User:**

That makes total sense — fail-fast is much better than silent no-op. I'll remember that pattern. It's the kind of thing that seems like overkill for a tiny script, but building the habit early means I won't have to debug weird silent failures later when things get bigger.

Thanks for walking through this. The todo CLI works, I understand the storage choice and the dispatch pattern — that's everything I needed.

<done/>

---

**Run end**: done after 3 turns (419s)
