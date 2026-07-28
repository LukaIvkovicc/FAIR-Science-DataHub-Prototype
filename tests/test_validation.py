import pytest
from pydantic import ValidationError

from app.schemas import SequenceCreate, TaxonCreate


def test_taxon_validation_requires_scientific_name() -> None:
    with pytest.raises(ValidationError):
        TaxonCreate(scientific_name="", kingdom="Fungi")


def test_sequence_validation_normalizes_iupac_dna() -> None:
    sequence = SequenceCreate(strain_id=1, marker="ITS", sequence="acgtnn--ac")

    assert sequence.sequence == "ACGTNN--AC"


def test_sequence_validation_rejects_invalid_symbols() -> None:
    with pytest.raises(ValidationError):
        SequenceCreate(strain_id=1, marker="ITS", sequence="ACGTXYZ123")

