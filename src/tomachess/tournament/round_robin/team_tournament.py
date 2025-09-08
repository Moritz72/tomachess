from typing import Literal

from tomachess.base import TeamParametersBase, TeamStatesBase,TeamTournamentBase
from tomachess.parameter import Tiebreaks
from tomachess.parameter.tiebreaks.criteria import BoardPoints, TeamTiebreakCriterium
from tomachess.registry import ParametersRegistry, StatesRegistry, TeamTournamentRegistry
from tomachess.tournament.round_robin.pairing_engine import RoundRobinPairingEngine


@ParametersRegistry.register
class RoundRobinTeamParameters(TeamParametersBase):
    type: Literal["round_robin"] = "round_robin"
    tiebreaks: Tiebreaks[TeamTiebreakCriterium] = Tiebreaks(criteria=[BoardPoints()])
    cycles: int = 1

@StatesRegistry.register
class RoundRobinTeamStates(TeamStatesBase):
    type: Literal["round_robin_team"] = "round_robin_team"


@TeamTournamentRegistry.register("round_robin")
class RoundRobinTeamTournament(TeamTournamentBase):
    pairing_engine = RoundRobinPairingEngine()

    type: Literal["round_robin"] = "round_robin"
    parameters: RoundRobinTeamParameters = RoundRobinTeamParameters()
    states: RoundRobinTeamStates = RoundRobinTeamStates()

    def is_finished(self) -> bool:
        even = len(self.participants) % 2 == 0
        return len(self.states.results) >= (len(self.participants) - even) * self.parameters.cycles

    def is_drop_in_allowed(self) -> bool:
        return not bool(self.states.results)
