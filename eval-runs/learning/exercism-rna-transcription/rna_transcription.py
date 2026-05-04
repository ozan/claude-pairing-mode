DNA_TO_RNA = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}


def to_rna(dna_strand):
    """Return the RNA complement of the given DNA strand.

    Raises ValueError for any character not in {G, C, T, A}.
    """
    rna = []
    for nucleotide in dna_strand:
        if nucleotide not in DNA_TO_RNA:
            raise ValueError(f"Invalid nucleotide: {nucleotide!r}")
        rna.append(DNA_TO_RNA[nucleotide])
    return ''.join(rna)
