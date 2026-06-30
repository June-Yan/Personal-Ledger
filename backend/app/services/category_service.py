from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Category, Bill
from app.schemas.category import CategoryCreate, CategoryUpdate


def get_categories(db: Session, user_id: int):
    return db.query(Category).filter(Category.user_id == user_id).order_by(Category.sort_order, Category.id).all()


def create_category(db: Session, user_id: int, data: CategoryCreate):
    existing = db.query(Category).filter(
        Category.user_id == user_id, Category.name == data.name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="分类名称已存在")
    cat = Category(user_id=user_id, **data.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


def update_category(db: Session, user_id: int, category_id: int, data: CategoryUpdate):
    cat = db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="分类不存在")
    if data.name is not None:
        existing = db.query(Category).filter(
            Category.user_id == user_id, Category.name == data.name, Category.id != category_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="分类名称已存在")
        cat.name = data.name
    if data.icon is not None:
        cat.icon = data.icon
    if data.sort_order is not None:
        cat.sort_order = data.sort_order
    db.commit()
    db.refresh(cat)
    return cat


def delete_category(db: Session, user_id: int, category_id: int, confirm: bool = False):
    cat = db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="分类不存在")

    bill_count = db.query(Bill).filter(Bill.category_id == category_id, Bill.user_id == user_id).count()
    if bill_count > 0 and not confirm:
        raise HTTPException(
            status_code=400,
            detail=f"该分类下有 {bill_count} 条账单记录，删除分类将同时删除关联账单，是否继续？",
        )

    db.query(Bill).filter(Bill.category_id == category_id, Bill.user_id == user_id).delete()
    db.delete(cat)
    db.commit()
    return {"message": "删除成功"}
