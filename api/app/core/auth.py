from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.repositories.member import get_active_member_by_id


'''
第 1 關：有沒有 Cookie 裡的 access_token
第 2 關：JWT 是否有效、未過期
第 3 關：member 是否存在而且 is_active = true'''
def get_current_member(
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("access_token")

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:
        member_id = decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    member = get_active_member_by_id(db, member_id)

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Member not found or inactive"
        )

    return member