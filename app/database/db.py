from pathlib import Path
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Try local app/database/.env first, then project-root .env
BASE_DIR = Path(__file__).resolve().parent
ENV_CANDIDATES = [
    BASE_DIR / ".env",
    BASE_DIR.parent.parent / ".env",
]

for env_file in ENV_CANDIDATES:
    if env_file.exists():
        load_dotenv(dotenv_path=env_file)
        break

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    searched_paths = ", ".join(str(path) for path in ENV_CANDIDATES)
    raise ValueError(f"DATABASE_URL ?? ????? ?? ??? .env. ?? ????? ??: {searched_paths}")

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_all_tables():
    Base.metadata.create_all(bind=engine)
