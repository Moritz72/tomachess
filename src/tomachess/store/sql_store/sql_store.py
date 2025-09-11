from typing import Sequence, Type, TypeVar
from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine, select

from tomachess.participant import Player, Team
from tomachess.store.abstract_store import AbstractStore
from tomachess.store.sql_store.player_row import PlayerRow
from tomachess.store.sql_store.team_row import TeamRow
from tomachess.store.sql_store.team_tournament_row import TeamTournamentRow
from tomachess.store.sql_store.tournament_row import TournamentRow
from tomachess.union_type import Tournament, TeamTournament

T = TypeVar("T", bound=SQLModel)


class SqlStore(AbstractStore):
    def __init__(self, file_path: Path) -> None:
        self.engine = create_engine(f"sqlite:///{file_path}", future=True)
        SQLModel.metadata.create_all(self.engine)

    def _save_models(self, models: Sequence[T]) -> None:
        if not models:
            return

        with Session(self.engine) as session:  # type: ignore[attr-defined]
            for m in models:
                session.merge(m)
            session.commit()

    def _load_models(self, model_type: Type[T]) -> list[T]:
        with Session(self.engine) as session:  # type: ignore[attr-defined]
            rows = session.exec(select(model_type)).all()
            return list(rows)

    def save_players(self, collection: str, players: Sequence[Player]) -> None:
        rows = [PlayerRow.from_collection_player(player, collection) for player in players]
        self._save_models(rows)

    def load_players(self, collection: str) -> list[Player]:
        rows = self._load_models(PlayerRow)
        return [row.to_player() for row in rows]

    def save_teams(self, collection: str, teams: Sequence[Team]) -> None:
        rows = [TeamRow.from_team(team, collection) for team in teams]
        self._save_models(rows)

    def load_teams(self, collection: str) -> list[Team]:
        rows = self._load_models(TeamRow)
        return [row.to_team() for row in rows]

    def save_tournaments(self, collection: str, tournaments: Sequence[Tournament]) -> None:
        rows = [TournamentRow.from_tournament(tournament, collection) for tournament in tournaments]
        self._save_models(rows)

    def load_tournaments(self, collection: str) -> list[Tournament]:
        rows = self._load_models(TournamentRow)
        return [row.to_tournament() for row in rows]

    def save_team_tournaments(self, collection: str, team_tournaments: Sequence[TeamTournament]) -> None:
        rows = [TeamTournamentRow.from_team_tournament(tournament, collection) for tournament in team_tournaments]
        self._save_models(rows)

    def load_team_tournaments(self, collection: str) -> list[TeamTournament]:
        rows = self._load_models(TeamTournamentRow)
        return [row.to_team_tournament() for row in rows]
