from abc import ABC, abstractmethod
from typing import Sequence

from tomachess.participant import Player, Team
from tomachess.union_type import Tournament, TeamTournament


class AbstractStore(ABC):
    @abstractmethod
    def save_players(self, collection: str, player: Sequence[Player]) -> None:
        pass

    @abstractmethod
    def load_players(self, collection: str) -> list[Player]:
        pass

    @abstractmethod
    def save_teams(self, collection: str, teams: Sequence[Team]) -> None:
        pass

    @abstractmethod
    def load_teams(self, collection: str) -> list[Team]:
        pass

    @abstractmethod
    def save_tournaments(self, collection: str, tournaments: Sequence[Tournament]) -> None:
        pass

    @abstractmethod
    def load_tournaments(self, collection: str) -> list[Tournament]:
        pass

    @abstractmethod
    def save_team_tournaments(self, collection: str, team_tournaments: Sequence[TeamTournament]) -> None:
        pass

    @abstractmethod
    def load_team_tournaments(self, collection: str) -> list[TeamTournament]:
        pass
