cache = {1: 1}

def chain_length(n):
    path = []
    x = n
    while x not in cache:
        path.append(x)
        x = x // 2 if x % 2 == 0 else 3 * x + 1
    length = cache[x]
    for val in reversed(path):
        length += 1
        cache[val] = length
    return cache[n]

best = max(range(1, 1_000_000), key=chain_length)
print(best)
