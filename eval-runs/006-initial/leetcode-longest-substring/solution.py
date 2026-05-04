def length_of_longest_substring(s: str) -> int:
    seen = {}
    left = 0
    max_len = 0
    for right, char in enumerate(s):
        if char in seen:
            left = max(left, seen[char] + 1)
        seen[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len
