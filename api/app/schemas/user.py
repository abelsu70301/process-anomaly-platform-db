from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):  #UserCreate = 新增 User 時 API 要收到的資料
    email: str
    hashed_password: str


class UserResponse(BaseModel):  #UserResponse = API 回傳 User 時的資料格式
    id: int
    email: str
    hashed_password: str
    created_at: datetime

    class Config:
        from_attributes = True