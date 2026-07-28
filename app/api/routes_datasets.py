from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db

router = APIRouter(prefix="/datasets", tags=["datasets"])


def _to_schema(dataset: models.Dataset) -> schemas.DatasetRead:
    return schemas.DatasetRead(
        id=dataset.id,
        identifier=dataset.identifier,
        title=dataset.title,
        description=dataset.description,
        license=dataset.license,
        creator=dataset.creator,
        keywords=[item for item in dataset.keywords.split(",") if item],
        landing_page=dataset.landing_page,
    )


@router.get("", response_model=list[schemas.DatasetRead])
def read_datasets(db: Session = Depends(get_db)) -> list[schemas.DatasetRead]:
    return [_to_schema(dataset) for dataset in crud.list_datasets(db)]


@router.post("", response_model=schemas.DatasetRead, status_code=201)
def add_dataset(dataset: schemas.DatasetCreate, db: Session = Depends(get_db)) -> schemas.DatasetRead:
    return _to_schema(crud.create_dataset(db, dataset))

