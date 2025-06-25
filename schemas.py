from pydantic import BaseModel
from datetime import datetime

class SavingBase(BaseModel):
    amount: float

class SavingOut(SavingBase):
    id: int
    date: datetime

    model_config = {"from_attributes": True}

class GoalBase(BaseModel):
    target_amount: float

class GoalOut(GoalBase):
    id: int
    model_config = {"from_attributes": True}

class TokenOut(BaseModel):
    name: str
    access_token: str
    token_type: str