def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    # dp[i][j] = edit distance between word1[:i] and word2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: transforming to/from empty string
    for i in range(m + 1):
        dp[i][0] = i  # delete all i chars
    for j in range(n + 1):
        dp[0][j] = j  # insert all j chars

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # chars match, no op needed
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j - 1],  # substitute
                    dp[i - 1][j],      # delete from word1
                    dp[i][j - 1],      # insert into word1
                )

    return dp[m][n]


def min_distance_opt(word1: str, word2: str) -> int:
    """Space-optimized O(n) version using a single row."""
    m, n = len(word1), len(word2)
    dp = list(range(n + 1))  # base case: dp[j] = j
    for i in range(1, m + 1):
        prev = dp[0]   # holds dp[i-1][j-1] (diagonal) before it's overwritten
        dp[0] = i      # base case: dp[i][0] = i
        for j in range(1, n + 1):
            temp = dp[j]  # save before overwrite; becomes prev (diagonal) next iteration
            if word1[i - 1] == word2[j - 1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(
                    prev,     # substitute  (dp[i-1][j-1])
                    dp[j],    # delete      (dp[i-1][j])
                    dp[j-1],  # insert      (dp[i][j-1])
                )
            prev = temp
    return dp[n]


if __name__ == "__main__":
    cases = [
        ("horse", "ros", 3),
        ("intention", "execution", 5),
        ("", "abc", 3),
        ("abc", "abc", 0),
        ("a", "b", 1),
    ]
    for w1, w2, expected in cases:
        r1 = min_distance(w1, w2)
        r2 = min_distance_opt(w1, w2)
        status = "✓" if r1 == r2 == expected else "✗"
        print(f"{status} ({w1!r}, {w2!r}) 2D={r1}  1D={r2}  expected={expected}")
