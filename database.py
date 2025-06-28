from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 🔥 TEMPORARY: Force the correct driver while Vercel env is broken
DATABASE_URL = "postgresql+psycopg2://neondb_owner:npg_R9JVBvXKL3HA@ep-cold-surf-a4hr81l9-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"

connect_args = {"sslmode": "require"}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
