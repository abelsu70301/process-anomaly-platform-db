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
    cid: int
):
    result = db.execute(
        text(
            "SELECT * FROM public.vd_objectlist "
            "WHERE cid = :cid "
            "ORDER BY oid"
        ),
        {"cid": cid}
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