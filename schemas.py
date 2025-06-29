from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# =========================
# SAVING SCHEMAS
# =========================

class SavingBase(BaseModel):
    amount: float

class SavingOut(SavingBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True  # Required for returning SQLAlchemy objects


# =========================
# GOAL SCHEMAS
# =========================

class GoalBase(BaseModel):
    target_amount: float

class GoalOut(GoalBase):
    id: int

    class Config:
        orm_mode = True  # Required for returning SQLAlchemy objects


# =========================
# AUTH SCHEMA
# =========================

class TokenOut(BaseModel):
    name: str
    access_token: str
    token_type: str


# =========================
# Budget SCHEMA
# =========================
class BudgetOut(BaseModel):
    budget: float

    class Config:
        orm_mode = True

class ExpenseIn(BaseModel):
    date: str
    amount: float
    category: Optional[str] = ""
    note: str

class ExpenseOut(BaseModel):
    id: int
    date: str
    amount: float
    category: str
    note: str
    tags: list[str]