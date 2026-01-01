from typing import TYPE_CHECKING, Any, Annotated, Union

from pydantic import Field

from tomachess.parameter.tiebreaks.criteria.abstract_criterium import AbstractCriterium
from tomachess.parameter.tiebreaks.criteria.board_points import BoardPoints
from tomachess.parameter.tiebreaks.criteria.buchholz import Buchholz
from tomachess.parameter.tiebreaks.criteria.sonneborn_berger import SonnebornBerger

if TYPE_CHECKING:
    from tomachess.base.tournament_base import TournamentBase, TeamTournamentBase

TiebreakCriterium = Annotated[Union[
    Buchholz["TournamentBase"],
    SonnebornBerger["TournamentBase"]
], Field(discriminator="type")]
TeamTiebreakCriterium = Annotated[Union[
    Buchholz["TeamTournamentBase"],
    SonnebornBerger["TeamTournamentBase"],
    BoardPoints
], Field(discriminator="type")]

__all__ = [
    "BoardPoints",
    "Buchholz",
    "SonnebornBerger",
    "TeamTiebreakCriterium",
    "TiebreakCriterium"
]
