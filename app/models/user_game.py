import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    SmallInteger,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.game import Game
    from app.models.user import User


class GameStatus(str, enum.Enum):
    playing = "playing"
    completed = "completed"
    dropped = "dropped"
    wishlist = "wishlist"


class UserGame(Base):
    """Relação do usuário com um jogo: status + nota."""

    __tablename__ = "user_games"
    __table_args__ = (
        UniqueConstraint("user_id", "game_id", name="uq_user_games_user_id_game_id"),
        CheckConstraint("rating IS NULL OR rating BETWEEN 1 AND 10", name="rating_range"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"))
    status: Mapped[GameStatus] = mapped_column(
        Enum(
            GameStatus,
            name="game_status",
            values_callable=lambda e: [m.value for m in e],
        )
    )
    rating: Mapped[int | None] = mapped_column(SmallInteger)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="user_games")
    game: Mapped["Game"] = relationship(back_populates="user_games")
