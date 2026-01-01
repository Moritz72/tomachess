from abc import ABC
from uuid import UUID

from pydantic import BaseModel

from tomachess.state import Pairings, Results, TeamParings, TeamResults


class AbstractStates(BaseModel, ABC):
    drop_outs: set[UUID] = set()
    byes: set[UUID] = set()
    pairings: Pairings | None = None
    results: Results = Results()


class StatesBase(AbstractStates, ABC):
    pass


class TeamStatesBase(AbstractStates, ABC):
    team_pairings: TeamParings | None = None
    team_results: TeamResults = TeamResults()
