import re
from itertools import groupby


def encode(s):
    return "".join(f"{k}{sum(1 for _ in g)}" for k, g in groupby(s))


def decode(s):
    return "".join(ch * int(n) for ch, n in re.findall(r"([a-zA-Z])(\d+)", s))


if __name__ == "__main__":
    # spot-checks
    assert encode("aaabbc") == "a3b2c1"
    assert decode("a3b2c1") == "aaabbc"
    assert encode("") == ""
    assert decode("") == ""
    # round-trips
    for s in ["aaabbc", "abc", "a", "", "a" * 10 + "bc"]:
        assert decode(encode(s)) == s, s
        enc = encode(s)
        assert encode(decode(enc)) == enc, enc
    print("all tests passed")
