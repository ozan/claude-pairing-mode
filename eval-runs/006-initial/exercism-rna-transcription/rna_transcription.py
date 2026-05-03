DNA_TO_RNA = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}

def to_rna(dna_strand):
    try:
        return ''.join(DNA_TO_RNA[n] for n in dna_strand)
    except KeyError as e:
        raise ValueError(f"Invalid nucleotide: {e.args[0]}") from e
