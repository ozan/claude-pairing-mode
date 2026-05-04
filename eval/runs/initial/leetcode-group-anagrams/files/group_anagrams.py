from collections import defaultdict


def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        groups[key].append(s)
    return list(groups.values())


if __name__ == "__main__":
    def check(strs, expected):
        result = group_anagrams(strs)
        norm = lambda groups: sorted(sorted(g) for g in groups)
        assert norm(result) == norm(expected), f"{result} != {expected}"

    check(["eat","tea","tan","ate","nat","bat"],
          [["ate","eat","tea"],["nat","tan"],["bat"]])
    check([""], [[""]])
    check(["a"], [["a"]])
    print("All tests passed.")
