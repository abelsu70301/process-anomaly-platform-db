from fastapi import APIRouter, Depends

from app.core.auth import get_current_member
from app.models.member import Member


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me")
def read_current_member(
    current_member: Member = Depends(get_current_member)  #FastAPI 在真正執行 /me 前，會先跑：get_current_member()
):
    return {
        "mid": current_member.mid,
        "email": current_member.email,
        "name": current_member.name,
    }