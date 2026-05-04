def climbStairs(n: int) -> int:
    # a, b represent ways(i-1) and ways(i), starting from ways(0)=1, ways(1)=1
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


if __name__ == "__main__":
    for n in range(1, 8):
        print(f"n={n}: {climbStairs(n)}")
