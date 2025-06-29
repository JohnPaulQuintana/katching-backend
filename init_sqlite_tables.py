from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Settings, Expense  # Make sure these models exist
from datetime import datetime

# SQLite setup
SQLITE_URL = "sqlite:///./kaching.db"
engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Seed data
db = SessionLocal()
try:
    # Add settings (budget)
    if not db.query(Settings).filter_by(id=1).first():
        db.add(Settings(id=1, budget=15000))

    # Add a sample expense
    if not db.query(Expense).first():
        db.add(Expense(
            date=datetime(2025, 6, 20),
            amount=320.50,
            category="food",
            note="Lunch at Jollibee"
        ))

    db.commit()
    print("✅ Tables created and seeded in SQLite")
except Exception as e:
    db.rollback()
    print("❌ Error seeding data:", e)
finally:
    db.close()
