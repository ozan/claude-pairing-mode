import math

def count_paths_dp(n):
    """DP solution: rolling row, O(n) space."""
    row = [1] * (n + 1)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            row[j] += row[j-1]
    return row[n]

def count_paths_closed(n):
    """Closed form: C(2n, n)."""
    return math.comb(2 * n, n)

if __name__ == "__main__":
    n = 20
    dp_answer = count_paths_dp(n)
    closed_answer = count_paths_closed(n)

    print(f"DP solution: {dp_answer}")
    print(f"Closed form: {closed_answer}")
    print(f"Match: {dp_answer == closed_answer}")
