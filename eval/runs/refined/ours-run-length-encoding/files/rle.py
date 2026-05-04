from itertools import groupby
import re


def encode(s):
    return "".join(f"{ch}{sum(1 for _ in g)}" for ch, g in groupby(s))


def decode(s):
    return "".join(ch * int(n) for ch, n in re.findall(r'([a-zA-Z])(\d+)', s))


assert encode("aaabbc") == "a3b2c1"
assert encode("hello") == "h1e1l2o1"
assert decode("a3b2c1") == "aaabbc"

for s in ["aaabbc", "hello", "aaa", "a", ""]:
    assert decode(encode(s)) == s
print("All tests passed.")
