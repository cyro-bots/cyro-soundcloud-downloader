from datetime import datetime, timezone
from typing import Type, TypeVar

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    select,
    update,
)

from app.database import Base

from . import get_session

T = TypeVar("T", bound="Base")


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(125), unique=True, nullable=False, index=True)
    created_at = Column(
        DateTime(timezone=True), server_default="CURRENT_TIMESTAMP"
    )
    expire_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Channel(username='{self.username}', active={self.is_active})>"

    @classmethod
    async def get_active_channels(cls: Type[T]) -> list[str]:
        """Returns a list of active channel usernames (UTC-aware)."""
        async with get_session() as session:
            now = datetime.now(timezone.utc)
            result = await session.execute(
                select(cls.username)
                .where(cls.is_active == True)
                .where((cls.expire_at == None) | (cls.expire_at > now))
            )
            return [row[0] for row in result.fetchall()]

    @classmethod
    async def add_channel(
        cls: Type[T], username: str, expire_at: datetime | None = None
    ) -> T:
        """Add a new channel or update expire date if exists."""
        async with get_session() as session:
            result = await session.execute(
                select(cls).where(cls.username == username)
            )
            channel = result.scalar_one_or_none()
            if channel:
                channel.expire_at = expire_at
            else:
                channel = cls(username=username, expire_at=expire_at)
                session.add(channel)
            await session.commit()
            return channel

    @classmethod
    async def deactivate_channel(cls: Type[T], username: str) -> bool:
        """Deactivate a channel manually."""
        async with get_session() as session:
            stmt = (
                update(cls)
                .where(cls.username == username)
                .values(is_active=False)
            )
            await session.execute(stmt)
            await session.commit()
            return True
