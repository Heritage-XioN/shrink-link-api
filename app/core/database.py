from sqlmodel import SQLModel, Session, create_engine, func, select, text, update
from sqlalchemy import event
from app.models.user import User
from app.models.urls import Urls
from app.core.config import settings
import logging
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



DB_URL = f"{settings.DB_DRIVER}://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOSTNAME}:{settings.DB_PORT}/{settings.DB_NAME}"
engine = create_engine(DB_URL,pool_size=10,max_overflow=20, pool_pre_ping=True)

# creates database connectuon
# def get_session():
#     with Session(engine) as session:
#         yield session

# Configure logging

def get_session():
    with Session(engine) as session:
        try:
            yield session
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred: {e}")
            session.rollback()

            # Optionally, re-raise or handle the error as needed
            raise
        finally:
            session.close()
