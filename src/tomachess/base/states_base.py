from abc import ABC
from uuid import UUID

from pydantic import BaseModel

from tomachess.state import Pairings, Results, TeamParings, TeamResults


class AbstractStates(BaseModel, ABC):
    type: str
    drop_outs: set[UUID] = set()
    byes: set[UUID] = set()
    pairings: Pairings | None = None
    results: Results = Results()


class StatesBase(AbstractStates, ABC):
    type: str


class TeamStatesBase(AbstractStates, ABC):
    type: str
    team_pairings: TeamParings | None = None
    team_results: TeamResults = TeamResults()
