def distance(strand_a, strand_b):
    """Return the Hamming distance between two equal-length DNA strands.

    Raises ValueError if the strands are not the same length.
    """
    if len(strand_a) != len(strand_b):
        raise ValueError("Strands must be of equal length")

    return sum(a != b for a, b in zip(strand_a, strand_b))
