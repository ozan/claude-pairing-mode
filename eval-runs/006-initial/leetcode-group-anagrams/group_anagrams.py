from collections import defaultdict


def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        groups[key].append(s)
    return list(groups.values())


if __name__ == "__main__":
    tests = [
        (["eat", "tea", "tan", "ate", "nat", "bat"], [["eat","tea","ate"],["tan","nat"],["bat"]]),
        ([""], [[""]]),
        (["a"], [["a"]]),
    ]
    for strs, expected in tests:
        result = group_anagrams(strs)
        # compare as sets of frozensets since order doesn't matter
        got = {frozenset(g) for g in result}
        exp = {frozenset(g) for g in expected}
        status = "✓" if got == exp else "✗"
        print(f"{status} group_anagrams({strs}) -> {result}")
