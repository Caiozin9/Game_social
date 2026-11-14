from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.game_list import GameListItem
    from app.models.review import Review
    from app.models.user_game import UserGame


class Game(Base):
    """Cache local dos jogos da IGDB (evita consultar a API a cada request)."""

    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    igdb_id: Mapped[int] = mapped_column(unique=True)
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    cover_url: Mapped[str | None] = mapped_column(String(500))
    release_date: Mapped[date | None] = mapped_column(Date)
    # Última sincronização com a IGDB: base para decidir quando revalidar
    synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user_games: Mapped[list["UserGame"]] = relationship(
        back_populates="game", cascade="all, delete-orphan", passive_deletes=True
    )
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="game", cascade="all, delete-orphan", passive_deletes=True
    )
    list_items: Mapped[list["GameListItem"]] = relationship(
        back_populates="game", cascade="all, delete-orphan", passive_deletes=True
    )
