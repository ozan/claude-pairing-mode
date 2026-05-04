_TABLE = str.maketrans('GCTA', 'CGAU')

def to_rna(dna_strand):
    if invalid := set(dna_strand) - set('GCTA'):
        raise ValueError(f"Invalid nucleotide(s): {invalid}")
    return dna_strand.translate(_TABLE)
