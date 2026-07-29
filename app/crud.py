from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


def list_taxa(db: Session, scientific_name: str | None = None) -> list[models.Taxon]:
    query = select(models.Taxon)
    if scientific_name:
        query = query.where(models.Taxon.scientific_name.ilike(f"%{scientific_name}%"))
    return list(db.scalars(query.order_by(models.Taxon.scientific_name)))


def create_taxon(db: Session, taxon: schemas.TaxonCreate) -> models.Taxon:
    existing = db.scalar(select(models.Taxon).where(models.Taxon.scientific_name == taxon.scientific_name))
    if existing:
        return existing
    record = models.Taxon(**taxon.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_strains(
    db: Session,
    taxon_id: int | None = None,
    origin_country: str | None = None,
) -> list[models.Strain]:
    query = select(models.Strain)
    if taxon_id is not None:
        query = query.where(models.Strain.taxon_id == taxon_id)
    if origin_country:
        query = query.where(models.Strain.origin_country.ilike(f"%{origin_country}%"))
    return list(db.scalars(query.order_by(models.Strain.strain_code)))


def create_strain(db: Session, strain: schemas.StrainCreate) -> models.Strain:
    existing = db.scalar(select(models.Strain).where(models.Strain.strain_code == strain.strain_code))
    if existing:
        return existing
    record = models.Strain(**strain.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_sequences(
    db: Session,
    strain_id: int | None = None,
    marker: str | None = None,
) -> list[models.SequenceRecord]:
    query = select(models.SequenceRecord)
    if strain_id is not None:
        query = query.where(models.SequenceRecord.strain_id == strain_id)
    if marker:
        query = query.where(models.SequenceRecord.marker.ilike(f"%{marker}%"))
    return list(db.scalars(query.order_by(models.SequenceRecord.marker, models.SequenceRecord.id)))


def create_sequence(db: Session, sequence: schemas.SequenceCreate) -> models.SequenceRecord:
    existing = db.scalar(
        select(models.SequenceRecord).where(
            models.SequenceRecord.strain_id == sequence.strain_id,
            models.SequenceRecord.marker == sequence.marker,
        )
    )
    if existing:
        return existing
    record = models.SequenceRecord(**sequence.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def list_datasets(db: Session) -> list[models.Dataset]:
    return list(db.scalars(select(models.Dataset).order_by(models.Dataset.identifier)))


def create_dataset(db: Session, dataset: schemas.DatasetCreate) -> models.Dataset:
    existing = db.scalar(select(models.Dataset).where(models.Dataset.identifier == dataset.identifier))
    if existing:
        return existing
    payload = dataset.model_dump()
    payload["keywords"] = ",".join(dataset.keywords)
    record = models.Dataset(**payload)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
