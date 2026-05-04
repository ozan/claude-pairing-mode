from itertools import groupby
import re


def encode(s):
    return "".join(f"{ch}{sum(1 for _ in g)}" for ch, g in groupby(s))


def decode(s):
    return "".join(ch * int(n) for ch, n in re.findall(r"([a-zA-Z])(\d+)", s))


def test():
    cases = [
        "aaabbc",
        "abcd",           # no runs
        "aaaaaaaaaaaa",   # 12 a's — the multi-digit case
        "aabbccdd",
    ]
    for original in cases:
        encoded = encode(original)
        decoded = decode(encoded)
        status = "OK" if decoded == original else "FAIL"
        print(f"[{status}] {original!r:20s} -> {encoded!r:20s} -> {decoded!r}")


if __name__ == "__main__":
    test()
