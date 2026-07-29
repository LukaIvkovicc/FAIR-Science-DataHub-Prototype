from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401
from app.database import Base, get_db
from app.main import app
from app.services.ingestion import load_example_data


def _client_with_example_data(data_dir) -> TestClient:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db() -> Generator[Session, None, None]:
        with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestingSessionLocal() as session:
            load_example_data(session, data_dir)

        return TestClient(app)
    except Exception:
        app.dependency_overrides.clear()
        raise


def test_api_health_and_core_endpoints(data_dir) -> None:
    client = _client_with_example_data(data_dir)
    try:
        assert client.get("/health").json() == {"status": "ok"}
        assert len(client.get("/taxa").json()) == 3
        assert len(client.get("/strains").json()) == 3
        assert len(client.get("/sequences").json()) == 3
        assert client.get("/datasets").json()[0]["identifier"] == "doi:10.0000/fair-data-hub-demo"
        assert client.get("/export/metadata").json()["@type"] == "Dataset"
    finally:
        app.dependency_overrides.clear()


def test_api_returns_clean_errors_for_missing_parent_records(data_dir) -> None:
    client = _client_with_example_data(data_dir)
    try:
        missing_taxon = client.post(
            "/strains",
            json={"strain_code": "FSDH-404", "taxon_id": 404},
        )
        missing_strain = client.post(
            "/sequences",
            json={"strain_id": 404, "marker": "ITS", "sequence": "ATGCGTACGT"},
        )

        assert missing_taxon.status_code == 404
        assert missing_taxon.json()["detail"] == "Taxon 404 was not found"
        assert missing_strain.status_code == 404
        assert missing_strain.json()["detail"] == "Strain 404 was not found"
    finally:
        app.dependency_overrides.clear()


def test_api_duplicate_sequence_post_is_idempotent(data_dir) -> None:
    client = _client_with_example_data(data_dir)
    try:
        sequence = client.get("/sequences").json()[0]
        response = client.post(
            "/sequences",
            json={
                "strain_id": sequence["strain_id"],
                "marker": sequence["marker"],
                "accession": sequence["accession"],
                "sequence": sequence["sequence"],
                "quality_note": sequence["quality_note"],
            },
        )

        assert response.status_code == 201
        assert response.json()["id"] == sequence["id"]
        assert len(client.get("/sequences").json()) == 3
    finally:
        app.dependency_overrides.clear()


def test_api_supports_lightweight_browse_filters(data_dir) -> None:
    client = _client_with_example_data(data_dir)
    try:
        taxa = client.get("/taxa", params={"scientific_name": "penicillium"}).json()
        strains = client.get("/strains", params={"origin_country": "croatia"}).json()
        sequences = client.get("/sequences", params={"marker": "ITS"}).json()

        assert [taxon["scientific_name"] for taxon in taxa] == ["Penicillium exemplare"]
        assert [strain["strain_code"] for strain in strains] == ["FSDH-002"]
        assert {sequence["accession"] for sequence in sequences} == {"SYN000001", "SYN000002"}
    finally:
        app.dependency_overrides.clear()
