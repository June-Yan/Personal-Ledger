from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date, DECIMAL, ForeignKey, Index
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    is_active = Column(Boolean, default=True)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(50), nullable=False)
    type = Column(String(10), nullable=False)  # income / expense
    icon = Column(String(50), default=None)
    sort_order = Column(Integer, default=0)
    is_preset = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("ix_categories_user_id_name", "user_id", "name", unique=True),
    )


class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    amount = Column(DECIMAL(12, 2), nullable=False)
    note = Column(String(200), default=None)
    bill_date = Column(Date, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("ix_bills_user_id_bill_date", "user_id", "bill_date"),
        Index("ix_bills_user_id_category_id", "user_id", "category_id"),
    )


class VerificationCode(Base):
    __tablename__ = "verification_codes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    code = Column(String(6), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("ix_verification_codes_email_code", "email", "code"),
    )
