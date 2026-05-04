_DNA_TO_RNA = str.maketrans("GCTA", "CGAU")
_VALID_DNA = frozenset("GCTA")


def to_rna(dna_strand: str) -> str:
    """Return the RNA complement of the given DNA strand.

    Mapping: G→C  C→G  T→A  A→U

    Raises ValueError for any character not in {G, C, T, A}.
    """
    invalid = set(dna_strand) - _VALID_DNA
    if invalid:
        raise ValueError(
            f"Invalid DNA nucleotide(s): {', '.join(sorted(invalid))}"
        )
    return dna_strand.translate(_DNA_TO_RNA)
