from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import models


def build_fair_metadata_export(db: Session) -> dict[str, object]:
    dataset = db.scalar(select(models.Dataset).order_by(models.Dataset.identifier))
    taxa_count = db.scalar(select(func.count(models.Taxon.id))) or 0
    strain_count = db.scalar(select(func.count(models.Strain.id))) or 0
    sequence_count = db.scalar(select(func.count(models.SequenceRecord.id))) or 0

    if dataset is None:
        return {
            "@context": "https://schema.org",
            "@type": "Dataset",
            "name": "Empty FAIR scientific data hub prototype",
            "description": "No dataset metadata has been loaded yet.",
            "isAccessibleForFree": True,
            "measurementTechnique": [],
            "variableMeasured": [],
        }

    keywords = [keyword for keyword in dataset.keywords.split(",") if keyword]
    return {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "@id": dataset.identifier,
        "name": dataset.title,
        "description": dataset.description,
        "license": dataset.license,
        "creator": {"@type": "Organization", "name": dataset.creator},
        "keywords": keywords,
        "url": dataset.landing_page,
        "isAccessibleForFree": True,
        "includedInDataCatalog": {
            "@type": "DataCatalog",
            "name": "FAIR Scientific Data Hub Prototype",
        },
        "measurementTechnique": ["DNA marker sequence", "phenotypic trait observation"],
        "variableMeasured": ["taxon", "strain", "sequence marker", "trait"],
        "distribution": {
            "@type": "DataDownload",
            "encodingFormat": "application/json",
            "contentUrl": "/export/metadata",
        },
        "additionalProperty": [
            {"name": "taxa_count", "value": taxa_count},
            {"name": "strain_count", "value": strain_count},
            {"name": "sequence_count", "value": sequence_count},
            {"name": "provenance_note", "value": "Synthetic data for portfolio demonstration only."},
        ],
    }

