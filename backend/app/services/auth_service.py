from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import User, Category
from app.schemas.user import UserCreate, UserLoginPassword, UserLoginCode
from app.utils.security import get_password_hash, verify_password, create_access_token
from app.utils.email import verify_code, create_verification_code, can_send_code


PRESET_CATEGORIES = [
    {"name": "餐饮", "type": "expense", "icon": "food", "sort_order": 1, "is_preset": True},
    {"name": "交通", "type": "expense", "icon": "transport", "sort_order": 2, "is_preset": True},
    {"name": "购物", "type": "expense", "icon": "shopping", "sort_order": 3, "is_preset": True},
    {"name": "娱乐", "type": "expense", "icon": "entertainment", "sort_order": 4, "is_preset": True},
    {"name": "住房", "type": "expense", "icon": "housing", "sort_order": 5, "is_preset": True},
    {"name": "收入", "type": "income", "icon": "income", "sort_order": 6, "is_preset": True},
]


def create_preset_categories(db: Session, user_id: int):
    for cat in PRESET_CATEGORIES:
        db_cat = Category(user_id=user_id, **cat)
        db.add(db_cat)
    db.commit()


def register_user(db: Session, data: UserCreate):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="邮箱已注册")

    if not verify_code(db, data.email, data.code):
        raise HTTPException(status_code=400, detail="验证码错误或已过期")

    user = User(
        email=data.email,
        password_hash=get_password_hash(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    create_preset_categories(db, user.id)

    token = create_access_token(user.id)
    return {"token": token, "user": {"id": user.id, "email": user.email}}


def login_with_password(db: Session, data: UserLoginPassword):
    user = db.query(User).filter(User.email == data.email, User.is_active == True).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="邮箱或密码错误")
    token = create_access_token(user.id)
    return {"token": token, "user": {"id": user.id, "email": user.email}}


def login_with_code(db: Session, data: UserLoginCode):
    if not verify_code(db, data.email, data.code):
        raise HTTPException(status_code=400, detail="验证码错误或已过期")

    user = db.query(User).filter(User.email == data.email, User.is_active == True).first()
    if user:
        token = create_access_token(user.id)
        return {"token": token, "user": {"id": user.id, "email": user.email}}

    # Auto register
    user = User(email=data.email, password_hash=get_password_hash(data.code))
    db.add(user)
    db.commit()
    db.refresh(user)
    create_preset_categories(db, user.id)
    token = create_access_token(user.id)
    return {"token": token, "user": {"id": user.id, "email": user.email}}


def send_code(db: Session, email: str):
    if not can_send_code(db, email):
        raise HTTPException(status_code=400, detail="验证码发送过于频繁，请稍后再试")
    create_verification_code(db, email)
    return {"message": "验证码已发送"}


def delete_account(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    db.query(Category).filter(Category.user_id == user_id).delete()
    from app.models import Bill
    db.query(Bill).filter(Bill.user_id == user_id).delete()
    db.delete(user)
    db.commit()
    return {"message": "账户已注销"}
