# ours-lru-cache

- Condition: `learning`
- Tutor: `claude-sonnet-4-6` / Student: `claude-haiku-4-5-20251001`
- Started: 2026-05-04T21:08:49

## Initial prompt

Let's implement an LRU cache class in Python with `get(key)` and `put(key, value)` both O(1). Configurable capacity; evict least-recently-used on overflow.

---

## Turn 1

### Tutor

Tutor: ## LRU Cache in Python

The trick is pairing two data structures:
- **`dict`** → O(1) key lookups
- **Doubly linked list** → O(1) move-to-front and evict-from-tail

The dict maps each key to its **node in the list**, so every operation is a pointer shuffle — no searching.

[Write(/repo/lru_cache.py)]
"""
LRU Cache — O(1) get and put via dict + doubly linked list.

Layout (most-recent → least-recent):
    [head] ↔ [node A] ↔ [node B] ↔ ... ↔ [tail]

Sentinels (head/tail) eliminate every edge-case null-check.
"""

from __future__ import annotations


… (128 more lines)
  error: EROFS: read-only file system, mkdir '/repo'

[Write(/tmp/lru_cache.py)]
"""
LRU Cache — O(1) get and put via dict + doubly linked list.

Layout (most-recent → least-recent):
    [head] ↔ [node A] ↔ [node B] ↔ ... ↔ [tail]

Sentinels (head/tail) eliminate every edge-case null-check.
"""

from __future__ import annotations


… (128 more lines)
  error: <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>

[Bash(cat -n /tmp/lru_cache.py 2>/dev/null || echo "FILE_NOT_FOUND")]
  1	"""
       2	LRU Cache — O(1) get and put.
       3	
       4	Strategy
       5	--------
       6	- dict          : key → Node          (O(1) lookup / membership)
       7	- doubly-linked : Most-Recently-Used … Least-Recently-Used
       8	                  (O(1) move-to-front and evict-from-tail)
       9	
      10	Two sentinel nodes (head / tail) mean we never have to
      11	special-case an empty list or a single element.
      12	
  … (206 more lines)

Tutor: The file already exists — let me run it to check what passes, then update it with the full implementation:

[Bash(python /tmp/lru_cache.py)]
  PASS  basic eviction
  PASS  update refreshes recency
  PASS  capacity-1 edge case
  PASS  __contains__
  PASS  __len__
  PASS  repr  → LRUCache(cap=3, ['a':1, 'c':3, 'b':2])
  
  All tests passed ✓

Tutor: All 6 tests pass. Now let me replace it with the definitive, annotated version:

[Read(/tmp/lru_cache.py)]
  1	"""
  2	LRU Cache — O(1) get and put.
  3	
  4	Strategy
  5	--------
  6	- dict          : key → Node          (O(1) lookup / membership)
  7	- doubly-linked : Most-Recently-Used … Least-Recently-Used
  8	                  (O(1) move-to-front and evict-from-tail)
  9	
  10	Two sentinel nodes (head / tail) mean we never have to
  11	special-case an empty list or a single element.
  12	
  … (207 more lines)

Tutor: All 6 tests pass on the existing file. Here's the complete implementation with a walkthrough of every design decision:

---

## The code

```python
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


class _Node:
    """Doubly-linked list node that also carries the cache key/value."""
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: object, value: object) -> None:
        self.key   = key
        self.value = value
        self.prev: _Node | None = None
        self.next: _Node | None = None


class LRUCache:
    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError(f"capacity must be >= 1, got {capacity}")

        self.capacity = capacity
        self._map: dict[object, _Node] = {}

        # Sentinels — never evicted, never in _map.
        self._head = _Node(None, None)   # ← MRU sentinel
        self._tail = _Node(None, None)   # ← LRU sentinel
        self._head.next = self._tail
        self._tail.prev = self._head

    # ── Public API ──────────────────────────────────────────────────────

    def get(self, key: object) -> object:
        """Return cached value (or -1), promote to MRU.  O(1)."""
        node = self._map.get(key)
        if node is None:
            return -1
        self._move_to_front(node)
        return node.value

    def put(self, key: object, value: object) -> None:
        """Insert/update key→value as MRU; evict LRU if over capacity.  O(1)."""
        node = self._map.get(key)
        if node is not None:
            node.value = value          # update in-place
            self._move_to_front(node)
        else:
            node = _Node(key, value)
            self._map[key] = node
            self._insert_front(node)
            if len(self._map) > self.capacity:
                self._evict_lru()

    # ── Dunder helpers ───────────────────────────────────────────────────

    def __len__(self)           -> int:  return len(self._map)
    def __contains__(self, key) -> bool: return key in self._map
    def __repr__(self)          -> str:
        pairs, node = [], self._head.next
        while node is not self._tail:
            pairs.append(f"{node.key!r}:{node.value!r}")
            node = node.next
        return f"LRUCache(cap={self.capacity}, [{', '.join(pairs)}])"

    # ── Private list helpers — all O(1) ──────────────────────────────────

    def _remove(self, node: _Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_front(self, node: _Node) -> None:
        node.next            = self._head.next
        node.prev            = self._head
        self._head.next.prev = node
        self._head.next      = node

    def _move_to_front(self, node: _Node) -> None:
        self._remove(node)
        self._insert_front(node)

    def _evict_lru(self) -> None:
        lru = self._tail.prev
        self._remove(lru)
        del self._map[lru.key]
```

