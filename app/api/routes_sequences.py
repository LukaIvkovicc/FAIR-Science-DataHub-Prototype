from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db

router = APIRouter(prefix="/sequences", tags=["sequences"])


@router.get("", response_model=list[schemas.SequenceRead])
def read_sequences(
    strain_id: int | None = None,
    marker: str | None = None,
    db: Session = Depends(get_db),
) -> list[schemas.SequenceRead]:
    return crud.list_sequences(db, strain_id=strain_id, marker=marker)


@router.post("", response_model=schemas.SequenceRead, status_code=201)
def add_sequence(sequence: schemas.SequenceCreate, db: Session = Depends(get_db)) -> schemas.SequenceRead:
    if db.get(models.Strain, sequence.strain_id) is None:
        raise HTTPException(status_code=404, detail=f"Strain {sequence.strain_id} was not found")
    return crud.create_sequence(db, sequence)
