from sys import exception
from sqlmodel import SQLModel, Session, create_engine, func, select, text, update
from sqlalchemy import event
from app.models.user import User
from app.models.urls import Urls
from app.core.config import settings
from sqlalchemy.exc import SQLAlchemyError


DB_URL = f"{settings.DB_DRIVER}://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOSTNAME}:{settings.DB_PORT}/{settings.DB_NAME}"
engine = create_engine(DB_URL, pool_size=10,
                       max_overflow=20, pool_pre_ping=True)


def get_session():
    with Session(engine) as session:
        try:
            yield session
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()
