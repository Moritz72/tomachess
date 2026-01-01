from typing import Generic, TypeVar

from tomachess.models import Parameter
from tomachess.parameter.tiebreaks.criteria import TeamTiebreakCriterium, TiebreakCriterium

T = TypeVar("T", bound=TiebreakCriterium)
U = TypeVar("U", bound=TeamTiebreakCriterium)


class Tiebreaks(Parameter, Generic[T]):
    criteria: list[T] = []


class TeamTiebreaks(Parameter, Generic[U]):
    criteria: list[U] = []
