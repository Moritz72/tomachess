import json
from typing import Self
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from tomachess.base import TournamentBase
from tomachess.registry import TournamentRegistry
from tomachess.store.sql_store.player_row import TournamentPlayerRow


class TournamentRow(SQLModel, table=True):
    collection: str
    uuid: UUID = Field(primary_key=True)
    type: str
    participants: list[TournamentPlayerRow] = Relationship(
        back_populates=None,
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    parameters: str
    states: str

    @classmethod
    def from_tournament(cls, tournament: TournamentBase, collection: str) -> Self:
        players = [TournamentPlayerRow.from_player(player, tournament.uuid) for player in tournament.participants]
        return cls(
            collection=collection,
            uuid=tournament.uuid,
            type=tournament.type,
            participants=players,
            parameters=tournament.parameters.model_dump_json(),
            states=tournament.states.model_dump_json()
        )

    def to_tournament(self) -> TournamentBase:
        values = {
            "uuid": self.uuid,
            "participants": [player.to_player() for player in self.participants],
            "parameters": json.loads(self.parameters),
            "states": json.loads(self.states)
        }
        return TournamentRegistry.require(self.type).model_validate(values)
