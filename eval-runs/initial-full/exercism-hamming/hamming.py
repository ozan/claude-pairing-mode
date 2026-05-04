def distance(a, b):
    if len(a) != len(b):
        raise ValueError("Strands must be of equal length.")
    return sum(x != y for x, y in zip(a, b))
