from uuid import UUID

from tomachess.models import Entity
from tomachess.participant.player import Player


class Team(Entity):
    name: str
    members: list[Player]

    def get_member_dict(self) -> dict[UUID, Player]:
        return {member.uuid: member for member in self.members}
