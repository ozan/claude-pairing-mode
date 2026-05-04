def distance(a, b):
    if len(a) != len(b):
        raise ValueError("Strands must be of equal length")
    return sum(c1 != c2 for c1, c2 in zip(a, b))
