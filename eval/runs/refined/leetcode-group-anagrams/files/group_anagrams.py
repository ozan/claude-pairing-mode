from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        groups[tuple(sorted(s))].append(s)
    return list(groups.values())

if __name__ == "__main__":
    result = group_anagrams(["eat","tea","tan","ate","nat","bat"])
    assert {frozenset(g) for g in result} == \
           {frozenset(["eat","tea","ate"]), frozenset(["tan","nat"]), frozenset(["bat"])}
    print("OK")
