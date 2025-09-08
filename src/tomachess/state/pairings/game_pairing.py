from __future__ import annotations
from typing import Self, TypeGuard
from uuid import UUID

from pydantic import BaseModel

from tomachess.state.pairings.game_pairing_item import FinalizedGamePairingItem, GamePairingItem


class GamePairing(BaseModel):
    uuid_1: GamePairingItem
    uuid_2: GamePairingItem

    @staticmethod
    def is_valid(game_pairing: GamePairing) -> bool:
        return all(GamePairingItem.is_valid(item) for item in (game_pairing.uuid_1, game_pairing.uuid_2))

    @staticmethod
    def is_playable(game_pairing: GamePairing) -> bool:
        present = game_pairing.uuid_1.content is not None and game_pairing.uuid_2.content is not None
        return GamePairing.is_valid(game_pairing) and present

    @staticmethod
    def is_finalized(game_pairing: GamePairing) -> TypeGuard[FinalizedGamePairing]:
        return all(GamePairingItem.is_finalized(item) for item in (game_pairing.uuid_1, game_pairing.uuid_2))

    def is_stricter_than(self, other: GamePairing) -> bool:
        return self.uuid_1.is_stricter_than(other.uuid_1) and self.uuid_2.is_stricter_than(self.uuid_2)


class FinalizedGamePairing(GamePairing):
    uuid_1: FinalizedGamePairingItem
    uuid_2: FinalizedGamePairingItem

    @classmethod
    def from_uuids(
            cls,
            uuid_1: UUID | None,
            uuid_2: UUID | None,
            bye_1: bool = False,
            bye_2: bool = False
    ) -> Self:
        return cls(
            uuid_1=FinalizedGamePairingItem.from_uuid(uuid_1, bye_1),
            uuid_2=FinalizedGamePairingItem.from_uuid(uuid_2, bye_2)
        )
