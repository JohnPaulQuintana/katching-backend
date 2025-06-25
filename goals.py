from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from auth import get_current_user, get_db

router = APIRouter()

@router.post("/", response_model=schemas.GoalOut)
def set_goal(data: schemas.GoalBase, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    goal = db.query(models.Goal).filter_by(user_id=user.id).first()
    if goal:
        goal.target_amount = data.target_amount
    else:
        goal = models.Goal(target_amount=data.target_amount, user_id=user.id)
        db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal

@router.put("/", response_model=schemas.GoalOut)
def update_goal(data: schemas.GoalBase, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    print("✅ PUT called. Payload:", data)
    goal = db.query(models.Goal).filter_by(user_id=user.id).first()
    print("🎯 Goal found:", goal)
    
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    goal.target_amount = data.target_amount
    db.commit()
    db.refresh(goal)
    return goal


@router.get("/", response_model=schemas.GoalOut)
def get_goal(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    goal = db.query(models.Goal).filter_by(user_id=user.id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not set")
    return goal