---

## How it achieves O(1)

Two structures work in tandem — each one covering the other's weakness:

| Structure | What it gives you |
|---|---|
| `dict` (`_map`) | O(1) lookup: `key → node` pointer |
| Doubly linked list | O(1) reorder: splice a node out and re-insert at front |

Neither structure alone is enough. A plain `dict` can't evict efficiently (you'd have to scan for the LRU). A plain linked list can't look up by key in O(1). Together they cover both.

---

## The sentinel trick

```
_head  ↔  [node A]  ↔  [node B]  ↔  _tail
  ↑ MRU end                  LRU end ↑
```

`_head` and `_tail` are **dummy nodes** that are never evicted and never stored in `_map`. The benefit: every real node always has a `prev` and a `next`, so `_remove` and `_insert_front` never need `if node.prev is None` guards. The code is the same for a 1-element list as a 100-element list.

---

## Walk through a key sequence

```
LRUCache(2)

put(1, "a")  →  head ↔ [1] ↔ tail
put(2, "b")  →  head ↔ [2] ↔ [1] ↔ tail
get(1)       →  head ↔ [1] ↔ [2] ↔ tail   (1 promoted to MRU)
put(3, "c")  →  head ↔ [3] ↔ [1] ↔ tail   (2 was LRU → evicted)
get(2)       →  returns -1
```

---

## `put` for an existing key

```python
node = self._map.get(key)
if node is not None:
    node.value = value          # ← update the value in-place
    self._move_to_front(node)   # ← reset recency
```

An update counts as a "use", so it must also move the node to front. The node is already in `_map`, so no dict change is needed — just a pointer shuffle in the list.

---

## `_evict_lru` stores the key in the node for a reason

```python
def _evict_lru(self) -> None:
    lru = self._tail.prev   # cheapest node to reach: just one pointer hop
    self._remove(lru)
    del self._map[lru.key]  # ← need the key to clean up the dict
```

Nodes store their own `key` precisely so eviction can do `del self._map[lru.key]` without an extra lookup. If the node only stored `value`, eviction would require a reverse search.

### Student

Thanks for walking through this! I can see how the two data structures complement each other — the dict gives us instant key lookup, and the linked list gives us instant reordering. The sentinels are clever too; they really do eliminate all the edge cases.

A couple of questions to make sure I understand:

1. **In `_move_to_front`, why do we call `_remove` first instead of just adjusting the pointers directly?** I know they're both O(1), but is it just for code clarity/reuse, or is there a reason to fully disconnect the node before reinserting it?

2. **When we do `get(key)`, we return -1 if the key isn't found.** Is that a convention for this problem, or would it be more Pythonic to raise a `KeyError` or return `None`? I'm wondering if there's a tradeoff I should know about.

3. **One last thing — in the repr, we walk the list from head to tail. Does that mean the repr always shows items in MRU-to-LRU order?** Just want to confirm that's intentional for debugging/understanding the cache state.

---

## Turn 2

### Tutor

Tutor: Great questions — each one touches a real design decision, not just an implementation detail.

---

## 1. Why `_remove` then `_insert_front` instead of inline pointer adjustment?

The decomposition isn't just cosmetic — it prevents a class of **pointer-clobbering bugs**.

When you manipulate linked-list pointers in-place, the order of assignments matters, and it's easy to overwrite a pointer you still need. Doing it as two clean phases sidesteps that entirely:

```
After _remove(node):                 After _insert_front(node):

  [prev] ↔ [next]                      [head] ↔ [node] ↔ [prev] ↔ [next]
   node still holds stale
   .prev / .next, but nobody
   points *back* to node anymore.
```

`_remove` leaves the node in a "dangling" state — its own `prev`/`next` still point at old neighbors, but those neighbors skip over it. That's fine because `_insert_front` overwrites all of node's pointers immediately anyway. Each helper operates on a **consistent intermediate state**.

The alternative — adjusting all 6 pointers inline — would look like this (fragile):

```python
# Danger zone: save old neighbors before any assignment
old_prev, old_next = node.prev, node.next
old_prev.next = old_next          # bypass node from behind
old_next.prev = old_prev          # bypass node from front
node.next = self._head.next       # start rewiring ...
...                               # if you misordered any line above,
                                  # you silently corrupt the list
```

A special case makes this worse: if `node` is **already at the front** (`node.prev is self._head`), an inline approach has to not do redundant work, or it risks writing `self._head.next = self._head.next` in the middle of other changes. The two-helper version handles that case for free — `_remove` + `_insert_front` is idempotent regardless of where the node currently lives.

> **The rule of thumb:** when an operation is naturally "undo one thing, then do another," decompose it that way. Each piece is independently testable and leaves the structure in a known state.

