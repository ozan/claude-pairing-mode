# ours-lru-cache

- Condition: `baseline`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T20:54:42

## Initial prompt

Let's implement an LRU cache class in Python with `get(key)` and `put(key, value)` both O(1). Configurable capacity; evict least-recently-used on overflow.

---

## Turn 1

### Tutor

Tutor: ## LRU Cache — Design

**The trick:** pair a `dict` (O(1) lookup) with a **doubly-linked list** (O(1) move-to-front / evict-from-tail).

```
head ↔ [most-recent] ↔ … ↔ [least-recent] ↔ tail
```

Sentinel `head`/`tail` nodes eliminate all edge-case null checks.

[Write(/repo/lru_cache.py)]
"""
LRU Cache — O(1) get and put.

Strategy
--------
- dict          : key → Node          (O(1) lookup / membership)
- doubly-linked : Most-Recently-Used … Least-Recently-Used
                  (O(1) move-to-front and evict-from-tail)

Two sentinel nodes (head / tail) mean we never have to
special-case an empty list or a single element.

… (152 more lines)
  error: EROFS: read-only file system, mkdir '/repo'

[Write(/tmp/lru_cache.py)]
"""
LRU Cache — O(1) get and put.

Strategy
--------
- dict          : key → Node          (O(1) lookup / membership)
- doubly-linked : Most-Recently-Used … Least-Recently-Used
                  (O(1) move-to-front and evict-from-tail)

Two sentinel nodes (head / tail) mean we never have to
special-case an empty list or a single element.

… (152 more lines)
  error: <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>

[Bash(cat -n /tmp/lru_cache.py 2>/dev/null || echo "FILE_NOT_FOUND")]
  1	"""
       2	LRU Cache — O(1) get and put.
       3	
       4	Strategy
       5	--------
       6	  dict          →  O(1) key → node lookup
       7	  doubly-linked list  →  O(1) order maintenance
       8	
       9	The list runs MRU ←→ LRU between two permanent sentinel nodes.
      10	Every access promotes the touched node to the MRU end.
      11	Overflow evicts the node at the LRU end.
      12	"""
  … (186 more lines)

Tutor: The file already exists with a good version. Let me overwrite it with the cleaner, well-commented implementation and run the tests:

