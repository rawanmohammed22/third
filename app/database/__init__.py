# app/database/__init__.py

# الملف الحقيقي اسمه db.py (مش database.py)
from .db import Base, engine, SessionLocal, get_db ,create_all_tables

