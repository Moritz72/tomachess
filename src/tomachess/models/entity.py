from abc import ABC
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Entity(BaseModel, ABC):
    uuid: UUID = Field(default_factory=uuid4)
