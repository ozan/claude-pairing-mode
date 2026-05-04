LIMIT = 1_000_000
cache = {1: 1}

def chain_length(n):
    path = []
    while n not in cache:
        path.append(n)
        n = n // 2 if n % 2 == 0 else 3 * n + 1
    length = cache[n]
    for node in reversed(path):
        length += 1
        cache[node] = length
    return length

max_length = 0
max_start = 0

for start in range(1, LIMIT):
    length = chain_length(start)
    if length > max_length:
        max_length = length
        max_start = start

print(max_start)
