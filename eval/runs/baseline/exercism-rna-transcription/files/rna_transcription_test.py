"""Tests for RNA Transcription exercise."""

import pytest
from rna_transcription import to_rna


# ── Single nucleotide mappings ────────────────────────────────────────────────

def test_cytosine_to_guanine():
    assert to_rna("C") == "G"

def test_guanine_to_cytosine():
    assert to_rna("G") == "C"

def test_thymine_to_adenine():
    assert to_rna("T") == "A"

def test_adenine_to_uracil():
    assert to_rna("A") == "U"


# ── Full strands ──────────────────────────────────────────────────────────────

def test_rna_complement_of_all_nucleotides():
    assert to_rna("ACGT") == "UGCA"

def test_typical_strand():
    assert to_rna("GCATGGTA") == "CGUACCAU"

def test_empty_strand():
    assert to_rna("") == ""

def test_long_strand():
    dna = "TTAAGGCCTTAAGGCCTTAAGGCC"
    rna = "AAUUCCGGAAUUCCGGAAUUCCGG"
    assert to_rna(dna) == rna


# ── Input validation ──────────────────────────────────────────────────────────

def test_invalid_nucleotide_raises():
    with pytest.raises(ValueError):
        to_rna("U")

def test_lowercase_raises():
    with pytest.raises(ValueError):
        to_rna("acgt")

def test_invalid_character_in_middle_raises():
    with pytest.raises(ValueError):
        to_rna("ACXGT")

def test_multiple_invalid_characters_raises():
    with pytest.raises(ValueError):
        to_rna("ABCDE")

def test_space_raises():
    with pytest.raises(ValueError):
        to_rna("A C G")
