from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from tomachess.models import Standings, StandingsItem

if TYPE_CHECKING:
    from tomachess.base.tournament_base import TournamentBase, TeamTournamentBase

T = TypeVar("T", bound="TournamentBase | TeamTournamentBase")


class StandingsCalculator(Generic[T], ABC):
    @classmethod
    @abstractmethod
    def get_standings(cls, tournament: T) -> Standings:
        pass


class DefaultStandingsCalculator(StandingsCalculator[T], Generic[T]):
    @classmethod
    def get_standings(cls, tournament: T) -> Standings:
        scoring_system = tournament.parameters.scoring_system
        participant_dict = tournament.get_participant_dict()
        point_score_dict = {uuid: 0.0 for uuid in participant_dict.keys()}

        for round_result in tournament.states.results.rounds:
            for game in round_result.items:
                if game.uuid_1 is not None:
                    point_score_dict[game.uuid_1] += scoring_system.get_points(game.result_1)
                if game.uuid_2 is not None:
                    point_score_dict[game.uuid_2] += scoring_system.get_points(game.result_2)

        score_dicts = (point_score_dict,) + tuple(
            criterium.compute_tiebreak(tournament)  # type: ignore[arg-type]
            for criterium in tournament.parameters.tiebreaks.criteria
        )

        standings_items = [
            StandingsItem(
                participant=participant_dict[uuid],
                scores=tuple(score_dict[uuid] for score_dict in score_dicts)
            )
            for uuid in participant_dict.keys()
        ]
        return Standings(items=sorted(standings_items, key=lambda item: item.scores, reverse=True))
