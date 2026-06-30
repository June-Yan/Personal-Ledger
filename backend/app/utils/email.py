import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import VerificationCode


DEV_CODE = "123456"


def generate_code() -> str:
    return "".join([str(random.randint(0, 9)) for _ in range(6)])


def create_verification_code(db: Session, email: str) -> str:
    code = DEV_CODE
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    db_code = VerificationCode(email=email, code=code, expires_at=expires_at)
    db.add(db_code)
    db.commit()
    return code


def verify_code(db: Session, email: str, code: str, mark_used: bool = True) -> bool:
    if code != DEV_CODE:
        return False
    db_code = db.query(VerificationCode).filter(
        VerificationCode.email == email,
        VerificationCode.code == code,
        VerificationCode.used == False,
        VerificationCode.expires_at > datetime.utcnow()
    ).order_by(VerificationCode.created_at.desc()).first()
    if not db_code:
        return False
    if mark_used:
        db_code.used = True
        db.commit()
    return True


def mark_code_used(db: Session, email: str, code: str) -> None:
    db_code = db.query(VerificationCode).filter(
        VerificationCode.email == email,
        VerificationCode.code == code,
        VerificationCode.used == False
    ).order_by(VerificationCode.created_at.desc()).first()
    if db_code:
        db_code.used = True
        db.commit()


def can_send_code(db: Session, email: str) -> bool:
    last_code = db.query(VerificationCode).filter(
        VerificationCode.email == email
    ).order_by(VerificationCode.created_at.desc()).first()
    if not last_code:
        return True
    return datetime.utcnow() - last_code.created_at > timedelta(seconds=60)
