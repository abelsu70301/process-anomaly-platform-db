import psycopg

import os #載入Ｐython 內建的os模組，會透過它取得“環境變數”
from dotenv import load_dotenv #從剛安裝的python-dotenv 套件中，把load_dotenv()功能載入進來


load_dotenv() #會去讀專案內的.env，把裡面的DATABASE_URL...載入成環境變數

DATABASE_URL = os.getenv("DATABASE_URL")
#從環境變數取得名稱叫做 DATABASE_URL 的值，存到 Python 的 DATABASE_URL 變數

with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT current_database(), current_user;")
        result = cur.fetchone()
        print(result)
        