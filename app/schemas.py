from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaxonBase(BaseModel):
    scientific_name: str = Field(min_length=3, max_length=255)
    kingdom: str = Field(min_length=3, max_length=80)
    phylum: str | None = None
    family: str | None = None


class TaxonCreate(TaxonBase):
    pass


class TaxonRead(TaxonBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class StrainBase(BaseModel):
    strain_code: str = Field(min_length=2, max_length=80)
    taxon_id: int = Field(gt=0)
    origin_country: str | None = None
    isolation_source: str | None = None
    collected_on: date | None = None
    provenance: str = "Synthetic example record"


class StrainCreate(StrainBase):
    pass


class StrainRead(StrainBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SequenceBase(BaseModel):
    strain_id: int = Field(gt=0)
    marker: str = Field(min_length=2, max_length=40)
    accession: str | None = None
    sequence: str = Field(min_length=10)
    quality_note: str | None = None

    @field_validator("sequence")
    @classmethod
    def sequence_uses_iupac_dna(cls, value: str) -> str:
        allowed = set("ACGTRYSWKMBDHVN-")
        normalized = value.upper()
        invalid = sorted(set(normalized) - allowed)
        if invalid:
            raise ValueError(f"sequence contains non-IUPAC DNA symbols: {', '.join(invalid)}")
        return normalized


class SequenceCreate(SequenceBase):
    pass


class SequenceRead(SequenceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TraitCreate(BaseModel):
    strain_id: int
    trait_name: str
    trait_value: str
    unit: str | None = None


class DatasetBase(BaseModel):
    identifier: str = Field(min_length=3, max_length=120)
    title: str = Field(min_length=5, max_length=255)
    description: str = Field(min_length=20)
    license: str
    creator: str
    keywords: list[str] = Field(default_factory=list)
    landing_page: str | None = None


class DatasetCreate(DatasetBase):
    pass


class DatasetRead(DatasetBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
