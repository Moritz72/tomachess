from __future__ import annotations

from typing import TYPE_CHECKING, Self

from pydantic import BaseModel

from tomachess.state.results import FinalizedRoundResult
from tomachess.state.team_pairings import TeamParings
from tomachess.state.team_results.team_game_result import FinalizedTeamGameResult
from tomachess.type import RoundIndex

if TYPE_CHECKING:
    from tomachess.parameter import ScoringSystem


class TeamRoundResult(BaseModel):
    index: RoundIndex
    items: list[FinalizedTeamGameResult]

    @staticmethod
    def has_empty(team_round_result: TeamRoundResult) -> bool:
        return any(FinalizedTeamGameResult.is_empty(item) for item in team_round_result.items)

    @classmethod
    def get_empty_instance(cls, team_pairings: TeamParings) -> Self:
        items = [FinalizedTeamGameResult.get_empty_instance() for _ in range(len(team_pairings.items))]
        return cls(index=team_pairings.index, items=items)

    def get_round_result(self, board_scoring_system: ScoringSystem) -> FinalizedRoundResult:
        items = tuple(item.get_game_result(board_scoring_system) for item in self.items)
        return FinalizedRoundResult(index=self.index, items=items)
