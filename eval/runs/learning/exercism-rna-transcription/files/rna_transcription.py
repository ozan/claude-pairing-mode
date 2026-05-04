"""RNA Transcription: convert a DNA strand to its RNA complement."""

# Maps each valid DNA nucleotide to its RNA complement
_DNA_TO_RNA = str.maketrans("GCTA", "CGAU")


def to_rna(dna_strand: str) -> str:
    """Return the RNA complement of *dna_strand*.

    Each nucleotide is transcribed according to the rule:
        G → C  |  C → G  |  T → A  |  A → U

    Raises ValueError for any character that is not a valid DNA nucleotide.
    """
    invalid = set(dna_strand) - set("GCTA")
    if invalid:
        label = "nucleotide" if len(invalid) == 1 else "nucleotides"
        raise ValueError(
            f"Invalid DNA {label}: {', '.join(sorted(invalid))}"
        )

    return dna_strand.translate(_DNA_TO_RNA)
