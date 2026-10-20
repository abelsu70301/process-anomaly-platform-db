from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NoteCreate(BaseModel):  #NoteCreate = Client → API
    title: str
    content: Optional[str] = None  #代表 content 可以不填


class NoteResponse(BaseModel):  #NoteResponse = APIS → Client
    id: int
    title: str
    content: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True  #是讓 Pydantic 可以直接把 SQLAlchemy ORM 物件轉成 NoteResponse