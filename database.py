import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()  # Load .env file for local dev

DATABASE_URL = os.getenv("DATABASE_URL_Origin", "postgresql+psycopg2://neondb_owner:npg_R9JVBvXKL3HA@ep-cold-surf-a4hr81l9-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require")
print(f"🔍 DATABASE_URL_Origin being used: {DATABASE_URL}")

# Neon requires SSL
connect_args = {"sslmode": "require"} if "neon.tech" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
