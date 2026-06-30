from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Bill, Category
from app.schemas.bill import BillCreate, BillUpdate


def get_bills(db: Session, user_id: int, year: int, month: int, page: int = 1, page_size: int = 20):
    from sqlalchemy import extract, desc
    query = db.query(Bill).filter(
        Bill.user_id == user_id,
        extract("year", Bill.bill_date) == year,
        extract("month", Bill.bill_date) == month
    ).order_by(desc(Bill.bill_date), desc(Bill.created_at))
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return items, total


def get_bill(db: Session, user_id: int, bill_id: int):
    return db.query(Bill).filter(Bill.id == bill_id, Bill.user_id == user_id).first()


def create_bill(db: Session, user_id: int, data: BillCreate):
    cat = db.query(Category).filter(Category.id == data.category_id, Category.user_id == user_id).first()
    if not cat:
        raise HTTPException(status_code=400, detail="分类不存在")
    bill = Bill(user_id=user_id, **data.model_dump())
    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill


def update_bill(db: Session, user_id: int, bill_id: int, data: BillUpdate):
    bill = db.query(Bill).filter(Bill.id == bill_id, Bill.user_id == user_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="账单不存在")
    if data.category_id is not None:
        cat = db.query(Category).filter(Category.id == data.category_id, Category.user_id == user_id).first()
        if not cat:
            raise HTTPException(status_code=400, detail="分类不存在")
        bill.category_id = data.category_id
    if data.amount is not None:
        bill.amount = data.amount
    if data.note is not None:
        bill.note = data.note
    if data.bill_date is not None:
        bill.bill_date = data.bill_date
    db.commit()
    db.refresh(bill)
    return bill


def delete_bill(db: Session, user_id: int, bill_id: int):
    bill = db.query(Bill).filter(Bill.id == bill_id, Bill.user_id == user_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="账单不存在")
    db.delete(bill)
    db.commit()
    return {"message": "删除成功"}
