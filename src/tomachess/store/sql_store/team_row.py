from abc import ABC
from typing import TYPE_CHECKING, Self, Sequence
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from tomachess.participant import Team
from tomachess.store.sql_store.player_row import AbstractPlayerRow, PlayerRow, TournamentPlayerRow
from tomachess.store.sql_store.team_player_link import TeamPlayerLink, TournamentTeamPlayerLink


class AbstractTeamRow(SQLModel, ABC):
    uuid: UUID = Field(primary_key=True)
    name: str

    if TYPE_CHECKING:
        members: Sequence[AbstractPlayerRow]

    @classmethod
    def _from_team(cls, team: Team) -> Self:
        return cls(uuid=team.uuid, name=team.name, members=[])

    def to_team(self) -> Team:
        members = [member.to_player() for member in self.members]
        return Team(uuid=self.uuid, name=self.name, members=members)


class TeamRow(AbstractTeamRow, table=True):
    collection: str
    members: list[PlayerRow] = Relationship(
        back_populates=None, link_model=TeamPlayerLink,
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    @classmethod
    def from_team(cls, team: Team, collection: str) -> Self:
        team_row = cls._from_team(team)
        team_row.collection = collection
        team_row.members = [PlayerRow.from_player(member, collection) for member in team.members]
        return team_row


class TournamentTeamRow(AbstractTeamRow, table=True):
    tournament_uuid: UUID = Field(foreign_key="teamtournamentrow.uuid", primary_key=True)
    members: list[TournamentPlayerRow] = Relationship(
        back_populates=None,
        link_model=TournamentTeamPlayerLink,
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    @classmethod
    def from_team(cls, team: Team, tournament_uuid: UUID) -> Self:
        team_row = cls._from_team(team)
        team_row.tournament_uuid = tournament_uuid
        team_row.members = [TournamentPlayerRow.from_player(member, tournament_uuid) for member in team.members]
        return team_row
