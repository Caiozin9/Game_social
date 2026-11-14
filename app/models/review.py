from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.game import Game
    from app.models.user import User


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        # Uma review por usuário por jogo
        UniqueConstraint("user_id", "game_id", name="uq_reviews_user_id_game_id"),
        # Perfil: "reviews do usuário X, mais recentes primeiro"
        Index("ix_reviews_user_id_created_at", "user_id", "created_at"),
        # Página do jogo: "reviews do jogo Y, mais recentes primeiro"
        Index("ix_reviews_game_id_created_at", "game_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="reviews")
    game: Mapped["Game"] = relationship(back_populates="reviews")
