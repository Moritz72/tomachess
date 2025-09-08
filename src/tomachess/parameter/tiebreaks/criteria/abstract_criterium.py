from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel

if TYPE_CHECKING:
    from tomachess.base import AbstractTournamentBase

T = TypeVar("T", bound="AbstractTournamentBase[Any]")


class AbstractCriterium(BaseModel, Generic[T], ABC):
    type: str

    @staticmethod
    def _get_point_scores(tournament: T) -> dict[UUID, float]:
        scoring_system = tournament.parameters.scoring_system
        point_score_dict = {uuid: 0.0 for uuid in tournament.get_participant_dict().keys()}

        for round_result in tournament.states.results.rounds:
            for game in round_result.items:
                if game.uuid_1 is not None:
                    point_score_dict[game.uuid_1] += scoring_system.get_points(game.result_1)
                if game.uuid_2 is not None:
                    point_score_dict[game.uuid_2] += scoring_system.get_points(game.result_2)

        return point_score_dict

    @abstractmethod
    def compute_tiebreak(self, tournament: T) -> dict[UUID, float]:
        pass
