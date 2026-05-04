def to_rna(dna_strand):
    mapping = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
    if any(n not in mapping for n in dna_strand):
        raise ValueError("Invalid nucleotide in strand")
    return ''.join(mapping[n] for n in dna_strand)
