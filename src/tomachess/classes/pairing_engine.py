from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from tomachess.state import Pairings

if TYPE_CHECKING:
    from tomachess.base.tournament_base import AbstractTournamentBase

T = TypeVar("T", bound="AbstractTournamentBase[Any]")


class PairingEngine(Generic[T], ABC):
    @classmethod
    @abstractmethod
    def get_pairings(cls, tournament: T) -> Pairings:
        pass
