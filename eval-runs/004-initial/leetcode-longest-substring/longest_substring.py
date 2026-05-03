def length_of_longest_substring(s: str) -> int:
    seen = set()
    left = 0
    best = 0
    for right, ch in enumerate(s):
        while ch in seen:
            seen.remove(s[left])
            left += 1
        seen.add(ch)
        best = max(best, right - left + 1)
    return best


def test_length_of_longest_substring():
    assert length_of_longest_substring("") == 0
    assert length_of_longest_substring("a") == 1
    assert length_of_longest_substring("abcdefg") == 7
    assert length_of_longest_substring("aaaa") == 1
    assert length_of_longest_substring("abba") == 2
    assert length_of_longest_substring("au") == 2
    assert length_of_longest_substring("dvdf") == 3
    print("✓ All tests passed")

if __name__ == "__main__":
    test_length_of_longest_substring()
