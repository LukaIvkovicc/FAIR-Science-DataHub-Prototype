from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/taxa", tags=["taxa"])


@router.get("", response_model=list[schemas.TaxonRead])
def read_taxa(db: Session = Depends(get_db)) -> list[schemas.TaxonRead]:
    return crud.list_taxa(db)


@router.post("", response_model=schemas.TaxonRead, status_code=201)
def add_taxon(taxon: schemas.TaxonCreate, db: Session = Depends(get_db)) -> schemas.TaxonRead:
    return crud.create_taxon(db, taxon)

