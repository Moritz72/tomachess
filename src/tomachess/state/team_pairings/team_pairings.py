from typing import Self

from pydantic import Field

from tomachess.models import State
from tomachess.state.pairings import FinalizedPairings
from tomachess.state.team_pairings.team_pairing import TeamPairing
from tomachess.type import RoundIndex


class TeamParings(State):
    index: RoundIndex
    items: list[TeamPairing] = Field(default_factory=list)

    @classmethod
    def from_pairings(cls, pairings: FinalizedPairings, size: int) -> Self:
        items = [TeamPairing.from_game_pairing(game_pairing, size) for game_pairing in pairings.items]
        return cls(index=pairings.index, items=items)
