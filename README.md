# FAIR Scientific Data Hub Prototype

A compact FastAPI prototype for FAIR-oriented scientific data infrastructure.
It demonstrates how synthetic mycology-style records can be ingested, validated,
stored relationally, served through an API, searched with lightweight filters,
and exported as FAIR-style machine-readable metadata.

## Why It Exists

Scientific data infrastructure work often lives between software engineering,
data stewardship, and domain science. This repository shows that intersection in
a small working vertical slice:

- structured example data for taxa, strains, marker sequences, traits, and datasets;
- Pydantic validation before records enter the system;
- SQLAlchemy models with SQLite locally and PostgreSQL through Docker Compose;
- FastAPI endpoints for browsing and creating scientific records;
- lightweight filters for common review/search workflows;
- JSON-LD-style metadata export inspired by Schema.org `Dataset`;
- pytest coverage and GitHub Actions CI;
- documentation, governance, contribution notes, and explicit scope boundaries.

All example data are synthetic and included only to demonstrate data handling
patterns.

## Quickstart

Use Python 3.11 or 3.12.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
python scripts/load_example_data.py
uvicorn app.main:app --reload
```

Open:

- Swagger UI: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- Taxa: http://localhost:8000/taxa
- FAIR metadata export: http://localhost:8000/export/metadata

## Docker Compose

Docker Compose runs the same API against PostgreSQL:

```bash
docker compose up --build
```

In another terminal, load the example data into the API container:

```bash
docker compose exec api python scripts/load_example_data.py
```

Then check:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/taxa
curl http://localhost:8000/export/metadata
```

## Example API Calls

Browse records:

```bash
curl http://localhost:8000/taxa
curl http://localhost:8000/strains
curl http://localhost:8000/sequences
curl http://localhost:8000/datasets
```

Use lightweight filters:

```bash
curl "http://localhost:8000/taxa?scientific_name=penicillium"
curl "http://localhost:8000/strains?origin_country=croatia"
curl "http://localhost:8000/strains?taxon_id=1"
curl "http://localhost:8000/sequences?marker=ITS"
curl "http://localhost:8000/sequences?strain_id=1"
```

Export FAIR-style metadata:

```bash
curl http://localhost:8000/export/metadata
```

More examples are in [docs/api_examples.md](docs/api_examples.md).

## Tests

```bash
pytest
```

The test suite covers validation, ingestion, idempotency, API behavior, browse
filters, and metadata export. GitHub Actions runs the same suite on Python 3.11
and 3.12.

## What To Review First

If you only have a few minutes, start here:

1. [app/main.py](app/main.py): FastAPI app setup and route registration.
2. [app/models.py](app/models.py): relational model for the scientific records.
3. [app/services/ingestion.py](app/services/ingestion.py): idempotent synthetic data loading.
4. [app/services/metadata_export.py](app/services/metadata_export.py): JSON-LD-style FAIR metadata export.
5. [tests/test_api.py](tests/test_api.py): end-to-end API contract and filter behavior.
6. [docs/open_science_alignment.md](docs/open_science_alignment.md): FAIR and Open Science mapping.

## Repository Structure

```text
app/
  api/                 FastAPI route modules
  services/            ingestion, validation, metadata export
  main.py              application entry point
  database.py          SQLAlchemy setup
  models.py            relational model
  schemas.py           Pydantic schemas
data/                  synthetic CSV/JSON example data
scripts/               local utility scripts
tests/                 pytest test suite
docs/                  architecture, data model, API examples, Open Science notes
artifacts/             example FAIR metadata export
```

## Open Science And FAIR Relevance

The prototype is intentionally small, but it reflects core Open Science
infrastructure concerns:

- findable records through stable identifiers and browse filters;
- accessible JSON APIs and OpenAPI documentation;
- interoperable metadata using a JSON-LD-style Schema.org shape;
- reusable synthetic records with license and provenance notes;
- reproducible setup through Python commands, Docker Compose, and tests.

See [docs/open_science_alignment.md](docs/open_science_alignment.md) for the
FAIR mapping and future standards touchpoints, including MIxS, Darwin Core,
OAI-PMH, and persistent identifiers.

## Current Boundaries

This repository is deliberately not a full research infrastructure. It does not
implement authentication, curator roles, full-text search, dataset versioning,
OAI-PMH harvesting, MIxS or Darwin Core exports, image/morphology/toxin data, or
production deployment hardening.

Those are natural next steps for a larger platform. Here, the goal is a clean,
reviewable slice that demonstrates architecture, data modelling, validation,
metadata thinking, reproducibility, and honest project scope.

## Repository Standards

- [CONTRIBUTING.md](CONTRIBUTING.md) explains contribution expectations.
- [GOVERNANCE.md](GOVERNANCE.md) documents the lightweight maintainer model.
- [LICENSE](LICENSE) provides the MIT software license.
