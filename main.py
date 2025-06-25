from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, SessionLocal
import models
from passlib.context import CryptContext
import auth, savings, goals
from datetime import datetime, timedelta

import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.100.173:5173", "https://stately-crisp-569e1b.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def create_default_user():
    db = SessionLocal()
    if not db.query(models.User).first():
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        user = models.User(name="JP QUINTANA",username="admin", password=pwd_context.hash("password123"))
        db.add(user)
        db.commit()
    db.close()

def seed_savings():
    db = SessionLocal()
    user = db.query(models.User).first()
    if user and not db.query(models.Saving).filter_by(user_id=user.id).first():
        # Historical seed
        savings_per_year = {
            2025: 10,
            2024: 15,
            2023: 20,
        }

        for year, count in savings_per_year.items():
            for _ in range(count):
                random_day = random.randint(1, 28)
                random_month = random.randint(1, 12)
                date = datetime(year, random_month, random_day)
                db.add(models.Saving(
                    amount=round(random.uniform(20, 500), 2),
                    date=date,
                    user_id=user.id
                ))

        
        now = datetime.now()
        for _ in range(5):  # number of entries for current month
            random_day = random.randint(1, 28)
            date = datetime(now.year, now.month, random_day)
            db.add(models.Saving(
                amount=round(random.uniform(20, 500), 2),
                date=date,
                user_id=user.id
            ))

        db.commit()
    db.close()



def seed_goal():
    db = SessionLocal()
    user = db.query(models.User).first()
    if user and not db.query(models.Goal).filter_by(user_id=user.id).first():
        db.add(models.Goal(
            target_amount=10000,
            user_id=user.id
        ))
        db.commit()
    db.close()


create_default_user()
seed_savings()
seed_goal()

# app.include_router(auth.router, prefix="/api/auth")
app.include_router(auth.router, prefix="/api/auth")
app.include_router(savings.router, prefix="/api/savings")
app.include_router(goals.router, prefix="/api/goals")