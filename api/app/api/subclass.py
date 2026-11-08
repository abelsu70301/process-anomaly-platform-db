from fastapi import APIRouter, Depends, Query  #APIRounter:管理這組API路徑/Depends：讓 FastAPI 幫我們取得 DB session
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import get_db
from app.core.auth import get_current_member

from app.repositories.subclass import get_subclasses_by_pcid, get_objects_by_cid, get_object_by_oid

router = APIRouter(
    prefix="/subclass",
    tags=["subclass"],
    dependencies=[Depends(get_current_member)]
)
#prefix="/subclass"：這個檔案底下的 API 都會以 /subclass 開頭

@router.get("/pcid/{id}")
def get_subclass(id: int, db: Session = Depends(get_db)):  #呼叫 repository 共用函式
    return get_subclasses_by_pcid(db, id)  #repository 查 vd_subclass，並回傳結果


#GET /api/subclass/objectlist/cid/2
@router.get("/objectlist/cid/{id}")
def get_objectlist(
    id: int,  #id 決定要查哪個 cid
    page: int = Query(1, ge=1),  #page 預設第1頁  #必須 >=1
    page_size: int = Query(2, ge=1, le=100),  #page_size 預設每頁兩筆  #必須 <=100
    class_name: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db)
):
    return get_objects_by_cid(db, id, page, page_size, class_name, search)

#vd_object 的單筆詳細資料 API
@router.get("/object/{id}")
def get_object(id: int, db: Session = Depends(get_db)):
    return get_object_by_oid(db, id)
