# Open Science Alignment

This repository is a compact portfolio prototype, not a production platform. It
uses synthetic fungal collection data to demonstrate practical Open Science and
FAIR infrastructure patterns in a form that can be reviewed quickly.

## FAIR Mapping

### Findable

- Dataset-level metadata includes an example identifier.
- Taxa, strain codes, sequence accessions, and dataset identifiers are exposed
  through stable API fields.
- Browse filters make records easier to discover by taxon name, country, marker,
  and parent record.

### Accessible

- Data are served through documented FastAPI endpoints.
- Swagger/OpenAPI documentation is available at `/docs` during local runs.
- Docker Compose demonstrates the same API against PostgreSQL.

### Interoperable

- The metadata export uses a JSON-LD-style shape inspired by Schema.org
  `Dataset`.
- The data model separates taxa, strains, sequences, traits, and dataset-level
  metadata so future standards mappings can be added without rewriting the
  whole application.

### Reusable

- Example records include provenance notes and a dataset license.
- The ingestion script is idempotent, supporting reproducible local demos.
- Tests verify validation, ingestion, API behavior, and metadata export.

## Standards Touchpoints

The prototype does not implement full community-standard exports yet, but its
model is intentionally shaped so those mappings are plausible future work.

- **MIxS**: sequence records could be extended with sample environment,
  collection, and sequencing metadata.
- **Darwin Core**: taxa and strains could be mapped to occurrence, taxon, event,
  and material sample terms.
- **OAI-PMH**: dataset metadata could be exposed through a harvesting endpoint
  once repository records and versioning are introduced.
- **Persistent identifiers**: synthetic identifiers in the example data indicate
  where real strain, sequence, and dataset PIDs would be used in a deployed
  infrastructure.

## Intentional Boundaries

- The data are synthetic and generic.
- The repository does not include confidential data or institution-specific
  records.
- Authentication, curator roles, full text search, dataset versioning, image
  records, mycotoxin data, and production deployment hardening are outside this
  small vertical slice.

These boundaries keep the project honest: it demonstrates architecture and data
stewardship thinking without claiming to be a complete research infrastructure.
