FAIR Scientific Data Hub Prototype — compact FAIR data platform (lead developer)

One-line impact: Delivered a compact, interview-ready data hub demonstrating end-to-end FAIR ingestion, validation, relational modelling, API serving and machine-readable metadata exports.

- Problem: reviewers need a small, runnable demonstrator to assess FAIR design and engineering skills quickly.
- Action: Built a FastAPI backend with idempotent ingestion, Pydantic validation, relational models for taxa/strains/sequences, and JSON-LD-style metadata export; provided Docker compose and tests.
- Result: A testable, documented vertical slice that proves design choices, metadata modelling, and API contracts; includes automated tests and demo data for immediate reviewer inspection.

Tech: FastAPI, SQLAlchemy, Pydantic, SQLite/Postgres, JSON-LD exports, Docker Compose, Pytest.
