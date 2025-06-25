from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import models, schemas
from auth import get_current_user, get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.SavingOut])
def get_savings(
    from_date: datetime = Query(None),
    to_date: datetime = Query(None),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user)
):
    query = db.query(models.Saving).filter(models.Saving.user_id == user.id)
    if from_date:
        query = query.filter(models.Saving.date >= from_date)
    if to_date:
        query = query.filter(models.Saving.date <= to_date)
    return query.order_by(models.Saving.date.desc()).all()


@router.post("/", response_model=schemas.SavingOut)
def create_saving(data: schemas.SavingBase, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    saving = models.Saving(amount=data.amount, user_id=user.id)
    db.add(saving)
    db.commit()
    db.refresh(saving)
    return saving


@router.delete("/{saving_id}")
def delete_saving(saving_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    saving = db.query(models.Saving).filter_by(id=saving_id, user_id=user.id).first()
    if not saving:
        raise HTTPException(status_code=404, detail="Saving not found")
    db.delete(saving)
    db.commit()
    return {"message": "Deleted successfully"}