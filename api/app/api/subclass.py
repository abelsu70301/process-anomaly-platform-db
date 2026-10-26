from fastapi import APIRouter, Depends  #APIRounter:管理這組API路徑/Depends：讓 FastAPI 幫我們取得 DB session
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import get_db

router = APIRouter(prefix="/subclass", tags=["subclass"])
#prefix="/subclass"：這個檔案底下的 API 都會以 /subclass 開頭

@router.get("/pcid/{id}")
def get_subclass(id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT * FROM vd_subclass WHERE pcid = :pcid"),
        {"pcid": id}
    )

    rows = result.mappings().all()
    return rows

#GET /api/subclass/objectlist/cid/2
@router.get("/objectlist/cid/{id}")
def get_objectlist(id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT * FROM vd_objectlist WHERE cid = :cid ORDER BY oid"),
        {"cid": id}
    )

    rows = result.mappings().all()
    return rows

#vd_object 的單筆詳細資料 API
@router.get("/object/{id}")
def get_object(id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT * FROM vd_object WHERE oid = :oid"),
        {"oid": id}
    )

    row = result.mappings().first()
    return row
