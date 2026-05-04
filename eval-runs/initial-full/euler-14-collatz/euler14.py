import sys
sys.setrecursionlimit(1_000_000)

cache = {1: 1}

def chain_len(n):
    if n in cache:
        return cache[n]
    step = chain_len(n // 2 if n % 2 == 0 else 3 * n + 1)
    cache[n] = step + 1
    return cache[n]

best = max(range(1, 1_000_000), key=chain_len)
print(best)
