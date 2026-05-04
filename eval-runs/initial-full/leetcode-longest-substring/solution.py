def length_of_longest_substring(s: str) -> int:
    last_seen = {}  # char -> most recent index
    left = 0
    best = 0

    for right, char in enumerate(s):
        if char in last_seen:
            # Jump left past the previous occurrence,
            # but never move it backwards (stale index guard).
            left = max(left, last_seen[char] + 1)
        last_seen[char] = right
        best = max(best, right - left + 1)

    return best


# --- tests ---
# Classic LeetCode examples
assert length_of_longest_substring("abcabcbb") == 3   # "abc"
assert length_of_longest_substring("bbbbb")    == 1   # "b"
assert length_of_longest_substring("pwwkew")   == 3   # "wke"

# Edge cases
assert length_of_longest_substring("")         == 0   # empty string
assert length_of_longest_substring("a")        == 1   # single char
assert length_of_longest_substring("aa")       == 1   # immediate duplicate

# All unique
assert length_of_longest_substring("abcdef")   == 6   # whole string

# Stale-index guard cases
assert length_of_longest_substring("abba")     == 2   # "ab" or "ba"
assert length_of_longest_substring("dvdf")     == 3   # "vdf"
assert length_of_longest_substring("ababa")    == 2   # stale 'a' index trap

# Answer at the end, not the start
assert length_of_longest_substring("aab")      == 2   # "ab"
assert length_of_longest_substring("aabc")     == 3   # "abc"

# Non-alpha characters
assert length_of_longest_substring("a b c")    == 3   # "b c" or "a b" (with space)
assert length_of_longest_substring("123!123!")  == 4   # "123!"

print("All 14 tests passed.")
