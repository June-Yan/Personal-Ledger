from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.bill import BillCreate, BillUpdate
from app.services import bill_service
from app.middleware.auth import get_current_user_id

router = APIRouter(prefix="/api/bills", tags=["bills"])


@router.get("")
def list_bills(
    year: int = Query(...),
    month: int = Query(...),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    items, total = bill_service.get_bills(db, user_id, year, month, page, page_size)
    # Enrich with category info
    from app.models import Category
    data = []
    for bill in items:
        cat = db.query(Category).filter(Category.id == bill.category_id).first()
        data.append({
            "id": bill.id,
            "amount": float(bill.amount),
            "category_id": bill.category_id,
            "category_name": cat.name if cat else "未分类",
            "category_type": cat.type if cat else "expense",
            "note": bill.note,
            "bill_date": str(bill.bill_date),
            "created_at": bill.created_at.isoformat() if bill.created_at else None
        })
    return {
        "code": 0,
        "message": "success",
        "data": {"items": data, "total": total, "page": page, "page_size": page_size}
    }


@router.post("")
def create_bill(data: BillCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    bill = bill_service.create_bill(db, user_id, data)
    cat = db.query(bill.__class__.__bases__[0]).session.query(bill.__class__).get(bill.id) if False else None
    # Re-fetch to enrich
    from app.models import Category
    cat = db.query(Category).filter(Category.id == bill.category_id).first()
    return {
        "code": 0,
        "message": "创建成功",
        "data": {
            "id": bill.id,
            "amount": float(bill.amount),
            "category_id": bill.category_id,
            "category_name": cat.name if cat else "未分类",
            "category_type": cat.type if cat else "expense",
            "note": bill.note,
            "bill_date": str(bill.bill_date),
            "created_at": bill.created_at.isoformat() if bill.created_at else None
        }
    }


@router.put("/{bill_id}")
def update_bill(bill_id: int, data: BillUpdate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    bill = bill_service.update_bill(db, user_id, bill_id, data)
    from app.models import Category
    cat = db.query(Category).filter(Category.id == bill.category_id).first()
    return {
        "code": 0,
        "message": "更新成功",
        "data": {
            "id": bill.id,
            "amount": float(bill.amount),
            "category_id": bill.category_id,
            "category_name": cat.name if cat else "未分类",
            "category_type": cat.type if cat else "expense",
            "note": bill.note,
            "bill_date": str(bill.bill_date),
            "created_at": bill.created_at.isoformat() if bill.created_at else None
        }
    }


@router.delete("/{bill_id}")
def delete_bill(bill_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    result = bill_service.delete_bill(db, user_id, bill_id)
    return {"code": 0, "message": result["message"], "data": None}
