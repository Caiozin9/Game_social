from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
    func,
    true,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.game import Game
    from app.models.user import User


class GameList(Base):
    """Lista customizada do usuário (ex.: "Melhores de 2026")."""

    __tablename__ = "lists"
    __table_args__ = (Index("ix_lists_user_id", "user_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(120))
    description: Mapped[str | None] = mapped_column(Text)
    is_public: Mapped[bool] = mapped_column(Boolean, server_default=true())
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="lists")
    items: Mapped[list["GameListItem"]] = relationship(
        back_populates="game_list",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="GameListItem.position",
    )


class GameListItem(Base):
    __tablename__ = "list_items"
    __table_args__ = (
        UniqueConstraint("list_id", "game_id", name="uq_list_items_list_id_game_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    list_id: Mapped[int] = mapped_column(ForeignKey("lists.id", ondelete="CASCADE"))
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"))
    position: Mapped[int]

    game_list: Mapped["GameList"] = relationship(back_populates="items")
    game: Mapped["Game"] = relationship(back_populates="list_items")
