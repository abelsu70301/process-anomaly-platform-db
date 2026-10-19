import psycopg  #載入 PostgreSQL Driver

import os #載入Ｐython 內建的os模組，會透過它取得“環境變數”
from dotenv import load_dotenv #從剛安裝的python-dotenv 套件中，把load_dotenv()功能載入進來


load_dotenv() #找目前專案中的.env，把裡面的設定(DATABASE_URL...)載入成環境變數

DATABASE_URL = os.getenv("DATABASE_URL")
#去環境變數取得名稱叫做 DATABASE_URL 的值，存到 Python 的 DATABASE_URL 變數
#左邊是Python變數，右邊是在讀環境變數

with psycopg.connect(DATABASE_URL) as conn:  #使用剛讀到的 DATABASE_URL 連線 PostgreSQL，並把這條連線命名成 conn
    with conn.cursor() as cur:  #從這條 database connection 建立一個 cursor
        cur.execute("SELECT current_database(), current_user;")  #把 SQL 送給 PostgreSQL 執行
        result = cur.fetchone()  #把查詢結果取回一筆
        print(result)


'''
PostgreSQL：DBMS  
Database：fastapi_dev
User/Role：dev_user
.env：保存環境設定與敏感連線資訊
DATABASE_URL：Database connection string
psycopg：Python ↔ PostgreSQL driver
Connection / Cursor：連線與執行 SQL 的物件
CREATE / INSERT / SELECT：建表、新增、查詢
'''