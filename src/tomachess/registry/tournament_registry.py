from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Type, TypeVar

if TYPE_CHECKING:
    from tomachess.base import TournamentBase, TeamTournamentBase

T = TypeVar("T", bound="TournamentBase")
U = TypeVar("U", bound="TeamTournamentBase")


class TournamentRegistry:
    _REGISTRY: dict[str, Type[TournamentBase]] = {}

    @classmethod
    def register(cls, name: str) -> Callable[[Type[T]], Type[T]]:
        def decorator(parameter_class: Type[T]) -> Type[T]:
            cls._REGISTRY[name] = parameter_class
            return parameter_class
        return decorator

    @classmethod
    def get(cls, name: str) -> Type[TournamentBase] | None:
        return cls._REGISTRY.get(name)

    @classmethod
    def get_all(cls) -> dict[str, Type[TournamentBase]]:
        return cls._REGISTRY


class TeamTournamentRegistry:
    _REGISTRY: dict[str, Type[TeamTournamentBase]] = {}

    @classmethod
    def register(cls, name: str) -> Callable[[Type[U]], Type[U]]:
        def decorator(parameter_class: Type[U]) -> Type[U]:
            cls._REGISTRY[name] = parameter_class
            return parameter_class
        return decorator

    @classmethod
    def get(cls, name: str) -> Type[TeamTournamentBase] | None:
        return cls._REGISTRY.get(name)

    @classmethod
    def get_all(cls) -> dict[str, Type[TeamTournamentBase]]:
        return cls._REGISTRY
