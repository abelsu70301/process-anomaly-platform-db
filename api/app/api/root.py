from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.subclass import get_subclasses_by_pcid


router = APIRouter(
    prefix="/root",
    tags=["root"]
)


@router.get("")
def get_root(db: Session = Depends(get_db)):
    return get_subclasses_by_pcid(db, 0)