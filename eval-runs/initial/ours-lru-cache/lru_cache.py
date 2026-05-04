class Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev: "Node | None" = None
        self.next: "Node | None" = None


class LRUCache:
    """
    O(1) get and put via dict + doubly linked list.

    Layout:  head (LRU end) <-> [nodes...] <-> tail (MRU end)
    Sentinels (head/tail) eliminate null-pointer edge cases.
    """

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self.cap = capacity
        self.cache: dict[int, Node] = {}   # key -> Node

        # Sentinel nodes — never evicted, never stored in cache dict
        self.head = Node()   # LRU end
        self.tail = Node()   # MRU end
        self.head.next = self.tail
        self.tail.prev = self.head

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def get(self, key: int) -> int:
        """Return value for key, or -1 if absent. Marks key as most-recently used."""
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._move_to_mru(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        """Insert or update key. Evicts LRU entry when over capacity."""
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._move_to_mru(node)
        else:
            node = Node(key, value)
            self.cache[key] = node
            self._insert_at_mru(node)
            if len(self.cache) > self.cap:
                self._evict_lru()

    # ------------------------------------------------------------------ #
    #  Internal helpers                                                    #
    # ------------------------------------------------------------------ #

    def _remove(self, node: Node) -> None:
        """Unlink node from wherever it sits in the list."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_at_mru(self, node: Node) -> None:
        """Insert node just before the tail sentinel (MRU position)."""
        prev = self.tail.prev
        prev.next = node
        node.prev = prev
        node.next = self.tail
        self.tail.prev = node

    def _move_to_mru(self, node: Node) -> None:
        self._remove(node)
        self._insert_at_mru(node)

    def _evict_lru(self) -> None:
        lru = self.head.next          # first real node = least recently used
        self._remove(lru)
        del self.cache[lru.key]       # key lives on the node — that's why we store it
