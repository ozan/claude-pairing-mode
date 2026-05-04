import re
from itertools import groupby


def encode(s: str) -> str:
    """'aaabbc' -> 'a3b2c1'"""
    # groupby yields (key, group_iter) for each run of identical chars.
    # list(group) consumes it eagerly — required before the next iteration.
    return "".join(f"{ch}{len(list(group))}" for ch, group in groupby(s))


def decode(s: str) -> str:
    """'a3b2c1' -> 'aaabbc'"""
    return "".join(ch * int(n) for ch, n in re.findall(r"(.)(\d+)", s))


# --- round-trip tests ---
if __name__ == "__main__":
    cases = [
        "aaabbc",
        "abcd",        # no repeats → each count is 1
        "aaaa",        # single run
        "",            # empty string
        "aabbaa",      # repeated groups
    ]

    all_ok = True
    for original in cases:
        encoded = encode(original)
        decoded = decode(encoded)
        ok = decoded == original
        all_ok = all_ok and ok
        print(f"{original!r:12} -> {encoded!r:16} -> {decoded!r:12}  {'✓' if ok else '✗ FAIL'}")

    print("\nAll round-trips passed." if all_ok else "\nSome tests FAILED.")
