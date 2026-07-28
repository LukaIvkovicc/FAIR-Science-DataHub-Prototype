# Data Model

The model focuses on a small vertical slice of scientific collection data.

## Tables

- `taxa`: scientific name and basic taxonomy.
- `strains`: strain code, taxon link, origin, source, collection date, and provenance note.
- `sequences`: marker sequence records linked to strains.
- `traits`: simple observed traits linked to strains.
- `datasets`: dataset-level descriptive metadata for export.

## FAIR Notes

- Findable: dataset identifiers, strain codes, and sequence accessions are indexed or unique where useful.
- Accessible: the API exposes browseable JSON endpoints.
- Interoperable: the metadata export uses a Schema.org-inspired JSON-LD shape.
- Reusable: records include license, provenance notes, creator, and keywords.

The example records are synthetic and are included only to demonstrate data handling patterns.

