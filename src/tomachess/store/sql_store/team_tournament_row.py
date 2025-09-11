import json
from typing import Self
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from tomachess.store.sql_store.team_row import TournamentTeamRow
from tomachess.union_type import TeamTournament


class TeamTournamentRow(SQLModel, table=True):
    collection: str
    uuid: UUID = Field(primary_key=True)
    type: str
    participants: list[TournamentTeamRow] = Relationship(
        back_populates=None,
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    parameters: str
    states: str

    @classmethod
    def from_team_tournament(cls, tournament: TeamTournament, collection: str) -> Self:
        teams = [TournamentTeamRow.from_team(team, tournament.uuid) for team in tournament.participants]
        return cls(
            collection=collection,
            uuid=tournament.uuid,
            type=tournament.type,
            participants=teams,
            parameters=tournament.parameters.model_dump_json(),
            states=tournament.states.model_dump_json()
        )

    def to_team_tournament(self) -> TeamTournament:
        values = {
            "uuid": self.uuid,
            "type": self.type,
            "participants": [team.to_team() for team in self.participants],
            "parameters": json.loads(self.parameters),
            "states": json.loads(self.states)
        }
        return TeamTournament.model_validate(values)
