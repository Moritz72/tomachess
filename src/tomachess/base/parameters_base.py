from abc import ABC

from pydantic import BaseModel

from tomachess.parameter import TeamTiebreaks, Tiebreaks, ScoringSystem
from tomachess.parameter.tiebreaks.criteria import TiebreakCriterium, TeamTiebreakCriterium


class AbstractParameters(BaseModel, ABC):
    type: str
    scoring_system: ScoringSystem = ScoringSystem()


class ParametersBase(AbstractParameters, ABC):
    type: str
    tiebreaks: Tiebreaks[TiebreakCriterium] = Tiebreaks()


class TeamParametersBase(AbstractParameters, ABC):
    type: str
    scoring_system: ScoringSystem = ScoringSystem(win=2.0, draw=1.0, loss=0.0)
    tiebreaks: TeamTiebreaks[TeamTiebreakCriterium] = TeamTiebreaks()
    boards: int = 8
    board_scoring_system: ScoringSystem = ScoringSystem()
