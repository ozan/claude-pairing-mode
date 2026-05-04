def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    if m < n:
        word1, word2 = word2, word1
        m, n = n, m
    dp = list(range(n+1))
    for i in range(1, m+1):
        prev = dp[0]   # dp[i-1][0] before overwrite
        dp[0] = i
        for j in range(1, n+1):
            temp = dp[j]
            if word1[i-1] == word2[j-1]: dp[j] = prev
            else: dp[j] = 1 + min(dp[j], dp[j-1], prev)
            prev = temp
    return dp[n]


cases = [
    ("horse",   "ros",    3),  # classic LC example
    ("intention","execution", 5),  # classic LC example
    ("",        "",       0),  # both empty
    ("a",       "",       1),  # delete one char
    ("",        "a",      1),  # insert one char
    ("abc",     "abc",    0),  # identical strings
    ("ab",      "ba",     2),  # two swaps (each = sub + sub)
]

for word1, word2, expected in cases:
    result = min_distance(word1, word2)
    status = "✓" if result == expected else f"✗ (got {result})"
    print(f"{status}  min_distance({word1!r}, {word2!r}) = {result}  (expected {expected})")
