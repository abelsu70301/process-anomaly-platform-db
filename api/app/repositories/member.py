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
        db.query(Member)
        .filter(Member.google_sub == google_sub)
        .first()
    )

    if member is None:
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

#JWT → decode 得到 member_id = 1 → 查 member.mid = 1 → 再確認 is_active = true → 才算目前有效的登入者
def get_active_member_by_id(
    db: Session,
    member_id: int
) -> Member | None:
    return (
        db.query(Member)
        .filter(
            Member.mid == member_id,
            Member.is_active.is_(True)
        )
        .first()
    )
