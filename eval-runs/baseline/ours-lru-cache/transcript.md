# ours-lru-cache

- Source: `ours`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:34:04.243Z

---

## Turn 1

**User:**

Let's implement an LRU cache class in Python with `get(key)` and `put(key, value)` both O(1). Configurable capacity; evict least-recently-used on overflow.

**Pair:**

Assistant: The classic solution combines a **hash map** (O(1) lookup) with a **doubly-linked list** (O(1) move-to-front / evict-tail). Here's a clean implementation:

[Write(/repo/lru_cache.py)]
from __future__ import annotations
from typing import Generic, Hashable, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class _Node(Generic[K, V]):
    """Doubly-linked list node that also carries the cache key/value."""

    __slots__ = ("key", "value", "prev", "next")

… (118 more lines)

[Bash(echo $HOME && ls ~)]
  /Users/oz
  Applications
  caesar_cipher.py
  Desktop
  dev
  Documents
  Downloads
  euler10.py
  evaluator.py
  exercism
  Library
  Movies
  … (6 more lines)

[Write(/Users/oz/lru_cache.py)]
from __future__ import annotations
from typing import Generic, Hashable, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class _Node(Generic[K, V]):
    """Doubly-linked list node that also carries the cache key/value."""

    __slots__ = ("key", "value", "prev", "next")

… (118 more lines)

Assistant: Now let's verify it works end-to-end:

[Bash(python3 - <<'EOF'
import sys
sys.path.insert(0, "/Users/oz")
from lru_cache import LRUCache

def check(condition, label):
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {label}")

print("=== basic get / put ===")
c = LRUCache(3)
c.put("a", 1); c.put("b", 2); c.put("c", 3)
check(c.get("a") == 1, "get existing key")
check(c.get("z") is None, "get missing key returns None")
check(len(c) == 3, "len == 3")
check("b" in c, "__contains__ hit")
check("z" not in c, "__contains__ miss")

print("\n=== eviction (LRU evicted) ===")
c = LRUCache(3)
c.put(1, "a"); c.put(2, "b"); c.put(3, "c")
# Access order now: 3(MRU) → 2 → 1(LRU)
_ = c.get(1)            # promotes 1  →  1(MRU), 3, 2(LRU)
c.put(4, "d")           # evicts 2
check(c.get(2) is None, "key 2 evicted")
check(c.get(1) == "a",  "key 1 still present")
check(c.get(3) == "c",  "key 3 still present")
check(c.get(4) == "d",  "key 4 just inserted")

print("\n=== update existing key ===")
c = LRUCache(2)
c.put("x", 10); c.put("y", 20)
c.put("x", 99)          # update – should NOT grow beyond capacity
check(len(c) == 2,      "no growth on update")
check(c.get("x") == 99, "updated value returned")
# x is now MRU, y is LRU; inserting z evicts y
c.put("z", 30)
check(c.get("y") is None, "y evicted after x was updated/promoted")
check(c.get("x") == 99,   "x still alive")

print("\n=== capacity = 1 ===")
c = LRUCache(1)
c.put("a", 1)
c.put("b", 2)
check(c.get("a") is None, "a evicted by b")
check(c.get("b") == 2,    "b present")

print("\n=== repr ===")
c = LRUCache(3)
c.put("p", 1); c.put("q", 2)
print(" ", repr(c))     # most-recent first

print("\n=== invalid capacity ===")
try:
    LRUCache(0)
    check(False, "should have raised")
except ValueError as e:
    check(True, f"ValueError raised: {e}")

print("\nAll checks done.")
EOF
)]
  === basic get / put ===
    [PASS] get existing key
    [PASS] get missing key returns None
    [PASS] len == 3
    [PASS] __contains__ hit
    [PASS] __contains__ miss
  
  === eviction (LRU evicted) ===
    [PASS] key 2 evicted
    [PASS] key 1 still present
    [PASS] key 3 still present
    [PASS] key 4 just inserted
  … (18 more lines)

Assistant: All 14 checks pass. Here's a walkthrough of the design:

---

## Design: HashMap + Doubly-Linked List

```
 head ←→ [most-recent] ←→ … ←→ [least-recent] ←→ tail
          ↑ always splice here          ↑ always evict here
```

Two sentinel nodes (`head` / `tail`) act as permanent bookends. They are never removed and never appear in the map, which means **every insert/delete path is branch-free** — no null checks for empty-list or single-element edge cases.

### Data structures

| Structure | Role | Why |
|---|---|---|
| `dict[K, _Node]` | key → node pointer | O(1) lookup |
| Doubly-linked list | recency ordering | O(1) unlink + relink anywhere |

### Operations

**`get(key)`** — O(1)
1. Dict lookup → if missing, return `None`.
2. Unlink node, splice it right after `head` (→ MRU position).
3. Return `node.value`.

**`put(key, value)`** — O(1)
- *Key exists:* update `node.value`, move to front (same as `get`).
- *Key is new:* if `len == capacity`, evict `tail.prev` (LRU) from both the list and the dict. Then create a new node and splice it at front.

### Why not `OrderedDict`?

Python's `collections.OrderedDict` *can* implement an LRU cache in ~5 lines (`move_to_end` + `popitem(last=False)`), and is perfectly valid in production. The explicit linked-list approach is used here because:
- It's the standard interview / CS-education version that proves O(1) complexity from first principles.
- It makes the recency ordering and eviction logic completely transparent.
- `OrderedDict` itself uses the same doubly-linked-list trick internally; this just makes it explicit.

---

## Turn 2 (final)

**User:**

Looking at this, I can see that the LRU cache has been **fully implemented and tested** — all 14 test checks pass! The solution uses the classic **HashMap + Doubly-Linked List** architecture:

1. **Hash map** (`dict`) for O(1) key lookup
2. **Doubly-linked list** for O(1) reordering (move-to-front on access, evict-tail on overflow)
3. **Sentinel head/tail nodes** to eliminate edge-case branches

Let me verify the implementation file exists and review it:Perfect! The implementation is **complete and correct**. The code demonstrates the classic LRU cache pattern with:

✅ **Core operations** (both O(1)):
- `get(key)` — lookup + move to front
- `put(key, value)` — insert or update + evict on overflow

✅ **Key design choices**:
- Sentinel nodes (`_head` / `_tail`) eliminate null-check branches
- Type-generic with `TypeVar` for flexibility
- `__slots__` on `_Node` for memory efficiency
- Separate `_move_to_front`, `_insert_at_front`, `_remove`, `_evict_lru` methods keep logic crisp

✅ **Test coverage**:
- Basic get/put ✓
- Eviction of LRU on overflow ✓
- Update of existing keys (no growth) ✓
- Edge case: capacity=1 ✓
- Error handling: invalid capacity ✓

The doubly-linked list with sentinels is a timeless approach—you've got a production-ready implementation that's also educational and transparent about its complexity.

<done/>

---

**Run end**: done after 1 turn (84s)
