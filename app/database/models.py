from datetime import datetime
from typing import Tuple, Type, TypeVar

from sqlalchemy import Boolean, Column, DateTime, Integer, Select, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func, select, update

from app.database import Base

from . import get_session

T = TypeVar("T", bound="Base")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(125), nullable=False)
    fullname = Column(String(125), nullable=False)
    language = Column(String(5), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    last_process_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=False)

    def __repr__(self):
        return f"<User(ChatId='{self.chat_id}', Username='{self.username}')>"

    @classmethod
    async def set_user_language(cls: Type[T], chat_id: int, lang: str) -> bool:
        async with get_session() as session:
            result = await session.execute(
                select(cls).where(cls.chat_id == chat_id)
            )
            user = result.scalar_one_or_none()
            if user:
                user.language = lang
                await session.commit()
                return True
            return False

    @classmethod
    async def get_user_language(cls: Type[T], chat_id: int) -> str:
        async with get_session() as session:
            result = await session.execute(
                select(cls.language).where(cls.chat_id == chat_id)
            )
            lang = result.scalar_one_or_none()
            return lang or "en"

    @classmethod
    async def get_or_create(
        cls: Type[T],
        chat_id: str,
        fullname: str,
        username: str,
    ) -> Tuple[T, bool]:
        """Gets a user by ChatId, or creates a new one. This is a complete transaction."""
        async with get_session() as session:
            result = await session.execute(
                select(cls).where(cls.chat_id == chat_id)
            )
            user = result.scalar_one_or_none()
            if not user:
                user = cls(
                    chat_id=chat_id, fullname=fullname, username=username
                )
                session.add(user)
                await session.commit()
                return user, True
            return user, False

    @classmethod
    async def update_last_processing(
        cls: Type[T], session: AsyncSession, chat_id: str
    ) -> None:
        """Updates the last processing time. A complete transaction."""
        stmt = (
            update(cls)
            .where(cls.chat_id == chat_id)
            .values(last_process_at=datetime.now())
        )
        await session.execute(stmt)
        await session.commit()

    # --- Direct Execution ---
    @classmethod
    async def set_language(
        cls: Type[T], session: AsyncSession, chat_id: str, lang: str
    ) -> T:
        """Creates or updates a language entry. Mimics INSERT OR REPLACE."""

        lang_entry = await session.merge(cls(chat_id=chat_id, language=lang))
        await session.commit()
        return lang_entry

    # --- Query Builder ---
    @classmethod
    def select_language(cls: Type[T], chat_id: str) -> Select:
        """Returns a Select statement for the language of a given user."""

        return select(cls.language).where(cls.chat_id == chat_id)
