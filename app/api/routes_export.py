from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.metadata_export import build_fair_metadata_export

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/metadata")
def export_metadata(db: Session = Depends(get_db)) -> dict[str, object]:
    return build_fair_metadata_export(db)

