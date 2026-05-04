class Node:
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map = {}           # key -> Node
        self.head = Node()      # LRU sentinel
        self.tail = Node()      # MRU sentinel
        self.head.next = self.tail
        self.tail.prev = self.head

    # --- linked-list primitives ---

    def _remove(self, node: Node) -> None:
        """Splice node out of the list."""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _push(self, node: Node) -> None:
        """Insert node just before tail (MRU position)."""
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    # --- public interface ---

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)
        self._push(node)
        return node.val

    def put(self, key: int, val: int) -> None:
        if key in self.map:
            node = self.map[key]
            node.val = val
            self._remove(node)
            self._push(node)
            return
        node = Node(key, val)
        self.map[key] = node
        self._push(node)
        if len(self.map) > self.cap:
            lru = self.head.next          # oldest node
            self._remove(lru)
            del self.map[lru.key]         # node stores key for exactly this
