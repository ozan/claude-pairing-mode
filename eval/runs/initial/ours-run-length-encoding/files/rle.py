import re
from itertools import groupby


def encode(s):
    return "".join(f"{k}{sum(1 for _ in g)}"
                   for k, g in groupby(s))


def decode(s):
    return "".join(ch * int(n)
                   for ch, n in re.findall(r"([A-Za-z])(\d+)", s))


if __name__ == "__main__":
    cases = ["aaabbc", "abcd", "aabbccdd", "zzz", ""]
    for s in cases:
        enc = encode(s)
        dec = decode(enc)
        status = "✓" if dec == s else "✗"
        print(f"{status}  {s!r:15} → {enc!r:15} → {dec!r}")
