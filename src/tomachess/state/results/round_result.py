from __future__ import annotations

from typing import Self, TypeGuard
from uuid import UUID

from pydantic import BaseModel

from tomachess.state.pairings import FinalizedPairings
from tomachess.state.results.game_result import FinalizedGameResult, GameResult
from tomachess.type import RoundIndex


class RoundResult(BaseModel):
    index: RoundIndex
    items: tuple[GameResult, ...]

    @staticmethod
    def is_valid(round_result: RoundResult) -> bool:
        return all(GameResult.is_valid(item) for item in round_result.items)

    @staticmethod
    def is_finalized(round_result: RoundResult) -> TypeGuard[FinalizedRoundResult]:
        return all(GameResult.is_finalized(item) for item in round_result.items)

    @classmethod
    def from_pairings(cls, pairings: FinalizedPairings) -> Self:
        items = tuple(GameResult.from_game_pairing(item) for item in pairings.items)
        return cls(index=pairings.index, items=items)

    def get_uuids(self) -> set[UUID | None]:
        return set().union(*(item.get_uuids() for item in self.items))

    def get_pairings(self) -> FinalizedPairings:
        items = tuple(item.get_game_pairing() for item in self.items)
        return FinalizedPairings(index=self.index, items=items)


class FinalizedRoundResult(RoundResult):
    index: RoundIndex
    items: tuple[FinalizedGameResult, ...]
