def length_of_longest_substring(s: str) -> int:
    last_seen = {}
    left = 0
    best = 0

    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)

    return best


# --- tests ---

def test_basic():
    assert length_of_longest_substring("abcabcbb") == 3   # "abc"
    assert length_of_longest_substring("bbbbb") == 1      # "b"
    assert length_of_longest_substring("pwwkew") == 3     # "wke"

def test_guard_matters():
    # "abba": when right hits 'a' again, last_seen['a']=0 is BEFORE left=2
    # without the >= left guard, left would jump back to 1 — wrong answer
    assert length_of_longest_substring("abba") == 2       # "ab" or "ba"

def test_edge():
    assert length_of_longest_substring("") == 0
    assert length_of_longest_substring("a") == 1
    assert length_of_longest_substring("au") == 2

if __name__ == "__main__":
    test_basic()
    test_guard_matters()
    test_edge()
    print("All tests passed.")
