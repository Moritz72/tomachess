from pydantic import BaseModel

from tomachess.participant import Participant


class StandingsItem(BaseModel):
    participant: Participant
    scores: tuple[float, ...]


class Standings(BaseModel):
    items: list[StandingsItem]
