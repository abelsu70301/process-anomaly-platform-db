import os  #讀環境變數
import psycopg  #python 和 postgreSQL 溝通的套件

#收到一筆 Log 資料，連到 PostgreSQL，然後把它 INSERT 進 public.api_logs
DATABASE_URL = os.environ["DATABASE_URL"]  #取得資料庫連線字串
#從目前系統環境中取得名為 DATABASE_URL 的值


async def save_log(data):  #async def 表示這個函式可以在等待資料庫 I/O 時把執行權讓出去
    async with await psycopg.AsyncConnection.connect(DATABASE_URL) as conn:  #使用 DATABASE_URL 連上 PostgreSQL
        async with conn.cursor() as cur:  #conn 是「資料庫連線」  #cur 是 cursor，真正拿來送 SQL 指令給 PostgreSQL 的工具
            await cur.execute(  #請 PostgreSQL 執行下面這段 SQL  #await: 表示「這裡要等資料庫結果，但等待期間 event loop 可以安排其他工作」
                """
                INSERT INTO public.api_logs (
                    session_id,
                    request_id,
                    method,
                    path,
                    status_code,
                    duration_ms,
                    error_code,
                    message
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,  #新增一筆 Log  #%: 這是 psycopg 的 SQL parameter placeholder
                (
                    data["session_id"],
                    data["request_id"],
                    data["method"],
                    data["path"],
                    data["status_code"],
                    data["duration_ms"],
                    data["error_code"],
                    data["message"]
                )  #會依序代入前面的 %s
            )

async def save_session(session_id, ip, mid):
    async with await psycopg.AsyncConnection.connect(DATABASE_URL) as conn:
        async with conn.cursor() as cur:
            await cur.execute(  #如果 session_id 不存在 → INSERT 一筆新的 api_sessions
                """
                INSERT INTO public.api_sessions (id, mid, ip)
                VALUES(%s, %s, %s)
                ON CONFLICT (id)
                DO UPDATE SET
                    mid = COALESCE(EXCLUDED.mid, api_sessions.mid),
                    last_seen_at = NOW()
                """,  #EXCLUDED.mid: 這次原本準備 INSERT 進去的 mid  #COALESCE(): 如果 EXCLUDED.mid 有值，就用新的mid
                (session_id, mid, ip)
            )  #如果 session_id 已經存在 → 只更新 last_seen_at