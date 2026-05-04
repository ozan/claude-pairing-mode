# ours-lru-cache

- Source: `ours`
- Difficulty: `hard`
- Pair model: `claude-sonnet-4-6`
- User model: `claude-haiku-4-5-20251001`
- Started: 2026-05-03T10:43:28.952Z

---

## Turn 1

**User:**

Let's implement an LRU cache class in Python with `get(key)` and `put(key, value)` both O(1). Configurable capacity; evict least-recently-used on overflow.

**Pair:**

Assistant: Good problem — the key insight is which data structures give you O(1) for *both* operations. Let me ask about that first.

Assistant: The `propose_options` tool isn't wired up in this session, so I'll walk through the key decision and then build it.

**Core question worth thinking about:** why not `dict + collections.deque`? It's tempting — `deque` tracks order, seems natural. The problem: `deque.remove(item)` is **O(n)** because it scans linearly. Every `get()` would need to find-and-move the item, blowing up the complexity.

The correct pairing is **`dict` + doubly linked list**:
- `dict`: O(1) lookup by key → gets you directly to the node
- Doubly linked list: O(1) node removal/insertion anywhere (you already have the pointer)

Sentinel head/tail nodes simplify edge cases (no null checks). Let's build it:

[Glob(lru_cache.py)]
  No files found

[Write(lru_cache.py)]
class Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev: "Node | None" = None
        self.next: "Node | None" = None


class LRUCache:
    """
… (69 more lines)

Assistant: Let's verify it with a few cases:

[Bash(cd /Users/ozan/src/pair && python3 - <<'EOF'
from lru_cache import LRUCache

# Basic put/get
c = LRUCache(2)
c.put(1, 1); c.put(2, 2)
assert c.get(1) == 1          # cache: {2, 1}  (1 is now MRU)

# Overflow — 2 should be evicted (LRU), not 1
c.put(3, 3)
assert c.get(2) == -1         # evicted
assert c.get(1) == 1
assert c.get(3) == 3

# Update existing key
c.put(3, 99)
assert c.get(3) == 99

# Capacity 1 edge case
c2 = LRUCache(1)
c2.put(1, 10); c2.put(2, 20)
assert c2.get(1) == -1
assert c2.get(2) == 20

print("All assertions passed ✓")
EOF
)]
  error: Exit code 1

[Bash(python3 - <<'EOF'
import sys; sys.path.insert(0, '.')
from lru_cache import LRUCache

# Basic put/get
c = LRUCache(2)
c.put(1, 1); c.put(2, 2)
assert c.get(1) == 1          # cache: {2, 1}  (1 is now MRU)

# Overflow — 2 should be evicted (LRU), not 1
c.put(3, 3)
assert c.get(2) == -1         # evicted
assert c.get(1) == 1
assert c.get(3) == 3

# Update existing key
c.put(3, 99)
assert c.get(3) == 99

# Capacity 1 edge case
c2 = LRUCache(1)
c2.put(1, 10); c2.put(2, 20)
assert c2.get(1) == -1
assert c2.get(2) == 20

print("All assertions passed ✓")
EOF
)]
  All assertions passed ✓

Assistant: All green. A few things worth noting about the design:

**Why store `key` on the `Node`?**  
During eviction (`_evict_lru`) we need to `del self.cache[lru.key]`. If the node didn't carry its own key, we'd have no way to remove it from the dict in O(1) — we'd have to scan the whole dict. This is a common stumbling block.

**Why sentinel nodes?**  
Without them, `_insert_at_mru` and `_evict_lru` need `if self.head is None` / `if prev is None` guards everywhere. Sentinels mean every node always has a real `prev` and `next` — no special cases.

**`__slots__` on Node?**  
Small but meaningful: prevents arbitrary attribute addition and uses a fixed-size array instead of a per-instance `__dict__`, saving ~50–200 bytes per node in memory-heavy caches.

Want to extend this — e.g., add a TTL, make it thread-safe, or generalize the key/value types?

---

## Turn 2 (final)

**User:**

Perfect! All tests pass. Let me walk you through the **key insights** that make this O(1):

## Why This Works

**The critical pairing: dict + doubly-linked list**

```
dict          → O(1) lookup by key → get direct node reference
linked list   → O(1) node removal/insertion at any position (just update pointers)
```

**Why not `dict + deque`?**  
`deque.remove(item)` is O(n) — it scans linearly for the item. Every `get()` would be O(n).

## Design Details Worth Learning

1. **Why store `key` on the Node?**  
   In `_evict_lru()`, we need `del self.cache[lru.key]`. Without the key on the node, we'd have no O(1) way to remove it from the dict.

2. **Why sentinel head/tail nodes?**  
   Every real node always has a `.prev` and `.next`. No null checks needed. Compare this to a naked list where you'd need `if node.prev is None` guards everywhere — sentinels make the code cleaner and bug-free.

3. **`__slots__` on Node?**  
   Prevents accidental attributes and uses fixed-size storage instead of per-instance `__dict__`. In a cache with millions of entries, this saves real memory.

4. **The `_move_to_mru()` pattern:**  
   Unlink, then re-insert. Both operations are O(1) pointer surgery because we already *have* the node reference (from the dict).

The implementation is done and tested. Ready to explore extensions — thread-safety, TTL per entry, or generalized key/value types?

<done/>

---

**Run end**: done after 1 turn (230s)
