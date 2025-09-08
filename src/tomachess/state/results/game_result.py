from __future__ import annotations

from typing import Self, TypeGuard
from uuid import UUID

from pydantic import BaseModel

from tomachess.exceptions import ResultError
from tomachess.state.pairings import GamePairing, FinalizedGamePairing, FinalizedGamePairingItem
from tomachess.state.results.individual_result import IndividualResult

_VALID_RESULT_PAIRS = {
    IndividualResult.WIN: IndividualResult.LOSS,
    IndividualResult.LOSS: IndividualResult.WIN,
    IndividualResult.DRAW: IndividualResult.DRAW,
    IndividualResult.FORFEIT_WIN: IndividualResult.FORFEIT_LOSS,
    IndividualResult.FORFEIT_LOSS: IndividualResult.FORFEIT_WIN
}


class GameResult(BaseModel):
    uuid_1: UUID | None
    uuid_2: UUID | None
    result_1: IndividualResult | None = None
    result_2: IndividualResult | None = None

    @staticmethod
    def _determine_opponent_result(item: FinalizedGamePairingItem) -> IndividualResult | None:
        if item.bye:
            return IndividualResult.PAIRING_ALLOCATED_BYE
        elif item.content is None:
            return IndividualResult.VOLUNTARY_BYE
        else:
            return None

    @staticmethod
    def _determine_result(
            item_1: FinalizedGamePairingItem, item_2: FinalizedGamePairingItem
    ) -> tuple[IndividualResult | None, IndividualResult | None]:
        result_white = GameResult._determine_opponent_result(item_1)
        result_black = GameResult._determine_opponent_result(item_2)
        if item_1.content is None:
            result_white = IndividualResult.UNDEFINED
        if item_2.content is None:
            result_black = IndividualResult.UNDEFINED
        return result_white, result_black

    @staticmethod
    def is_valid(game_result: GameResult) -> bool:
        if not GamePairing.is_valid(game_result.get_game_pairing()):
            return False

        pairing = (game_result.uuid_1, game_result.uuid_2)
        result = (game_result.result_1, game_result.result_2)
        valids = (IndividualResult.VOLUNTARY_BYE, IndividualResult.PAIRING_ALLOCATED_BYE, IndividualResult.UNDEFINED)

        if pairing[0] is None:
            return result[1] in valids
        if pairing[1] is None:
            return result[0] in valids
        if not GameResult.is_finalized(game_result):
            return True
        if result == (IndividualResult.FORFEIT_LOSS, IndividualResult.FORFEIT_LOSS):
            return True
        return _VALID_RESULT_PAIRS.get(game_result.result_1) == game_result.result_2

    @staticmethod
    def is_finalized(game_result: GameResult) -> TypeGuard[FinalizedGameResult]:
        return game_result.result_1 is not None and game_result.result_2 is not None

    @classmethod
    def from_game_pairing(cls, game_pairing: FinalizedGamePairing) -> Self:
        if not GamePairing.is_valid(game_pairing):
            raise ResultError("The provided game pairing is invalid")

        item_1 = game_pairing.uuid_1
        item_2 = game_pairing.uuid_2
        result_1, result_2 = GameResult._determine_result(item_1, item_2)

        return cls(
            uuid_1=item_1.content,
            uuid_2=item_2.content,
            result_1=result_1,
            result_2=result_2
        )

    def get_uuids(self) -> set[UUID | None]:
        return {self.uuid_1, self.uuid_2}

    def get_game_pairing(self) -> FinalizedGamePairing:
        return FinalizedGamePairing.from_uuids(
            uuid_1=self.uuid_1,
            uuid_2=self.uuid_2,
            bye_1=self.result_1 == IndividualResult.VOLUNTARY_BYE,
            bye_2=self.result_1 == IndividualResult.VOLUNTARY_BYE,
        )


class FinalizedGameResult(GameResult):
    uuid_1: UUID | None
    uuid_2: UUID | None
    result_1: IndividualResult
    result_2: IndividualResult
