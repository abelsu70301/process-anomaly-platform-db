#建立 JWT
import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv


load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ACCESS_TOKEN_EXPIRE_SECONDS = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", "3600")
)
#先去 .env 找 ACCESS_TOKEN_EXPIRE_SECONDS
#→ 如果有，就用你設定的值
#→ 如果沒有，就預設用 3600 秒

JWT_ALGORITHM = "HS256"


if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not set")


def create_access_token(member_id: int) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(member_id),
        "iat": now,
        "exp": now + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS),
    }

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    return token

#反方向
def decode_access_token(token: str) -> int:
    payload = jwt.decode(  #不只是「把 JWT 拆開看內容」，它還會驗證
        token,
        JWT_SECRET_KEY,
        algorithms=[JWT_ALGORITHM],
    )

    member_id = payload.get("sub")  #把我們建立 token 時放進去的"sub"：拿回來

    if member_id is None:
        raise ValueError("Token does not contain sub")

    return int(member_id)