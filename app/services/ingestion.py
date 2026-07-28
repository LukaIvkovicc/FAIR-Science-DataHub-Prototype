from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.services.validation import read_csv_rows, read_json_records, validate_dataset_records, validate_sequence_rows, validate_taxa_rows


def load_example_data(db: Session, data_dir: Path) -> dict[str, int]:
    taxa = validate_taxa_rows(read_csv_rows(data_dir / "example_taxa.csv"))
    taxon_by_name = {taxon.scientific_name: crud.create_taxon(db, taxon) for taxon in taxa}

    strain_count = 0
    strain_ids: dict[str, int] = {}
    for row in read_csv_rows(data_dir / "example_strains.csv"):
        taxon_name = row.pop("scientific_name")
        strain = schemas.StrainCreate(taxon_id=taxon_by_name[taxon_name].id, **row)
        record = crud.create_strain(db, strain)
        strain_ids[record.strain_code] = record.id
        strain_count += 1

    sequence_count = 0
    for sequence in validate_sequence_rows(read_csv_rows(data_dir / "example_sequences.csv"), strain_ids):
        existing = db.scalar(
            select(models.SequenceRecord).where(
                models.SequenceRecord.strain_id == sequence.strain_id,
                models.SequenceRecord.marker == sequence.marker,
            )
        )
        if not existing:
            crud.create_sequence(db, sequence)
        sequence_count += 1

    trait_count = 0
    for row in read_csv_rows(data_dir / "example_traits.csv"):
        strain_code = row.pop("strain_code")
        existing = db.scalar(
            select(models.Trait).where(
                models.Trait.strain_id == strain_ids[strain_code],
                models.Trait.trait_name == row["trait_name"],
            )
        )
        if not existing:
            db.add(models.Trait(strain_id=strain_ids[strain_code], **row))
            db.commit()
        trait_count += 1

    datasets = validate_dataset_records(read_json_records(data_dir / "example_datasets.json"))
    for dataset in datasets:
        crud.create_dataset(db, dataset)

    return {
        "taxa": len(taxa),
        "strains": strain_count,
        "sequences": sequence_count,
        "traits": trait_count,
        "datasets": len(datasets),
    }

