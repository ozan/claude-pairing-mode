MAP = {"G": "C", "C": "G", "T": "A", "A": "U"}

def to_rna(dna_strand: str) -> str:
    try:
        return "".join(MAP[c] for c in dna_strand)
    except KeyError as e:
        raise ValueError(f"invalid nucleotide: {e}") from e
