"""RNA Transcription: convert a DNA strand to its RNA complement."""

# Maps each valid DNA nucleotide to its RNA complement
_DNA_TO_RNA = str.maketrans("GCTA", "CGAU")
_VALID_DNA = frozenset("GCTA")


def to_rna(dna_strand: str) -> str:
    """Return the RNA complement of a DNA strand.

    Mapping:
        G -> C
        C -> G
        T -> A
        A -> U

    Args:
        dna_strand: A string of uppercase DNA nucleotides (G, C, T, A).

    Returns:
        The RNA complement string.

    Raises:
        ValueError: If the strand contains any character that is not a valid
                    DNA nucleotide (G, C, T, or A).
    """
    invalid = set(dna_strand) - _VALID_DNA
    if invalid:
        raise ValueError(
            f"Invalid DNA nucleotide(s): {', '.join(sorted(invalid))}"
        )
    return dna_strand.translate(_DNA_TO_RNA)
