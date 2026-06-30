from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.JWT_EXPIRY_DAYS)
    to_encode = {"sub": str(user_id), "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def decode_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = int(payload.get("sub"))
        return user_id
    except (JWTError, ValueError, TypeError):
        return None
