import csv
import json
from pathlib import Path
from typing import Any

from app import schemas


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_json_records(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, list):
        raise ValueError(f"{path} must contain a JSON array")
    return payload


def validate_taxa_rows(rows: list[dict[str, str]]) -> list[schemas.TaxonCreate]:
    return [schemas.TaxonCreate(**row) for row in rows]


def validate_sequence_rows(rows: list[dict[str, str]], strain_ids: dict[str, int]) -> list[schemas.SequenceCreate]:
    validated = []
    for row in rows:
        strain_code = row.pop("strain_code")
        validated.append(schemas.SequenceCreate(strain_id=strain_ids[strain_code], **row))
    return validated


def validate_dataset_records(records: list[dict[str, Any]]) -> list[schemas.DatasetCreate]:
    return [schemas.DatasetCreate(**record) for record in records]

