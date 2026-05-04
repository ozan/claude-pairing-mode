def length_of_longest_substring(s: str) -> int:
    seen = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in seen:
            left = max(left, seen[ch] + 1)
        seen[ch] = right
        best = max(best, right - left + 1)
    return best


if __name__ == "__main__":
    cases = [
        ("abcabcbb", 3),
        ("bbbbb", 1),
        ("pwwkew", 3),
        ("abba", 2),
        ("", 0),
    ]
    for s, expected in cases:
        result = length_of_longest_substring(s)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{s}' → {result} (expected {expected})")
