class Node:
    def __init__(self, key: int = 0, val: int = 0):
        self.key = key
        self.val = val
        self.prev: "Node | None" = None
        self.next: "Node | None" = None


class LRUCache:
    """
    LRU cache with O(1) get and put.

    Layout (most-recent → least-recent):
        head <-> [MRU node] <-> ... <-> [LRU node] <-> tail
    """

    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache: dict[int, Node] = {}

        # Sentinel nodes — never hold real data, eliminate edge cases
        self.head = Node()  # MRU side
        self.tail = Node()  # LRU side
        self.head.next = self.tail
        self.tail.prev = self.head

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _remove(self, node: Node) -> None:
        """Detach node from wherever it currently sits in the list."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _push_front(self, node: Node) -> None:
        """Insert node right after head (MRU position)."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._push_front(node)
        return node.val

    def put(self, key: int, val: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.val = val
            self._remove(node)
            self._push_front(node)
        else:
            node = Node(key, val)
            self.cache[key] = node
            self._push_front(node)
            if len(self.cache) > self.cap:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]
