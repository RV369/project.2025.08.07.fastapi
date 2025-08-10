from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    with SessionLocal() as session:
        try:
            yield session
        finally:
            session.close()
