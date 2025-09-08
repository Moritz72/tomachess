from typing import Generic, TypeVar

from tomachess.models import Parameter
from tomachess.parameter.tiebreaks.criteria import AbstractTiebreakCriterium

T = TypeVar("T", bound=AbstractTiebreakCriterium)


class Tiebreaks(Parameter, Generic[T]):
    criteria: list[T] = []
