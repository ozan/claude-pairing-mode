def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)

    # dp[j] = edit distance between word1[:i] and word2[:j] for current row i
    dp = list(range(n + 1))  # base case: row 0 = [0, 1, 2, ..., n]

    for i in range(1, m + 1):
        new_dp = [i] + [0] * n      # new_dp[0] = i (delete all of word1[:i])
        prev = dp[0]                 # holds dp[i-1][j-1] before it's overwritten
        for j in range(1, n + 1):
            temp = dp[j]             # save dp[i-1][j] before we move on
            if word1[i - 1] == word2[j - 1]:
                new_dp[j] = prev     # no cost: consume one char from each
            else:
                new_dp[j] = 1 + min(
                    dp[j],           # delete  (above)
                    new_dp[j - 1],   # insert  (left in current row)
                    prev,            # substitute (diagonal)
                )
            prev = temp              # slide the diagonal forward
        dp = new_dp

    return dp[n]


# --- tests ---
assert min_distance("horse", "ros") == 3
assert min_distance("intention", "execution") == 5
assert min_distance("", "abc") == 3
assert min_distance("abc", "") == 3
assert min_distance("abc", "abc") == 0
assert min_distance("a", "b") == 1
print("All tests passed.")
