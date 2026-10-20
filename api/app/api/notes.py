from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteResponse


router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)
#表示這個檔案裡的 API 都以 /notes 開頭


@router.post("/", response_model=NoteResponse)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db)  #表示每個 API 需要操作資料庫時，都向 get_db() 取得 Session
):
    db_note = Note(**note.model_dump())

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note


@router.get("/", response_model=list[NoteResponse])
def list_notes(
    db: Session = Depends(get_db)
):
    return db.query(Note).all()


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(
        Note.id == note_id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return note


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_data: NoteCreate,
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(
        Note.id == note_id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    for key, value in note_data.model_dump().items():
        setattr(note, key, value)

    db.commit()
    db.refresh(note)

    return note


@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(
        Note.id == note_id
    ).first()

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )  #表示找不到 Note 時，不讓程式亂掉，而是正確回傳 404 Not Found

    db.delete(note)
    db.commit()

    return {"detail": "deleted"}