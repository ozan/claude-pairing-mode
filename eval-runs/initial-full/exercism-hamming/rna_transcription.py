MAP = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}


def to_rna(dna_strand):
    if invalid := set(dna_strand) - MAP.keys():
        raise ValueError(f"Invalid nucleotide(s): {invalid}")
    return ''.join(MAP[c] for c in dna_strand)
