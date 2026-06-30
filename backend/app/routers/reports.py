from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import report_service
from app.middleware.auth import get_current_user_id

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/monthly-summary")
def monthly_summary(
    year: int = Query(...),
    month: int = Query(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    data = report_service.get_monthly_summary(db, user_id, year, month)
    return {
        "code": 0,
        "message": "success",
        "data": {
            "income_total": float(data["income_total"]),
            "expense_total": float(data["expense_total"]),
            "balance": float(data["balance"])
        }
    }


@router.get("/category-breakdown")
def category_breakdown(
    year: int = Query(...),
    month: int = Query(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    data = report_service.get_category_breakdown(db, user_id, year, month)
    return {"code": 0, "message": "success", "data": data}
