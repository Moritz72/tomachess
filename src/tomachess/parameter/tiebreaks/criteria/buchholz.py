from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypeVar
from uuid import UUID

from tomachess.parameter.tiebreaks.criteria.abstract_criterium import AbstractCriterium
from tomachess.state.results import FinalizedGameResult, IndividualResult

if TYPE_CHECKING:
    from tomachess.base import AbstractTournamentBase

T = TypeVar("T", bound="AbstractTournamentBase[Any]")


class Buchholz(AbstractCriterium[T]):
    type: Literal["buchholz"] = "buchholz"

    @staticmethod
    def _get_game_individual_score(
            uuid: UUID,
            uuid_opp: UUID | None,
            result: IndividualResult,
            point_score_dict: dict[UUID, float]
    ) -> float:
        if result.unplayed:
            return point_score_dict[uuid]
        assert uuid_opp is not None
        return point_score_dict[uuid_opp]

    def _handle_game_scores(
            self,
            game: FinalizedGameResult,
            point_score_dict: dict[UUID, float],
            buho_score_dict: dict[UUID, float]
    ) -> None:
        uuid_1 = game.uuid_1
        uuid_2 = game.uuid_2
        if uuid_1 is not None:
            score = self._get_game_individual_score(uuid_1, uuid_2, game.result_1, point_score_dict)
            buho_score_dict[uuid_1] += score
        if uuid_2 is not None:
            score = self._get_game_individual_score(uuid_2, uuid_1, game.result_2, point_score_dict)
            buho_score_dict[uuid_2] += score

    def compute_tiebreak(self, tournament: T) -> dict[UUID, float]:
        point_score_dict = self._get_point_scores(tournament)
        buho_score_dict = {uuid: 0.0 for uuid in tournament.get_participant_uuids()}

        for round_result in tournament.states.results.rounds:
            for game in round_result.items:
                self._handle_game_scores(game, point_score_dict, buho_score_dict)

        return buho_score_dict
