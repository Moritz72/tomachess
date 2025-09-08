from __future__ import annotations

from typing import TYPE_CHECKING, Self, TypeGuard
from uuid import UUID

from pydantic import BaseModel

from tomachess.exceptions import ResultError
from tomachess.state.results import FinalizedGameResult, GameResult, IndividualResult
from tomachess.state.team_pairings import FinalizedTeamPairing

if TYPE_CHECKING:
    from tomachess.parameter import ScoringSystem


class TeamGameResult(BaseModel):
    team_1: UUID | None
    team_2: UUID | None
    items: tuple[GameResult, ...]

    @staticmethod
    def _determine_result(game_results: tuple[GameResult, ...]) -> tuple[IndividualResult, IndividualResult] | None:
        if all(item.result_1 == IndividualResult.VOLUNTARY_BYE for item in game_results):
            return IndividualResult.VOLUNTARY_BYE, IndividualResult.UNDEFINED
        if all(item.result_2 == IndividualResult.VOLUNTARY_BYE for item in game_results):
            return IndividualResult.UNDEFINED, IndividualResult.VOLUNTARY_BYE

        byes_1 = sum(item.result_1 == IndividualResult.PAIRING_ALLOCATED_BYE for item in game_results)
        byes_2 = sum(item.result_2 == IndividualResult.PAIRING_ALLOCATED_BYE for item in game_results)
        forfeit_1 = byes_1 > len(game_results) // 2
        forfeit_2 = byes_2 > len(game_results) // 2

        match (forfeit_1, forfeit_2):
            case (True, True):
                return IndividualResult.FORFEIT_LOSS, IndividualResult.FORFEIT_LOSS
            case (True, False):
                return IndividualResult.FORFEIT_LOSS, IndividualResult.FORFEIT_WIN
            case (False, True):
                return IndividualResult.FORFEIT_WIN, IndividualResult.FORFEIT_LOSS
            case _:
                return None

    @staticmethod
    def is_valid(team_result: TeamGameResult) -> bool:
        return all(GameResult.is_valid(item) for item in team_result.items)

    @staticmethod
    def is_finalized(team_result: TeamGameResult) -> TypeGuard[FinalizedTeamGameResult]:
        return all(GameResult.is_finalized(item) for item in team_result.items)

    @staticmethod
    def is_empty(team_result: TeamGameResult) -> bool:
        return not bool(team_result.items)

    @classmethod
    def from_team_pairing(cls, team_pairing: FinalizedTeamPairing) -> Self:
        items = tuple(GameResult.from_game_pairing(item) for item in team_pairing.items)
        return cls(team_1=team_pairing.team_1, team_2=team_pairing.team_2, items=items)

    @classmethod
    def get_empty_instance(cls) -> Self:
        return cls(team_1=None, team_2=None, items=())

    def _calculate_results(self, board_scoring_system: ScoringSystem) -> tuple[IndividualResult, IndividualResult]:
        if not TeamGameResult.is_finalized(self):
            raise ResultError("The results are not finalized")

        score_1 = sum(board_scoring_system.get_points(item.result_1) for item in self.items)
        score_2 = sum(board_scoring_system.get_points(item.result_2) for item in self.items)

        if score_1 == score_2:
            return IndividualResult.DRAW, IndividualResult.DRAW
        if score_1 > score_2:
            return IndividualResult.WIN, IndividualResult.LOSS
        return IndividualResult.LOSS, IndividualResult.WIN

    def get_team_pairing(self) -> FinalizedTeamPairing:
        items = tuple(GameResult.get_game_pairing(item) for item in self.items)
        return FinalizedTeamPairing(team_1=self.team_1, team_2=self.team_2, items=items)

    def get_game_result(self, board_scoring_system: ScoringSystem) -> FinalizedGameResult:
        results = TeamGameResult._determine_result(self.items)
        if results is None:
            result_1, result_2 = self._calculate_results(board_scoring_system)
        else:
            result_1, result_2 = results

        return FinalizedGameResult(uuid_1=self.team_1, uuid_2=self.team_2, result_1=result_1, result_2=result_2)


class FinalizedTeamGameResult(TeamGameResult):
    team_1: UUID | None
    team_2: UUID | None
    items: tuple[FinalizedGameResult, ...]

