from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal

router = APIRouter()

@router.get("/budget", response_model=schemas.BudgetOut)
def get_budget():
    db: Session = SessionLocal()
    try:
        setting = db.query(models.Settings).filter_by(id=1).first()
        return {"budget": setting.budget if setting else 10000}
    finally:
        db.close()

@router.post("/budget", response_model=schemas.BudgetOut)
def set_budget(b: schemas.BudgetOut):
    db: Session = SessionLocal()
    try:
        setting = db.query(models.Settings).filter_by(id=1).first()
        if setting:
            setting.budget = b.budget
        else:
            setting = models.Settings(id=1, budget=b.budget)
            db.add(setting)
        db.commit()
        return {"budget": b.budget}
    finally:
        db.close()
