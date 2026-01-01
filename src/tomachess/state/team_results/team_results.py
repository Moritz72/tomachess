from pydantic import Field

from tomachess.models import State
from tomachess.state.team_results.team_round_result import TeamRoundResult


class TeamResults(State):
    rounds: list[TeamRoundResult] = Field(default_factory=list)

    def __len__(self) -> int:
        return len(self.rounds)