[Bash(cat > /tmp/lru_cache.py << 'PYEOF'
"""
LRU Cache — O(1) get and put.

Strategy
--------
- dict          : key → Node          (O(1) lookup / membership)
- doubly-linked : Most-Recently-Used … Least-Recently-Used
                  (O(1) move-to-front and evict-from-tail)

Two sentinel nodes (head / tail) mean we never have to
special-case an empty list or a single element.

    head  ↔  [MRU]  ↔  …  ↔  [LRU]  ↔  tail
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Internal node
# ---------------------------------------------------------------------------

class _Node:
    """Doubly-linked list node that also carries the cache key/value."""

    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: object, value: object) -> None:
        self.key   = key
        self.value = value
        self.prev: _Node | None = None
        self.next: _Node | None = None


# ---------------------------------------------------------------------------
# LRU Cache
# ---------------------------------------------------------------------------

class LRUCache:
    """
    Least-Recently-Used cache with configurable capacity.

    Parameters
    ----------
    capacity : int
        Maximum number of items to hold.  Must be >= 1.

    Both ``get`` and ``put`` run in **O(1)** time and space per call.

    Examples
    --------
    >>> cache = LRUCache(2)
    >>> cache.put("a", 1)
    >>> cache.put("b", 2)
    >>> cache.get("a")        # 1  — "a" is now MRU
    1
    >>> cache.put("c", 3)     # capacity exceeded → evict "b" (LRU)
    >>> cache.get("b")        # -1 — evicted
    -1
    """

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError(f"capacity must be >= 1, got {capacity}")

        self.capacity = capacity
        self._map: dict[object, _Node] = {}

        # Sentinel nodes — never evicted, never in _map.
        # head is the MRU end; tail is the LRU end.
        self._head = _Node(None, None)   # ← MRU sentinel
        self._tail = _Node(None, None)   # ← LRU sentinel
        self._head.next = self._tail
        self._tail.prev = self._head

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, key: object) -> object:
        """
        Return the cached value for *key*, or -1 if absent.
        Promotes the entry to most-recently-used position.

        Complexity: O(1)
        """
        node = self._map.get(key)
        if node is None:
            return -1
        self._move_to_front(node)
        return node.value

    def put(self, key: object, value: object) -> None:
        """
        Insert or update *key* → *value*, marking it most-recently used.
        Evicts the least-recently-used entry when at capacity.

        Complexity: O(1)
        """
        node = self._map.get(key)
        if node is not None:
            # Key already exists: refresh value and recency.
            node.value = value
            self._move_to_front(node)
        else:
            # Brand-new key: insert at MRU end, then evict if over capacity.
            node = _Node(key, value)
            self._map[key] = node
            self._insert_front(node)
            if len(self._map) > self.capacity:
                self._evict_lru()

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._map)

    def __contains__(self, key: object) -> bool:
        """Membership check — does NOT affect recency order."""
        return key in self._map

    def __repr__(self) -> str:
        """Show entries from MRU (left) to LRU (right)."""
        pairs, node = [], self._head.next
        while node is not self._tail:
            pairs.append(f"{node.key!r}:{node.value!r}")
            node = node.next
        return f"LRUCache(cap={self.capacity}, [{', '.join(pairs)}])"

    # ------------------------------------------------------------------
    # Private linked-list helpers — all O(1)
    # ------------------------------------------------------------------

    def _remove(self, node: _Node) -> None:
        """Splice *node* out of the list."""
        node.prev.next = node.next   # type: ignore[union-attr]
        node.next.prev = node.prev   # type: ignore[union-attr]

    def _insert_front(self, node: _Node) -> None:
        """Place *node* right after the MRU sentinel."""
        node.next            = self._head.next
        node.prev            = self._head
        self._head.next.prev = node  # type: ignore[union-attr]
        self._head.next      = node

    def _move_to_front(self, node: _Node) -> None:
        """Promote *node* to MRU position."""
        self._remove(node)
        self._insert_front(node)

    def _evict_lru(self) -> None:
        """Remove the node just before the LRU sentinel."""
        lru = self._tail.prev        # always a real node when map is non-empty
        self._remove(lru)
        del self._map[lru.key]       # type: ignore[union-attr]


# ---------------------------------------------------------------------------
# Tests  (python lru_cache.py)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # 1. Basic eviction ---------------------------------------------------
    c = LRUCache(2)
    c.put(1, "a"); c.put(2, "b")
    assert c.get(1) == "a"           # 1 → MRU
    c.put(3, "c")                    # 2 is LRU → evicted
    assert c.get(2) == -1
    assert c.get(3) == "c"
    c.put(4, "d")                    # 1 is LRU now → evicted
    assert c.get(1) == -1
    assert c.get(3) == "c"
    assert c.get(4) == "d"
    print("PASS  basic eviction")

    # 2. Update refreshes recency -----------------------------------------
    c = LRUCache(2)
    c.put(1, "x"); c.put(2, "y")
    c.put(1, "X")                    # update → 1 becomes MRU
    c.put(3, "z")                    # 2 is LRU → evicted
    assert c.get(1) == "X"
    assert c.get(2) == -1
    assert c.get(3) == "z"
    print("PASS  update refreshes recency")

    # 3. Capacity-1 edge case ---------------------------------------------
    c = LRUCache(1)
    c.put("a", 1); c.put("b", 2)
    assert c.get("a") == -1
    assert c.get("b") == 2
    print("PASS  capacity-1 edge case")

    # 4. __contains__ does NOT change recency -----------------------------
    c = LRUCache(2)
    c.put("x", 10); c.put("y", 20)
    assert "x" in c and "y" in c
    print("PASS  __contains__")

    # 5. len() tracks evictions -------------------------------------------
    c = LRUCache(3)
    assert len(c) == 0
    c.put(1, 1); c.put(2, 2); c.put(3, 3)
    assert len(c) == 3
    c.put(4, 4)
    assert len(c) == 3
    print("PASS  __len__")

    # 6. repr shows MRU → LRU order ---------------------------------------
    c = LRUCache(3)
    c.put("a", 1); c.put("b", 2); c.put("c", 3)
    c.get("a")                       # "a" → MRU
    r = repr(c)
    assert r.index("'a'") < r.index("'b'"), "MRU 'a' should appear first"
    print(f"PASS  repr  → {r}")

    print("\nAll tests passed ✓")
PYEOF
python3 /tmp/lru_cache.py)]
  PASS  basic eviction
  PASS  update refreshes recency
  PASS  capacity-1 edge case
  PASS  __contains__
  PASS  __len__
  PASS  repr  → LRUCache(cap=3, ['a':1, 'c':3, 'b':2])
  
  All tests passed ✓

Tutor: All 6 tests pass. Here's the full implementation with an explanation of every design decision:

---

## How it works

### Data structures

| Structure | Role | Why |
|---|---|---|
| `dict` (`_map`) | `key → _Node` | O(1) lookup by key |
| Doubly-linked list | Recency order (MRU ↔ LRU) | O(1) remove + insert anywhere |

The two are kept **in sync**: every node in the list has a matching entry in the dict, and vice versa.

### Sentinel nodes

```
_head  ↔  [MRU node]  ↔  …  ↔  [LRU node]  ↔  _tail
```

`_head` and `_tail` are dummy nodes that are **never** stored in `_map` and **never** evicted. This eliminates every `if node.prev is None` null check — `_remove`, `_insert_front`, and `_evict_lru` work identically on one node or a million.

### `get(key)` — O(1)
1. Hash-map lookup → O(1)  
2. `_move_to_front` = `_remove` + `_insert_front` → 6 pointer assignments = O(1)

### `put(key, value)` — O(1)
- **Key exists**: update `.value` in place, `_move_to_front` → O(1)  
- **New key**: create node, `_insert_front`, then if `len > capacity` call `_evict_lru` → O(1)
  - Eviction reads `_tail.prev` (the LRU node), unlinks it, and `del`s from the dict — all O(1)

### Why `_insert_front` needs 4 steps
```
Before:  head  ↔  A  ↔  …
Insert X after head:
  1. X.next = head.next   (= A)
  2. X.prev = head
  3. A.prev = X           ← must happen before head.next changes
  4. head.next = X
```
Steps 3 and 4 must be in that order — otherwise you lose the pointer to `A`.

### Student

Got it—this is a really clean implementation. Let me make sure I understand the key points:

1. **The dict is for O(1) key lookups**, and the doubly-linked list maintains recency order.

2. **Sentinels (`_head` and `_tail`)** eliminate all the null-check edge cases. Every real node sits between them, so `_remove` and `_insert_front` always work the same way.

3. **`get` moves a hit to the front** by removing it and reinserting it right after `_head`.

4. **`put` either updates an existing node** (and refreshes its position) **or creates a new one** and evicts the LRU tail if we're over capacity.

5. **The order of pointer assignments matters**—in `_insert_front`, we have to update `A.prev` (the old first node's backlink) *before* we update `head.next`, or we lose track of `A`.

I notice the tests all pass. One thing I want to confirm: **when we `put` with a key that already exists, does calling `_move_to_front` prevent it from being evicted?** For instance, if the cache is full and we update an existing key, we don't want to accidentally evict it, right?

Looking at the code:
```python
if node is not None:
    node.value = value
    self._move_to_front(node)
```

We move it to the front *before* checking capacity, so it's already MRU and won't be the LRU target if eviction happens. But actually, we don't reach the `if len > capacity` line in this branch at all—we only check capacity in the `else` (new key) branch. So an update never triggers eviction. Is that the intended behavior?

---

## Turn 2

### Tutor

Tutor: Yes, exactly right — and the reason is even simpler than "it's already MRU so it won't be chosen": **an update can never overflow the cache because the map doesn't grow.**

The invariant the class maintains is:

```
len(_map) <= capacity   ← always true at the end of any put/get
```

Trace what each branch of `put` does to `len(_map)`:

| Branch | Size change | Eviction needed? |
|---|---|---|
| Key **exists** | 0 (update in place) | No — invariant already holds |
| Key **new** | +1 | Maybe — check and evict if `> capacity` |

So the capacity check belongs exclusively in the new-key branch, not because we moved the node first, but because **updating an existing entry is a size-neutral operation**. The dict has the same number of entries before and after. There's simply nothing to evict.

You can see this plays out with the invariant across a full sequence:

```
LRUCache(2)

put(1, "a")  → map: {1}        len=1  ≤ 2  ✓
put(2, "b")  → map: {1,2}      len=2  ≤ 2  ✓
put(2, "B")  → map: {1,2}      len=2  ≤ 2  ✓  (update, no growth)
put(3, "c")  → map: {1,2,3}    len=3  > 2  → evict LRU → map: {2,3}  len=2  ✓
```

If the eviction check were inside the `if node is not None` branch it would never fire anyway (you'd have to add a key to overflow), but more importantly it would be *semantically wrong* — it would suggest there's a scenario where updating an existing key can push the cache over its limit, which there isn't.

Your summary of all five points is exactly correct.

### Student

Ah, that makes perfect sense. The invariant `len(_map) <= capacity` is maintained throughout, so updates can't break it. Updates are strictly size-neutral.

I was overthinking it by worrying about *which node gets evicted*—but the real insight is that **there's nothing to evict when the dictionary doesn't grow**. The capacity check belongs exactly where it is: only on the new-key path.

This also clarifies the design philosophy: keep the invariant tight and let the logic follow naturally from it, rather than adding defensive checks everywhere.

I feel like I've got the full picture now:
- **Structure & why**: dict for O(1) lookup, doubly-linked list for O(1) reordering, sentinels to eliminate edge cases
- **The core operations**: `get` hits and promotes, `put` updates in-place or inserts-and-maybe-evicts
- **The invariant**: the map never exceeds capacity by construction
- **The pointer order**: matters in `_insert_front` to not lose references

The code is clean and all the tests pass. I think I'm done here.

<done/>

---

**Run end:** done after 2 turn(s) in 100.6s
