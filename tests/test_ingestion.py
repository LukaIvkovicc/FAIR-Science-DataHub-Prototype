from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.services.ingestion import load_example_data


def test_load_example_data(db_session: Session, data_dir) -> None:
    summary = load_example_data(db_session, data_dir)

    assert summary == {"taxa": 3, "strains": 3, "sequences": 3, "traits": 3, "datasets": 1}
    assert db_session.scalar(select(models.Taxon).where(models.Taxon.scientific_name == "Aspergillus demoensis"))
    assert db_session.scalar(select(models.SequenceRecord).where(models.SequenceRecord.accession == "SYN000001"))


def test_load_example_data_is_idempotent(db_session: Session, data_dir) -> None:
    load_example_data(db_session, data_dir)
    load_example_data(db_session, data_dir)

    assert db_session.query(models.Taxon).count() == 3
    assert db_session.query(models.Strain).count() == 3
    assert db_session.query(models.SequenceRecord).count() == 3
    assert db_session.query(models.Dataset).count() == 1

