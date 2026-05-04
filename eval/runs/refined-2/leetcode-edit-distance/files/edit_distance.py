def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)

    prev = list(range(n + 1))          # dp[i-1][*], base case: empty word1

    for i in range(1, m + 1):
        curr = [i] + [0] * n           # base case: dp[i][0] = i (delete all)
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]  # characters match — no operation needed
            else:
                curr[j] = 1 + min(
                    prev[j],           # delete from word1
                    curr[j - 1],       # insert into word1
                    prev[j - 1],       # substitute
                )
        prev = curr

    return prev[n]


# --- tests ---
assert minDistance("horse", "ros") == 3
assert minDistance("intention", "execution") == 5
assert minDistance("", "") == 0
assert minDistance("a", "") == 1
assert minDistance("", "a") == 1
assert minDistance("abc", "abc") == 0
print("All tests passed.")
