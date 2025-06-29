from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal
from ml_utils import train_model, predict_category, generate_tags
from datetime import datetime

router = APIRouter()
@router.get("/expenses")
def get_expenses():
    db: Session = SessionLocal()
    try:
        expenses = db.query(models.Expense).order_by(models.Expense.date.desc()).all()
        return [
            {
                "id": e.id,
                "date": e.date.isoformat(),
                "amount": e.amount,
                "category": e.category,
                "note": e.note,
                "tags": generate_tags(e.note)
            } for e in expenses
        ]
    finally:
        db.close()

@router.post("/expenses")
def add_expense(expense: schemas.ExpenseIn):
    db: Session = SessionLocal()
    try:
        if not expense.category:
            train_model(db)
            expense.category = predict_category(expense.note)

        new_exp = models.Expense(
            date=expense.date,
            amount=expense.amount,
            category=expense.category,
            note=expense.note,
        )
        db.add(new_exp)
        db.commit()
        db.refresh(new_exp)
        return {"message": "Expense added successfully!", "category": expense.category}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
