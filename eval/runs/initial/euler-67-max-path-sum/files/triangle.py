TRIANGLE = [
    [3],
    [7, 4],
    [2, 4, 6],
    [8, 5, 9, 3],
    [1, 6, 2, 7, 8],
    [3, 2, 9, 1, 4, 5],
    [6, 7, 3, 5, 8, 2, 4],
    [1, 8, 5, 2, 7, 6, 3, 9],
    [4, 3, 7, 2, 6, 8, 1, 5, 9],
    [2, 6, 8, 4, 7, 3, 5, 9, 1, 4],
]


def max_path(triangle):
    dp = [row[:] for row in triangle]
    for i in range(len(dp) - 2, -1, -1):
        for j in range(len(dp[i])):
            dp[i][j] += max(dp[i + 1][j], dp[i + 1][j + 1])

    # Greedy trace: walk top-to-bottom, always following the larger child
    path, j = [], 0
    for i in range(len(triangle)):
        path.append(triangle[i][j])
        if i < len(triangle) - 1:
            j = j if dp[i + 1][j] >= dp[i + 1][j + 1] else j + 1

    return dp[0][0], path


if __name__ == "__main__":
    total, path = max_path(TRIANGLE)
    print(f"Max sum: {total}")
    print(f"Path:    {' -> '.join(map(str, path))}")
