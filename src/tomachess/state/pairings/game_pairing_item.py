from __future__ import annotations

from uuid import UUID
from types import EllipsisType
from typing import Any, Self, TypeGuard

from pydantic import BaseModel, field_serializer, field_validator, model_validator

from tomachess.exceptions import PairingError

GamePairingItemContent = EllipsisType | list[UUID] | UUID | None
FinalizedGamePairingItemContent = UUID | None


class GamePairingItem(BaseModel):
    content: GamePairingItemContent = None
    bye: bool = False
    nullable: bool = False

    model_config = {"arbitrary_types_allowed": True}

    @model_validator(mode="after")
    @staticmethod
    def check_validity(model: GamePairingItem) -> GamePairingItem:
        if model.content == []:
            raise PairingError("Content can not be an empty list")
        if model.content is None and model.nullable is False:
            raise PairingError("Nullable must be 'True' if content is 'None'")
        if model.bye and model.content is not None:
            raise PairingError("Content must be 'None' if bye is set to 'True'")
        if model.bye and model.nullable is not None:
            raise PairingError("Nullable must be 'False' if bye is set to 'True'")
        return model

    @model_validator(mode="after")
    @staticmethod
    def unwrap_singleton_list(model: GamePairingItem) -> GamePairingItem:
        if isinstance(model.content, list) and len(model.content) == 1:
            model.content = model.content[0]
        return model

    @field_validator("content", mode="before")
    @staticmethod
    def deserialize_ellipsis(v: object) -> object:
        if v == "...":
            return ...
        return v

    @field_serializer("content")
    def serialize_ellipsis(self, info: Any) -> dict[str, object]:
        return {"content": ... if self.content == "..." else self.content}

    @staticmethod
    def is_valid(game_pairing_item: GamePairingItem) -> bool:
        if game_pairing_item.content == []:
            return False
        if game_pairing_item.content is None and game_pairing_item.nullable is False:
            return False
        if game_pairing_item.bye and game_pairing_item.content is not None:
            return False
        if game_pairing_item.bye and game_pairing_item.nullable is not None:
            return False
        return True

    @staticmethod
    def is_finalized(game_pairing_item: GamePairingItem) -> TypeGuard[FinalizedGamePairingItem]:
        return isinstance(game_pairing_item.content, FinalizedGamePairingItemContent)

    @classmethod
    def get_free_instance(cls) -> Self:
        return cls(content=..., bye=False, nullable=True)

    @classmethod
    def get_empty_instance(cls, bye: bool = False) -> Self:
        return cls(content=None, bye=bye, nullable=not bye)

    def is_stricter_than(self, other: GamePairingItem) -> bool:
        if not GamePairingItem.is_valid(self):
            return False
        if self.bye != other.bye:
            return False
        if self.bye:
            return True
        if self.nullable and not other.nullable:
            return False
        if other.content == ...:
            return True
        if self.content == ...:
            return other.content == ...

        match (self.content, other.content):
            case (None, None):
                return True
            case (_, None):
                return False
            case (None, _):
                return True
            case (UUID() as i_1, UUID() as i_2):
                return i_1 == i_2
            case (UUID() as i_1, list() as i_2):
                return i_1 in i_2
            case (list(), UUID()):
                return False
            case (list() as i_1, list() as i_2):
                return set(i_1).issubset(i_2)
            case _:
                return False


class FinalizedGamePairingItem(GamePairingItem):
    content: FinalizedGamePairingItemContent
    bye: bool
    nullable: bool

    @classmethod
    def from_uuid(cls, uuid: UUID | None, bye: bool = False) -> Self:
        if uuid is None:
            return cls.get_empty_instance(bye=bye)
        return cls(content=uuid, bye=False, nullable=False)
