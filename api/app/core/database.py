import os  #匯入內建的os模組，主要是為了後面使用os.getenv("DATABASE_URL") 去讀環境變數

from dotenv import load_dotenv  #dotenv 是安裝的 python-dotenv 套件，把 .env 檔案裡的設定載入到程式執行環境裡
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


load_dotenv()  #就是先讀 .env

DATABASE_URL = os.getenv("DATABASE_URL")  #告訴 SQLAlchemy PostgreSQL 在哪裡
#從環境變數裡取得名稱叫 DATABASE_URL 的值

if not DATABASE_URL :
    raise RuntimeError("DATABASE_URL is not set")
#如果程式沒有成功取得 DATABASE_URL，就直接停止並明確告訴我們原因


DATABASE_URL = DATABASE_URL.replace(  #將..改成..
    "postgresql://",
    "postgresql+psycopg://",  #postgresql = 我要連 PostgreSQL  #psycopg = 我要透過 psycopg 這個 driver 去連
    1
)


engine = create_engine(DATABASE_URL) #engine 是 SQLAlchemy 與 PostgreSQL 溝通的核心入口

SessionLocal = sessionmaker(  #SessionLocal：每次操作資料時產生 Session
    autocommit = False,  #不要每做一個修改就自動 commit
    autoflush = False,  #不要在某些操作前自動把尚未提交的變更送到 DB
    bind = engine  #這個 Session 要使用哪個 Engine
)
#sessionmaker() 是：建立 Session 的「工廠」
#SessionLocal 則是之後真正操作資料時，用來產生 Session 的「工廠」
#Session 的作用是：Python 程式實際跟資料庫做查詢、新增、修改、刪除時使用的工作區

Base = declarative_base()  #Base：讓之後的 ORM model，例如 Note，可以被 SQLAlchemy 當成資料表模型
#建立：SQLAlchemy ORM model 的共同 Base class

def get_db():  #這個函式是給 FastAPI 用的，每個 FastAPI request 需要 DB 時，幫它開一個 Session，用完再關掉
    db = SessionLocal()  #建立一個 Session
    try : 
        yield db  #yield：把這個 DB Session 暫時交給 API 使用
    finally :
        db.close()  #不管 API：正常完成/出錯 最後都會把session關掉
    #若一直不關資料庫連線資源可能一直被占用