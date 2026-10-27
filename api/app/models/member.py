from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, func

from app.core.database import Base


class Member(Base):
    __tablename__ = "member"

    mid = Column(BigInteger, primary_key=True, index=True)
    google_sub = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    name = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    last_login = Column(DateTime, nullable=True)



from datetime import datetime
from sqlalchemy.orm import Session
from app.models.member import Member

def upsert_member(
    db: Session,
    google_sub: str,
    email: str,
    name: str | None
) -> Member:
    member = (
        db.query(Member) #查 member table
        .filter(Member.google_sub == google_sub)  # 用 Google sub 找同一個使用者
        .first()  #找第一筆符合資料
    )

    if member is None:  #代表第一次登入，所以新增
        member = Member(
            google_sub=google_sub,
            email=email,
            name=name,
            last_login=datetime.now()
        )

        db.add(member)

    else:
        member.email = email
        member.name = name
        member.last_login = datetime.now()

    db.commit()
    db.refresh(member)

    return member