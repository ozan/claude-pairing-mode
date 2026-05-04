import re
from itertools import groupby


def encode(s):
    return "".join(
        f"{char}{sum(1 for _ in group)}"
        for char, group in groupby(s)
    )


def decode(s):
    return "".join(
        char * int(n)
        for char, n in re.findall(r"([a-zA-Z])(\d+)", s)
    )


if __name__ == "__main__":
    cases = ["aaabbc", "abcd", "aaaaaa", "", "a"]
    for s in cases:
        encoded = encode(s)
        decoded = decode(encoded)
        status = "✓" if decoded == s else "✗"
        print(f"{status} {s!r:12} → {encoded!r:14} → {decoded!r}")
