import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()  # Load .env file for local dev

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kaching.db")
print(f"🔍 DATABASE_URL being used: {DATABASE_URL}")

# Neon requires SSL
connect_args = {"sslmode": "require"} if "neon.tech" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
