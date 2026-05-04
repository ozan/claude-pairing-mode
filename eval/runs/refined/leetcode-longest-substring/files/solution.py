def length_of_longest_substring(s: str) -> int:
    last_seen = {}
    left = 0
    best = 0
    for right, c in enumerate(s):
        if c in last_seen:
            left = max(left, last_seen[c] + 1)
        last_seen[c] = right
        best = max(best, right - left + 1)
    return best
