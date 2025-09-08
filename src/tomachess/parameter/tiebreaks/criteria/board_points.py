from __future__ import annotations

from typing import TYPE_CHECKING, Literal
from uuid import UUID

from tomachess.parameter.scoring_system import ScoringSystem
from tomachess.parameter.tiebreaks.criteria.abstract_criterium import AbstractCriterium
from tomachess.state.team_results import FinalizedTeamGameResult

if TYPE_CHECKING:
    from tomachess.base import TeamTournamentBase


class BoardPoints(AbstractCriterium["TeamTournamentBase"]):
    type: Literal["board_points"] = "board_points"

    @staticmethod
    def _handle_team_game_scores(
            team_game: FinalizedTeamGameResult,
            scoring_system: ScoringSystem,
            buho_score_dict: dict[UUID, float]
    ) -> None:
        uuid_1 = team_game.team_1
        uuid_2 = team_game.team_2
        if uuid_1 is not None:
            score = sum(scoring_system.get_points(game.result_1) for game in team_game.items)
            buho_score_dict[uuid_1] += score
        if uuid_2 is not None:
            score = sum(scoring_system.get_points(game.result_2) for game in team_game.items)
            buho_score_dict[uuid_2] += score

    def compute_tiebreak(self, tournament: TeamTournamentBase) -> dict[UUID, float]:
        scoring_system = tournament.parameters.board_scoring_system
        bopo_score_dict = {uuid: 0.0 for uuid in tournament.get_participant_uuids()}

        for round_result in tournament.states.team_results.rounds:
            for team_game in round_result.items:
                self._handle_team_game_scores(team_game, scoring_system, bopo_score_dict)

        return bopo_score_dict
