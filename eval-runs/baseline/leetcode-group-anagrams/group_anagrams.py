from collections import defaultdict


def groupAnagrams(strs: list[str]) -> list[list[str]]:
    """
    Group strings that are anagrams of each other.

    Strategy: sorted characters form a canonical key — all anagrams
    share the same key and get collected into the same bucket.

    Time:  O(N * K log K)  — N words, K = max word length
    Space: O(N * K)        — storing all words in the hash map
    """
    groups: dict[tuple, list[str]] = defaultdict(list)

    for word in strs:
        key = tuple(sorted(word))
        groups[key].append(word)

    return list(groups.values())


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def sorted_groups(result: list[list[str]]) -> list[list[str]]:
    """Canonical form for comparison: sort within each group, then sort groups."""
    return sorted(sorted(group) for group in result)


def test_leetcode_example():
    strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    result = groupAnagrams(strs)
    assert sorted_groups(result) == sorted_groups([
        ["eat", "tea", "ate"],
        ["tan", "nat"],
        ["bat"],
    ])


def test_single_empty_string():
    # Edge case: one empty string — it's its own group
    assert groupAnagrams([""]) == [[""]]


def test_multiple_empty_strings():
    # Two empty strings are anagrams of each other
    result = groupAnagrams(["", ""])
    assert sorted_groups(result) == [[""  , ""]]


def test_all_unique():
    strs = ["abc", "def", "ghi"]
    result = groupAnagrams(strs)
    assert sorted_groups(result) == sorted_groups([["abc"], ["def"], ["ghi"]])


def test_all_same_anagram():
    strs = ["abc", "bca", "cab", "acb"]
    result = groupAnagrams(strs)
    assert len(result) == 1
    assert sorted(result[0]) == ["abc", "acb", "bca", "cab"]


def test_single_character_words():
    strs = ["a", "b", "a"]
    result = groupAnagrams(strs)
    assert sorted_groups(result) == sorted_groups([["a", "a"], ["b"]])


def test_single_word():
    assert groupAnagrams(["hello"]) == [["hello"]]


def test_mixed_lengths():
    # Words of different lengths cannot be anagrams
    strs = ["ab", "ba", "abc", "bca"]
    result = groupAnagrams(strs)
    assert sorted_groups(result) == sorted_groups([["ab", "ba"], ["abc", "bca"]])


if __name__ == "__main__":
    tests = [
        test_leetcode_example,
        test_single_empty_string,
        test_multiple_empty_strings,
        test_all_unique,
        test_all_same_anagram,
        test_single_character_words,
        test_single_word,
        test_mixed_lengths,
    ]
    for t in tests:
        t()
        print(f"  PASS  {t.__name__}")
    print(f"\n{len(tests)} tests passed.")
