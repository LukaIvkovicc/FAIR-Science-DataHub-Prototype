# API Examples

Run the API:

```bash
uvicorn app.main:app --reload
```

Load example data:

```bash
python scripts/load_example_data.py
```

Check health:

```bash
curl http://localhost:8000/health
```

List taxa:

```bash
curl http://localhost:8000/taxa
```

Filter taxa by partial scientific name:

```bash
curl "http://localhost:8000/taxa?scientific_name=penicillium"
```

Filter strains by country or taxon:

```bash
curl "http://localhost:8000/strains?origin_country=croatia"
curl "http://localhost:8000/strains?taxon_id=1"
```

Filter sequences by marker or strain:

```bash
curl "http://localhost:8000/sequences?marker=ITS"
curl "http://localhost:8000/sequences?strain_id=1"
```

Export FAIR-style metadata:

```bash
curl http://localhost:8000/export/metadata
```

Create a taxon:

```bash
curl -X POST http://localhost:8000/taxa \
  -H "Content-Type: application/json" \
  -d '{"scientific_name":"Demo species","kingdom":"Fungi","phylum":"Ascomycota","family":"Demoaceae"}'
```

Create a strain linked to an existing taxon:

```bash
curl -X POST http://localhost:8000/strains \
  -H "Content-Type: application/json" \
  -d '{"strain_code":"FSDH-004","taxon_id":1,"origin_country":"Netherlands","isolation_source":"synthetic demo record"}'
```

Create a sequence linked to an existing strain:

```bash
curl -X POST http://localhost:8000/sequences \
  -H "Content-Type: application/json" \
  -d '{"strain_id":1,"marker":"ITS","accession":"SYN000004","sequence":"ATGCGTACGTAGCTAGCTAG"}'
```

If a linked parent record does not exist, the API returns a clean `404` response
instead of exposing a database error.
