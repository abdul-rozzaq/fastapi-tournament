import os
import dotenv

dotenv.load_dotenv()

from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


class Base(DeclarativeBase):
    pass


DATABASE_URL = os.getenv("DATABASE_URL")

# check_same_thread: False
# engine = create_engine(url=DATABASE_URL, echo=True)
engine = create_async_engine(url=DATABASE_URL)

# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore
