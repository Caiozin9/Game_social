from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.game_list import GameList
    from app.models.review import Review
    from app.models.user_game import UserGame


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    bio: Mapped[str | None] = mapped_column(Text)
    avatar_url: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # passive_deletes=True: quem apaga os filhos é o ON DELETE CASCADE do banco
    user_games: Mapped[list["UserGame"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )
    lists: Mapped[list["GameList"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )
