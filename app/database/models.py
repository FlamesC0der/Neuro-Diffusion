import os
from dotenv import load_dotenv

from sqlalchemy import BigInteger, String, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

load_dotenv()
engine = create_async_engine(os.getenv('SQLALCHEMY_DATABASE_URL'))

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    tokens = mapped_column(Integer, default=30)

    # stats
    images_generated = mapped_column(Integer, default=0)
    activated_promo_codes = mapped_column(String, default="")


class Prompt(Base):
    __tablename__ = "prompts"

    id: Mapped[int] = mapped_column(String, primary_key=True)
    prompt = mapped_column(String)
    user_id = mapped_column(BigInteger)


class Promocode(Base):
    __tablename__ = "promocodes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name = mapped_column(String)
    active = mapped_column(Boolean)
    value = mapped_column(Integer)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
