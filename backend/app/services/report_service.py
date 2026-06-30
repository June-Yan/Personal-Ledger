from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from app.models import Bill, Category


def get_monthly_summary(db: Session, user_id: int, year: int, month: int):
    from decimal import Decimal
    results = db.query(
        Category.type,
        func.sum(Bill.amount).label("total")
    ).join(Bill, Bill.category_id == Category.id).filter(
        Bill.user_id == user_id,
        extract("year", Bill.bill_date) == year,
        extract("month", Bill.bill_date) == month
    ).group_by(Category.type).all()

    income_total = Decimal("0")
    expense_total = Decimal("0")
    for row in results:
        if row.type == "income":
            income_total = Decimal(str(row.total or 0))
        else:
            expense_total = Decimal(str(row.total or 0))

    return {
        "income_total": income_total,
        "expense_total": expense_total,
        "balance": income_total - expense_total
    }


def get_category_breakdown(db: Session, user_id: int, year: int, month: int):
    from decimal import Decimal
    results = db.query(
        Category.id.label("category_id"),
        Category.name.label("category_name"),
        func.sum(Bill.amount).label("amount")
    ).join(Bill, Bill.category_id == Category.id).filter(
        Bill.user_id == user_id,
        Category.type == "expense",
        extract("year", Bill.bill_date) == year,
        extract("month", Bill.bill_date) == month
    ).group_by(Category.id, Category.name).order_by(func.sum(Bill.amount).desc()).all()

    total = sum(Decimal(str(r.amount or 0)) for r in results)
    data = []
    for r in results:
        amount = Decimal(str(r.amount or 0))
        data.append({
            "category_id": r.category_id,
            "category_name": r.category_name,
            "amount": amount,
            "percentage": round(float(amount / total * 100), 2) if total > 0 else 0
        })
    return data
