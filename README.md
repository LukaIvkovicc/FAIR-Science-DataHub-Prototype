# FAIR Scientific Data Hub Prototype

An interview-ready prototype for a FAIR-oriented scientific data hub. The code shows a compact but complete slice of a mycology data platform: ingest structured example data, validate it, store it relationally, expose it through FastAPI, and export FAIR-style metadata in a machine-readable form.

The repository uses synthetic example data only. It is intentionally scoped as a portfolio prototype, not a production deployment, and it does not contain confidential or institution-specific project material.

## Why This Repo Exists

This project is designed to demonstrate how a small scientific data hub can be made reproducible, reviewable, and easy to extend. It is especially aimed at showing:

- clear backend architecture,
- data modelling for biological entities,
- practical validation and ingestion logic,
- FAIR-minded metadata export,
- and a testable, documented developer workflow.

## What It Demonstrates

- FastAPI service design with route modules and dependency injection.
- Relational modelling for taxa, strains, sequences, traits, and datasets.
- Structured validation for scientific example data.
- Synthetic ingestion that is idempotent and easy to rerun.
- SQLite for local development, PostgreSQL through Docker Compose.
- JSON-LD-style metadata export inspired by Schema.org.
- Automated tests for validation, ingestion, API endpoints, and metadata export.
- A repo structure that is easy for reviewers to inspect quickly.

## Fastest Way To Try It

Use Python 3.11 or 3.12.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
python scripts/load_example_data.py
uvicorn app.main:app --reload
```

Open these URLs after startup:

- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Metadata export: http://localhost:8000/export/metadata

## What To Check First

If you only have a minute, inspect these files in order:

1. [app/main.py](app/main.py) for the app entry point and mounted routes.
2. [app/services/ingestion.py](app/services/ingestion.py) for the synthetic data loading flow.
3. [app/services/metadata_export.py](app/services/metadata_export.py) for the FAIR-style export.
4. [tests/test_api.py](tests/test_api.py) for the main end-to-end contract.
5. [docs/architecture.md](docs/architecture.md) for the repo-level design story.

## Run Tests

```bash
pytest
```

The repository also includes a GitHub Actions workflow so the same checks can run automatically on pull requests.

## Docker Compose

Docker Compose starts the API with PostgreSQL and waits for the database to become healthy before launching the app:

```bash
docker compose up --build
```

In another terminal, load the example data into the running API container:

```bash
docker compose exec api python scripts/load_example_data.py
```

## Project Structure

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
docs/                  architecture, data model, API examples
```

## Repository Standards

- [CONTRIBUTING.md](CONTRIBUTING.md) explains how to work on the codebase.
- [GOVERNANCE.md](GOVERNANCE.md) documents the maintainer model for this prototype.
- [docs/api_examples.md](docs/api_examples.md) shows example requests and responses.

## Notes For Reviewers

This is deliberately a small, working vertical slice. It is meant to be easy to run, easy to verify, and easy to discuss in an interview. The code favours clarity and reproducibility over broad feature coverage.

