from uuid import UUID

from pydantic import Field

from tomachess.models import State
from tomachess.state.results.round_result import FinalizedRoundResult


class Results(State):
    rounds: list[FinalizedRoundResult] = Field(default_factory=list)

    def __len__(self) -> int:
        return len(self.rounds)

    def get_uuids(self) -> set[UUID | None]:
        return set().union(*(item.get_uuids() for item in self.rounds))
