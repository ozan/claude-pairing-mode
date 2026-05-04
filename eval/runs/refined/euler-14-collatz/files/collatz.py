cache = {1: 1}

def collatz_len(n):
    chain = []
    while n not in cache:
        chain.append(n)
        n = n // 2 if n % 2 == 0 else 3 * n + 1
    length = cache[n]
    for x in reversed(chain):
        length += 1
        cache[x] = length
    return cache[chain[0]] if chain else cache[n]

print(max(range(1, 1_000_000), key=collatz_len))
