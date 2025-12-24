from backend.app.config import DATABASE_URL_SYNC

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL_SYNC)
SessionLocal = sessionmaker(bind=engine)