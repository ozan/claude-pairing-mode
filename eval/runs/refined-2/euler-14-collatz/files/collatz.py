cache = {1: 1}

def chain_len(start):
    path = []
    n = start
    while n not in cache:
        path.append(n)
        n = n // 2 if n % 2 == 0 else 3 * n + 1
    length = cache[n]
    for x in reversed(path):
        length += 1
        cache[x] = length
    return cache[start]

best_start, best_len = 1, 1
for i in range(2, 1_000_000):
    l = chain_len(i)
    if l > best_len:
        best_start, best_len = i, l

print(f"Starting number: {best_start}  (chain length: {best_len})")
