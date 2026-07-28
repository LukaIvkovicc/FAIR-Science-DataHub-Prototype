from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Taxon(Base):
    __tablename__ = "taxa"

    id: Mapped[int] = mapped_column(primary_key=True)
    scientific_name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    kingdom: Mapped[str] = mapped_column(String(80))
    phylum: Mapped[str | None] = mapped_column(String(120), nullable=True)
    family: Mapped[str | None] = mapped_column(String(120), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    strains: Mapped[list["Strain"]] = relationship(back_populates="taxon")


class Strain(Base):
    __tablename__ = "strains"

    id: Mapped[int] = mapped_column(primary_key=True)
    strain_code: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    taxon_id: Mapped[int] = mapped_column(ForeignKey("taxa.id"))
    origin_country: Mapped[str | None] = mapped_column(String(80), nullable=True)
    isolation_source: Mapped[str | None] = mapped_column(String(160), nullable=True)
    collected_on: Mapped[date | None] = mapped_column(Date, nullable=True)
    provenance: Mapped[str] = mapped_column(Text, default="Synthetic example record")

    taxon: Mapped[Taxon] = relationship(back_populates="strains")
    sequences: Mapped[list["SequenceRecord"]] = relationship(back_populates="strain")
    traits: Mapped[list["Trait"]] = relationship(back_populates="strain")


class SequenceRecord(Base):
    __tablename__ = "sequences"
    __table_args__ = (UniqueConstraint("strain_id", "marker", name="uq_sequence_strain_marker"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    strain_id: Mapped[int] = mapped_column(ForeignKey("strains.id"))
    marker: Mapped[str] = mapped_column(String(40))
    accession: Mapped[str | None] = mapped_column(String(80), nullable=True)
    sequence: Mapped[str] = mapped_column(Text)
    quality_note: Mapped[str | None] = mapped_column(String(160), nullable=True)

    strain: Mapped[Strain] = relationship(back_populates="sequences")


class Trait(Base):
    __tablename__ = "traits"

    id: Mapped[int] = mapped_column(primary_key=True)
    strain_id: Mapped[int] = mapped_column(ForeignKey("strains.id"))
    trait_name: Mapped[str] = mapped_column(String(120))
    trait_value: Mapped[str] = mapped_column(String(120))
    unit: Mapped[str | None] = mapped_column(String(40), nullable=True)

    strain: Mapped[Strain] = relationship(back_populates="traits")


class Dataset(Base):
    __tablename__ = "datasets"

    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    license: Mapped[str] = mapped_column(String(120))
    creator: Mapped[str] = mapped_column(String(160))
    keywords: Mapped[str] = mapped_column(String(255), default="")
    landing_page: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

