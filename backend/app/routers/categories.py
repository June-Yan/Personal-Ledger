from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services import category_service
from app.middleware.auth import get_current_user_id

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("")
def list_categories(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    items = category_service.get_categories(db, user_id)
    return {"code": 0, "message": "success", "data": items}


@router.post("")
def create_category(data: CategoryCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    item = category_service.create_category(db, user_id, data)
    return {"code": 0, "message": "创建成功", "data": item}


@router.put("/{category_id}")
def update_category(category_id: int, data: CategoryUpdate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    item = category_service.update_category(db, user_id, category_id, data)
    return {"code": 0, "message": "更新成功", "data": item}


@router.delete("/{category_id}")
def delete_category(category_id: int, confirm: bool = Query(False), user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    result = category_service.delete_category(db, user_id, category_id, confirm)
    return {"code": 0, "message": result["message"], "data": None}
