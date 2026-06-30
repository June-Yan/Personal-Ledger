from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


class BillBase(BaseModel):
    amount: Decimal = Field(..., gt=0)
    category_id: int
    note: Optional[str] = Field(None, max_length=200)
    bill_date: date


class BillCreate(BillBase):
    pass


class BillUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0)
    category_id: Optional[int] = None
    note: Optional[str] = Field(None, max_length=200)
    bill_date: Optional[date] = None


class BillResponse(BaseModel):
    id: int
    amount: Decimal
    category_id: int
    category_name: str
    category_type: str
    note: Optional[str]
    bill_date: date
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BillListResponse(BaseModel):
    items: list[BillResponse]
    total: int
    page: int
    page_size: int
