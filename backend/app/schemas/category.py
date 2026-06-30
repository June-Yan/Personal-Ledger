from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    type: str = Field(..., pattern="^(income|expense)$")
    icon: Optional[str] = None
    sort_order: int = 0


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    icon: Optional[str] = None
    sort_order: Optional[int] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    type: str
    icon: Optional[str]
    sort_order: int
    is_preset: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
