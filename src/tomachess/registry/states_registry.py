from __future__ import annotations

from typing import TYPE_CHECKING, Type, TypeVar

if TYPE_CHECKING:
    from tomachess.base import AbstractStates

T = TypeVar("T", bound="AbstractStates")


class StatesRegistry:
    _REGISTRY: list[Type[AbstractStates]] = []

    @classmethod
    def register(cls, parameter_class: Type[T]) -> Type[T]:
        cls._REGISTRY.append(parameter_class)
        return parameter_class

    @classmethod
    def get_all(cls) -> list[Type[AbstractStates]]:
        return cls._REGISTRY
