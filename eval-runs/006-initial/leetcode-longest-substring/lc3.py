def length_set(s: str) -> int:
    """Sliding window with a set. Left shrinks one step at a time — can't move backward."""
    chars = set()
    left = 0
    max_len = 0
    for right in range(len(s)):
        while s[right] in chars:
            chars.remove(s[left])
            left += 1
        chars.add(s[right])
        max_len = max(max_len, right - left + 1)
    return max_len


def length_dict(s: str) -> int:
    """Sliding window with a dict. Left jumps directly — needs max() guard to avoid going backward."""
    last_seen: dict[str, int] = {}
    left = 0
    max_len = 0
    for right in range(len(s)):
        if s[right] in last_seen:
            left = max(left, last_seen[s[right]] + 1)
        last_seen[s[right]] = right
        max_len = max(max_len, right - left + 1)
    return max_len


if __name__ == "__main__":
    cases = [
        ("abcabcbb", 3),   # classic
        ("bbbbb",    1),   # all same
        ("pwwkew",   3),   # wke
        ("abba",     2),   # trap: stale dict entry would move left backward
        ("",         0),   # empty
        ("a",        1),   # single char
        ("au",       2),   # two distinct
        ("dvdf",     3),   # vdf — left must not regress on second d
    ]

    for fn in (length_set, length_dict):
        print(f"\n{fn.__name__}:")
        for s, expected in cases:
            result = fn(s)
            status = "✓" if result == expected else f"✗ (got {result})"
            print(f"  {s!r:15} → {result}  {status}")
