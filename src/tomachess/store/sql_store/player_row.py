from abc import ABC
from typing import Self
from uuid import UUID

from sqlmodel import Field, SQLModel

from tomachess.enum import Sex, Title
from tomachess.participant.player import Player


class AbstractPlayerRow(SQLModel, ABC):
    uuid: UUID = Field(primary_key=True)
    name: str
    sex: Sex
    birthday: int | None
    country: str | None
    title: Title
    rating: int | None

    @classmethod
    def _from_player(cls, player: Player) -> Self:
        return cls(
            uuid=player.uuid,
            name=player.name,
            sex=player.sex,
            birthday=player.birthday,
            country=player.country,
            title=player.title,
            rating=player.rating
        )

    def to_player(self) -> Player:
        return Player(
            uuid=self.uuid,
            name=self.name,
            sex=self.sex,
            birthday=self.birthday,
            country=self.country,
            title=self.title,
            rating=self.rating
        )


class PlayerRow(AbstractPlayerRow, table=True):
    collection: str

    @classmethod
    def from_player(cls, player: Player, collection: str) -> Self:
        player_row = cls._from_player(player)
        player_row.collection = collection
        return player_row


class TournamentPlayerRow(AbstractPlayerRow, table=True):
    tournament_uuid: UUID = Field(foreign_key="tournamentrow.uuid", primary_key=True)

    @classmethod
    def from_player(cls, player: Player, tournament_uuid: UUID) -> Self:
        player_row = cls._from_player(player)
        player_row.tournament_uuid = tournament_uuid
        return player_row
