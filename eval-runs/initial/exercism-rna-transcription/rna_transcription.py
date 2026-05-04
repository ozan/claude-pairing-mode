"""RNA Transcription: convert a DNA strand to its RNA complement.

Mapping: G → C, C → G, T → A, A → U
Invalid characters raise ValueError.
"""

_VALID_DNA = frozenset("GCTA")
_TABLE = str.maketrans("GCTA", "CGAU")


def to_rna(dna_strand: str) -> str:
    """Return the RNA complement of *dna_strand*.

    Raises ValueError for any character not in {G, C, T, A}.
    """
    invalid = frozenset(dna_strand) - _VALID_DNA
    if invalid:
        raise ValueError(
            f"Invalid nucleotide(s) in DNA strand: {sorted(invalid)}"
        )
    return dna_strand.translate(_TABLE)
