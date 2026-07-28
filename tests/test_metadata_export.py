from sqlalchemy.orm import Session

from app.services.ingestion import load_example_data
from app.services.metadata_export import build_fair_metadata_export


def test_metadata_export_contains_fair_signals(db_session: Session, data_dir) -> None:
    load_example_data(db_session, data_dir)

    exported = build_fair_metadata_export(db_session)

    assert exported["@context"] == "https://schema.org"
    assert exported["@type"] == "Dataset"
    assert exported["license"] == "CC0-1.0"
    assert "FAIR data" in exported["keywords"]
    assert {"name": "taxa_count", "value": 3} in exported["additionalProperty"]

