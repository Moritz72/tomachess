from __future__ import annotations

from typing import TYPE_CHECKING, Type, TypeVar

if TYPE_CHECKING:
    from tomachess.base import AbstractParameters

T = TypeVar("T", bound="AbstractParameters")


class ParametersRegistry:
    _REGISTRY: list[Type[AbstractParameters]] = []

    @classmethod
    def register(cls, parameter_class: Type[T]) -> Type[T]:
        cls._REGISTRY.append(parameter_class)
        return parameter_class

    @classmethod
    def get_all(cls) -> list[Type[AbstractParameters]]:
        return cls._REGISTRY
