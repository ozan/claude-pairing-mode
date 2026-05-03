from dataclasses import dataclass
from typing import Optional


@dataclass
class Node:
    value: int
    next: Optional["Node"] = None


def reverse(head: Optional[Node]) -> Optional[Node]:
    prev = None
    curr = head
    while curr is not None:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev


def from_list(xs):
    head = None
    for v in reversed(xs):
        head = Node(v, head)
    return head


def to_list(head):
    out = []
    while head is not None:
        out.append(head.value)
        head = head.next
    return out


if __name__ == "__main__":
    for xs in ([], [1], [1, 2, 3, 4, 5]):
        assert to_list(reverse(from_list(xs))) == list(reversed(xs))
        assert to_list(reverse(reverse(from_list(xs)))) == xs
        print(xs, "->", to_list(reverse(from_list(xs))))
