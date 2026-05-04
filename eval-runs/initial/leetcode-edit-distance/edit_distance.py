def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)

    # prev[j] = min edits to convert word1[:i-1] -> word2[:j]
    prev = list(range(n + 1))

    for i in range(1, m + 1):
        curr = [i] + [0] * n          # curr[0] = i deletions to reach empty word2
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                curr[j] = prev[j-1]   # chars match: inherit diagonal, no op needed
            else:
                curr[j] = 1 + min(prev[j],      # delete word1[i-1]
                                  curr[j-1],    # insert word2[j-1]
                                  prev[j-1])    # substitute
        prev = curr

    return prev[n]


# quick smoke tests
assert min_distance("horse", "ros") == 3
assert min_distance("intention", "execution") == 5
assert min_distance("", "abc") == 3
assert min_distance("abc", "") == 3
assert min_distance("abc", "abc") == 0
print("all tests passed")
