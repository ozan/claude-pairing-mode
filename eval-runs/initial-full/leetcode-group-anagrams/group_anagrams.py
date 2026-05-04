from collections import defaultdict


def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))
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
        result = group_anagrams(strs)
        # Compare as sets of frozensets (order doesn't matter)
        r = {frozenset(g) for g in result}
        e = {frozenset(g) for g in expected}
        status = "✓" if r == e else "✗"
        print(f"{status} {strs} → {result}")
