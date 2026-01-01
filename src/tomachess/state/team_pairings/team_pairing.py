from __future__ import annotations

from typing import Self, TypeGuard
from uuid import UUID

from pydantic import BaseModel

from tomachess.exceptions import PairingError
from tomachess.state.pairings import FinalizedGamePairing, GamePairing, GamePairingItem


class TeamPairing(BaseModel):
    team_1: UUID | None
    team_2: UUID | None
    items: tuple[GamePairing, ...]

    @staticmethod
    def is_valid(team_pairing: TeamPairing) -> bool:
        return all(GamePairing.is_valid(item) for item in team_pairing.items)

    @staticmethod
    def is_playable(team_pairing: TeamPairing) -> bool:
        return team_pairing.team_1 is not None and team_pairing.team_2 is not None

    @staticmethod
    def is_finalized(team_pairing: TeamPairing) -> TypeGuard[FinalizedTeamPairing]:
        return all(GamePairing.is_finalized(item) for item in team_pairing.items)

    @classmethod
    def from_game_pairing(cls, game_pairing: FinalizedGamePairing, size: int) -> Self:
        if not GamePairing.is_valid(game_pairing):
            raise PairingError("The provided game pairing is invalid")

        match (game_pairing.uuid_1.content, game_pairing.uuid_2.content):
            case (None, _):
                item_template = GamePairing(
                    uuid_1=GamePairingItem.get_empty_instance(bye=game_pairing.uuid_1.bye),
                    uuid_2=GamePairingItem.get_free_instance()
                )
            case (_, None):
                item_template = GamePairing(
                    uuid_1=GamePairingItem.get_free_instance(),
                    uuid_2=GamePairingItem.get_empty_instance(bye=game_pairing.uuid_2.bye)
                )
            case _:
                item_template = GamePairing(
                    uuid_1=GamePairingItem.get_free_instance(),
                    uuid_2=GamePairingItem.get_free_instance()
                )

        items = tuple(item_template.model_copy(deep=True) for _ in range(size))
        return cls(team_1=game_pairing.uuid_1.content, team_2=game_pairing.uuid_2.content, items=items)

    def is_stricter_than(self, other: TeamPairing) -> bool:
        teams_equal = self.team_1 == other.team_1 and self.team_2 == other.team_2
        return teams_equal and all(s.is_stricter_than(o) for s, o in zip(self.items, other.items))


class FinalizedTeamPairing(TeamPairing):
    team_1: UUID | None
    team_2: UUID | None
    items: tuple[FinalizedGamePairing, ...]
