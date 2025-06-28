import os
import random
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext

from database import Base, engine, SessionLocal
import models
import auth, savings, goals
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://192.168.100.173:5173",
        "https://katching.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional: Only auto-create tables in development
if os.getenv("AUTO_CREATE_TABLES", "true").lower() == "true":
    Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def on_startup():
    if os.getenv("SEED_DATA", "false").lower() == "true":
        create_default_user()
        seed_savings()
        seed_goal()


@app.get("/health")
def health_check():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


def create_default_user():
    db = SessionLocal()
    try:
        if not db.query(models.User).first():
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            user = models.User(
                name="JP QUINTANA",
                username="admin",
                password=pwd_context.hash("password123")
            )
            db.add(user)
            db.commit()
    finally:
        db.close()


def seed_savings():
    db = SessionLocal()
    try:
        user = db.query(models.User).first()
        if user and not db.query(models.Saving).filter_by(user_id=user.id).first():
            savings_per_year = {
                2025: 10,
                2024: 15,
                2023: 20,
            }

            for year, count in savings_per_year.items():
                for _ in range(count):
                    date = datetime(year, random.randint(1, 12), random.randint(1, 28))
                    db.add(models.Saving(
                        amount=round(random.uniform(20, 500), 2),
                        date=date,
                        user_id=user.id
                    ))

            now = datetime.now()
            for _ in range(5):
                date = datetime(now.year, now.month, random.randint(1, 28))
                db.add(models.Saving(
                    amount=round(random.uniform(20, 500), 2),
                    date=date,
                    user_id=user.id
                ))

            db.commit()
    finally:
        db.close()


def seed_goal():
    db = SessionLocal()
    try:
        user = db.query(models.User).first()
        if user and not db.query(models.Goal).filter_by(user_id=user.id).first():
            db.add(models.Goal(target_amount=10000, user_id=user.id))
            db.commit()
    finally:
        db.close()


# Register routers
app.include_router(auth.router, prefix="/api/auth")
app.include_router(savings.router, prefix="/api/savings")
app.include_router(goals.router, prefix="/api/goals")
