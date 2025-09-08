from __future__ import annotations

from typing import TypeGuard

from tomachess.models import State
from tomachess.state.pairings.game_pairing import FinalizedGamePairing, GamePairing
from tomachess.type import RoundIndex


class Pairings(State):
    index: RoundIndex
    items: tuple[GamePairing, ...] = ()

    @staticmethod
    def is_valid(pairings: Pairings) -> bool:
        return all(GamePairing.is_valid(item) for item in pairings.items)

    @staticmethod
    def is_finalized(pairings: Pairings) -> TypeGuard[FinalizedPairings]:
        return all(GamePairing.is_finalized(item) for item in pairings.items)

    def is_stricter_than(self, other: Pairings) -> bool:
        return self.index == other.index and all(s.is_stricter_than(o) for s, o in zip(self.items, other.items))


class FinalizedPairings(Pairings):
    index: RoundIndex
    items: tuple[FinalizedGamePairing, ...] = ()
