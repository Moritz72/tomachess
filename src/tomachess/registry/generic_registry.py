from typing import ClassVar, Generic, Protocol, Type, TypeVar


class HasType(Protocol):
    type: ClassVar[str]


T = TypeVar("T", bound=HasType)


class GenericRegistry(Generic[T]):
    _REGISTRY: dict[str, Type[T]]

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls._REGISTRY = {}

    @classmethod
    def register(cls, object_class: Type[T]) -> Type[T]:
        cls._REGISTRY[object_class.type] = object_class
        return object_class

    @classmethod
    def get(cls, key: str) -> Type[T] | None:
        return cls._REGISTRY.get(key)

    @classmethod
    def require(cls, key: str) -> Type[T]:
        return cls._REGISTRY[key]

    @classmethod
    def get_all(cls) -> dict[str, Type[T]]:
        return cls._REGISTRY