---

## 2. Return -1, raise `KeyError`, or return `None`?

The `-1` sentinel comes directly from [LeetCode #146](https://leetcode.com/problems/lru-cache/), which constrains keys and values to positive integers. In that narrow problem definition it works fine. In any real-world cache it's a design smell:

| Return style | When it's correct | When it breaks |
|---|---|---|
| `return -1` | Values are always positive ints | `-1` is a valid cache value |
| `return None` | `None` is never a valid value | `None` is a valid value |
| `raise KeyError(key)` | Always correct | Caller must use `try/except` |
| `return default` (configurable) | Always correct | Slightly more API surface |

The most Pythonic design mirrors `dict`'s own split API:

```python
def __getitem__(self, key):        # raises KeyError on miss
    node = self._map.get(key)
    if node is None:
        raise KeyError(key)
    self._move_to_front(node)
    return node.value

def get(self, key, default=None):  # returns default on miss
    node = self._map.get(key)
    if node is None:
        return default
    self._move_to_front(node)
    return node.value
```

This way callers choose their contract:
```python
cache["x"]               # raises KeyError if missing — "I know it's there"
cache.get("x")           # returns None  — "maybe it's there"
cache.get("x", 0)        # returns 0     — "give me a fallback"
```

> **The tradeoff in one sentence:** `-1` is fine for interview problems with integer constraints; for production code, `KeyError` + optional `get(key, default)` is safer because it can't silently return a value that looks real.

---

## 3. Does `__repr__` always show MRU → LRU?

Yes, intentionally. The walk starts at `self._head.next` (the node inserted/accessed most recently) and follows `.next` pointers toward `self._tail`:

```
_head  ↔  [most recent]  ↔  ...  ↔  [least recent]  ↔  _tail
          ↑ head.next                  ↑ tail.prev
          walk starts here             walk stops here
```

So the repr for a `put(1), put(2), put(3), get(1)` sequence looks like:

```
LRUCache(cap=3, [1:..., 3:..., 2:...])
                 ↑ MRU              ↑ LRU (next evicted)
```

That ordering is deliberate for debugging: the **leftmost item is the safest** (won't be evicted soon) and the **rightmost is the most vulnerable**. It directly mirrors the structure's internal state, which makes it easy to verify correctness by eye during a test or REPL session.

### Student

Thanks — that cleared things up a lot. I understand now why splitting the removal and insertion prevents pointer corruption, and the `dict`-style API with optional default makes much more sense than hardcoding `-1`.

Just to solidify my understanding: in the `_move_to_front` pattern, we're essentially saying "disconnect the node, then plug it back in at the front." The intermediate state where the node is dangling doesn't matter because we fully rewrite its pointers immediately after.

And I like the MRU-to-LRU repr ordering — it gives you a visual of what's "safe" vs what's about to be evicted. That's genuinely useful for debugging.

I think the implementation is solid and the design makes sense to me now. The only thing I'd want to do before considering this "done" is run through the test cases one more time to make sure they all still pass with our current code. Are the tests we saw earlier (`basic eviction`, `update refreshes recency`, etc.) still passing?

---

## Turn 3

### Tutor

[Bash(python /tmp/lru_cache.py)]
  PASS  basic eviction
  PASS  update refreshes recency
  PASS  capacity-1 edge case
  PASS  __contains__
  PASS  __len__
  PASS  repr  → LRUCache(cap=3, ['a':1, 'c':3, 'b':2])
  
  All tests passed ✓

Tutor: All 6 pass. Each one targets a distinct failure mode:

| Test | What it would catch if broken |
|---|---|
| `basic eviction` | Core LRU ordering — wrong node evicted |
| `update refreshes recency` | `put` on existing key not promoting to MRU |
| `capacity-1 edge case` | Off-by-one in eviction (evicting before or after the threshold) |
| `__contains__` | Membership check accidentally mutating recency order |
| `__len__` | Dict and list falling out of sync after eviction |
| `repr` | List pointer wiring — a corrupt list would produce wrong order |

The `repr` test is doing double duty: it's both a display check and a **structural integrity check**. If any `_remove` or `_insert_front` left a dangling pointer, the walk from `head` to `tail` would produce the wrong order (or loop forever). Seeing the correct MRU sequence in the output means the list topology is sound.

### Student

Perfect — that's exactly the reassurance I needed. Seeing all 6 tests pass, especially the `repr` test validating the list structure itself, means the implementation is working correctly end-to-end.

I feel confident about how this works now:
- The dict + linked list pairing handles both O(1) lookup and O(1) reordering
- The sentinel nodes eliminate edge cases
- The two-step `_remove` → `_insert_front` pattern prevents pointer corruption
- The test suite covers the key failure modes that would break an LRU cache

This was really helpful — I went from "why do we need two data structures?" to understanding the exact tradeoffs and design decisions behind each piece. Thanks for walking through the pointer safety issue and the API design choices; those are the kinds of things I wouldn't have thought to question on my own.

<done/>

---

**Run end:** done after 3 turn(s) in 141.1s
