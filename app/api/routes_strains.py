from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db

router = APIRouter(prefix="/strains", tags=["strains"])


@router.get("", response_model=list[schemas.StrainRead])
def read_strains(
    taxon_id: int | None = None,
    origin_country: str | None = None,
    db: Session = Depends(get_db),
) -> list[schemas.StrainRead]:
    return crud.list_strains(db, taxon_id=taxon_id, origin_country=origin_country)


@router.post("", response_model=schemas.StrainRead, status_code=201)
def add_strain(strain: schemas.StrainCreate, db: Session = Depends(get_db)) -> schemas.StrainRead:
    if db.get(models.Taxon, strain.taxon_id) is None:
        raise HTTPException(status_code=404, detail=f"Taxon {strain.taxon_id} was not found")
    return crud.create_strain(db, strain)
