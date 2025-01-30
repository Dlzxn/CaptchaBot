from sqlalchemy import Column, BigInteger, String, create_engine, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
import asyncio

from models.create_database import engine

engine = engine



Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String, nullable=True)
    captcha = Column(Boolean, nullable=False, default=False)
    is_admin = Column(Boolean, nullable=False, default=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# asyncio.run(create_tables())