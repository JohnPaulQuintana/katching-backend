import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

import models  # Make sure this contains your User, Saving, Goal models
from database import Base  # To initialize tables on Neon if not done

load_dotenv()

# Paths
SQLITE_URL = "sqlite:///./kaching.db"
NEON_URL = "postgresql+psycopg2://neondb_owner:npg_R9JVBvXKL3HA@ep-cold-surf-a4hr81l9-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

# Engines
sqlite_engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
neon_engine = create_engine(NEON_URL, connect_args={"sslmode": "require"})

# Sessions
SQLiteSession = sessionmaker(bind=sqlite_engine)
NeonSession = sessionmaker(bind=neon_engine)

sqlite_db = SQLiteSession()
neon_db = NeonSession()

# OPTIONAL: Create tables in Neon if they don't exist
Base.metadata.create_all(bind=neon_engine)

try:
     # === MIGRATE SETTINGS ===
    settings = sqlite_db.query(models.Settings).all()
    for s in settings:
        neon_db.add(models.Settings(
            id=s.id,
            budget=s.budget
        ))

    neon_db.commit()
    print(f"✅ Migrated {len(settings)} settings.")

    # === MIGRATE EXPENSES ===
    expenses = sqlite_db.query(models.Expense).all()
    for e in expenses:
        neon_db.add(models.Expense(
            id=e.id,
            date=e.date,
            amount=e.amount,
            category=e.category,
            note=e.note
        ))

    neon_db.commit()
    print(f"✅ Migrated {len(expenses)} expenses.")

    # === MIGRATE USERS ===
    users = sqlite_db.query(models.User).all()
    for user in users:
        exists = neon_db.query(models.User).filter_by(username=user.username).first()
        if not exists:
            neon_db.add(models.User(
                id=user.id,
                name=user.name,
                username=user.username,
                password=user.password
            ))

    neon_db.commit()
    print(f"✅ Migrated {len(users)} users.")

    # === MIGRATE SAVINGS ===
    savings = sqlite_db.query(models.Saving).all()
    for s in savings:
        neon_db.add(models.Saving(
            id=s.id,
            amount=s.amount,
            date=s.date,
            user_id=s.user_id
        ))

    neon_db.commit()
    print(f"✅ Migrated {len(savings)} savings.")

    # === MIGRATE GOALS ===
    goals = sqlite_db.query(models.Goal).all()
    for g in goals:
        neon_db.add(models.Goal(
            id=g.id,
            target_amount=g.target_amount,
            user_id=g.user_id
        ))

    neon_db.commit()
    print(f"✅ Migrated {len(goals)} goals.")

except Exception as e:
    print("❌ Error during migration:", e)
    neon_db.rollback()

finally:
    sqlite_db.close()
    neon_db.close()
