import pytest
from rna_transcription import to_rna

@pytest.mark.parametrize("dna, rna", [
    ("G", "C"),
    ("C", "G"),
    ("T", "A"),
    ("A", "U"),
    ("ACGT", "UGCA"),
    ("", ""),
])
def test_to_rna(dna, rna):
    assert to_rna(dna) == rna

def test_invalid_raises():
    with pytest.raises(ValueError):
        to_rna("ACGX")
