from sqlalchemy.orm import Session
from sqlalchemy import text


def get_subclasses_by_pcid(
    db: Session,
    pcid: int
):
    result = db.execute(
        text(
            "SELECT * FROM public.vd_subclass "
            "WHERE pcid = :pcid "
            "ORDER BY cid"
        ),
        {"pcid": pcid}
    )

    return result.mappings().all()

def get_objects_by_cid(
    db: Session,
    cid: int,
    page: int,
    page_size: int,
    class_name: str | None = None,
    search: str | None = None
):
    offset = (page - 1) * page_size

    sql = """
        SELECT *
        FROM public.vd_objectlist
        WHERE cid = :cid
    """

    params = {
        "cid": cid,
        "page_size": page_size,
        "offset": offset
    }

    if class_name is not None:  #有傳class_name :加上篩選條件，若沒有 :不篩選，只照原本查
        sql += "AND class_name = :class_name"
        params["class_name"] = class_name

    if search is not None:
        sql += "AND object_title ILIKE :search"
        params["search"] = f"%{search}%"

    sql += " ORDER BY oid LIMIT :page_size OFFSET :offset"

    result = db.execute(
        text(sql),
        params
    )

    return result.mappings().all()

def get_object_by_oid(  #輸入oid
    db: Session,
    oid: int
):
    result = db.execute(
        text(  #查 public.vd_object
            "SELECT * FROM public.vd_object "
            "WHERE oid = :oid"
        ),
        {"oid": oid}  #回傳單一 Object 的詳細資料
    )

    return result.mappings().first()