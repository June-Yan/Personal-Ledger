from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserLoginPassword, UserLoginCode, SendCodeRequest
from app.services import auth_service
from app.middleware.auth import get_current_user_id

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    result = auth_service.register_user(db, data)
    return {"code": 0, "message": "注册成功", "data": result}


@router.post("/login/password")
def login_password(data: UserLoginPassword, db: Session = Depends(get_db)):
    result = auth_service.login_with_password(db, data)
    return {"code": 0, "message": "登录成功", "data": result}


@router.post("/login/code")
def login_code(data: UserLoginCode, db: Session = Depends(get_db)):
    result = auth_service.login_with_code(db, data)
    return {"code": 0, "message": "登录成功", "data": result}


@router.post("/send-code")
def send_code(data: SendCodeRequest, db: Session = Depends(get_db)):
    result = auth_service.send_code(db, data.email)
    return {"code": 0, "message": result["message"], "data": None}


@router.post("/logout")
def logout(user_id: int = Depends(get_current_user_id)):
    return {"code": 0, "message": "已退出登录", "data": None}


@router.delete("/account")
def delete_account(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    result = auth_service.delete_account(db, user_id)
    return {"code": 0, "message": result["message"], "data": None}
