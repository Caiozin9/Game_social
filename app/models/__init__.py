"""Importa todos os models para que o Alembic os enxergue no metadata."""

from app.models.game import Game
from app.models.game_list import GameList, GameListItem
from app.models.review import Review
from app.models.user import User
from app.models.user_game import GameStatus, UserGame

__all__ = [
    "Game",
    "GameList",
    "GameListItem",
    "GameStatus",
    "Review",
    "User",
    "UserGame",
]
