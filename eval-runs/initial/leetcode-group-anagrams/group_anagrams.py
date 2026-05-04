from collections import defaultdict


def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        groups[key].append(s)
    return list(groups.values())


if __name__ == "__main__":
    tests = [
        (["eat", "tea", "tan", "ate", "nat", "bat"],
         [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]),
        ([""], [[""]]),
        (["a"], [["a"]]),
    ]
    for strs, expected in tests:
        result = groupAnagrams(strs)
        # Compare as sets of frozensets (order doesn't matter)
        assert {frozenset(g) for g in result} == {frozenset(g) for g in expected}
    print("All tests passed.")
