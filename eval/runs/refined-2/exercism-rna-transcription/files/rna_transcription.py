MAP = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}

def to_rna(dna_strand):
    result = []
    for ch in dna_strand:
        if ch not in MAP:
            raise ValueError(f"Invalid nucleotide: {ch!r}")
        result.append(MAP[ch])
    return ''.join(result)
