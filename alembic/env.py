from logging.config import fileConfig
import sys
import os

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# ─────────────── Paths ───────────────
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()  # ← أضف السطر ده

# ─────────────── Import Models & Base ───────────────
from app.database import Base
from app.models import (
    Student,
    Book,
    student_book,
    Course,
    student_course,
    User,
    UserCV,
    Document,
    DocumentChunk,
    Embedding,
    Chat,
    ChatMessage
)

from pgvector.sqlalchemy import Vector
from sqlalchemy import event
from sqlalchemy.engine import Engine
# ─────────────── Alembic Config ───────────────
config = context.config

# ← أضف السطرين دول عشان يقرأ من .env
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()