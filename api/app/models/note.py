from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, func
#這些都是 SQLAlchemy 用來描述資料表欄位的工具
#Integer → 整數 ; String(200) → 最多 200 字元的字串 ; Text → 較長文字 ; DateTime → 日期時間 ; Boolean → True / False ; func.now() → 呼叫資料庫端的目前時間函式 

from app.core.database import Base
#把剛剛 database.py 建立的 Base = declarative_base() 拿進來用

class Note(Base) :  #Note 是一個 SQLAlchemy ORM Model，也就是 Python 的 Note class 會對應一張資料表
    __tablename__ = "notes"  #在告訴 SQLAlchemy ，這個 Model 對應 PostgreSQL 裡名稱叫 notes 的 table

    id = Column(Integer, primary_key = True, index = True)  #欄位名稱：id;型別：Integer;primary_key=True：主鍵;index=True：建立 index，讓用 id 查詢通常更快
    title = Column(String(200), nullable = False)  #title 是最多 200 字元的字串，而且不能是 NULL
    content = Column(Text, nullable = True)  #content 可以放較長文字，而且允許 NULL
    created_at = Column(DateTime, server_default = func.now())  #created_at 是日期時間欄位，如果 Python 沒有傳值，就讓「資料庫伺服器」自己填現在時間
    is_archived = Column(Boolean, nullable=False, default=False)  #is_archived 是 Boolean，不能是 NULL，Python ORM 新增資料時預設值是 False