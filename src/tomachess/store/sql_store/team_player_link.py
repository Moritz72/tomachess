from uuid import UUID

from sqlmodel import Field, ForeignKeyConstraint, SQLModel


class TeamPlayerLink(SQLModel, table=True):
    team_uuid: UUID = Field(foreign_key="teamrow.uuid", primary_key=True)
    player_uuid: UUID = Field(foreign_key="playerrow.uuid", primary_key=True)


class TournamentTeamPlayerLink(SQLModel, table=True):
    team_uuid: UUID = Field(primary_key=True)
    team_tournament_uuid: UUID = Field(primary_key=True)

    player_uuid: UUID = Field(primary_key=True)
    player_tournament_uuid: UUID = Field(primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["team_uuid", "team_tournament_uuid"],
            ["tournamentteamrow.uuid", "tournamentteamrow.tournament_uuid"],
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["player_uuid", "player_tournament_uuid"],
            ["tournamentplayerrow.uuid", "tournamentplayerrow.tournament_uuid"],
            ondelete="CASCADE",
        ),
    )
