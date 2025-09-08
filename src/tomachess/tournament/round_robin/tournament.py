from typing import Literal

from tomachess.base import ParametersBase, StatesBase, TournamentBase
from tomachess.parameter.tiebreaks import Tiebreaks
from tomachess.parameter.tiebreaks.criteria import SonnebornBerger, TiebreakCriterium
from tomachess.registry import ParametersRegistry, StatesRegistry, TournamentRegistry
from tomachess.tournament.round_robin.pairing_engine import RoundRobinPairingEngine


@ParametersRegistry.register
class RoundRobinParameters(ParametersBase):
    type: Literal["round_robin"] = "round_robin"
    tiebreaks: Tiebreaks[TiebreakCriterium] = Tiebreaks(criteria=[SonnebornBerger()])
    cycles: int = 1


@StatesRegistry.register
class RoundRobinStates(StatesBase):
    type: Literal["round_robin"] = "round_robin"


@TournamentRegistry.register("round_robin")
class RoundRobinTournament(TournamentBase):
    pairing_engine = RoundRobinPairingEngine()

    type: Literal["round_robin"] = "round_robin"
    parameters: RoundRobinParameters = RoundRobinParameters()
    states: RoundRobinStates = RoundRobinStates()

    def is_finished(self) -> bool:
        even = len(self.participants) % 2 == 0
        return len(self.states.results) >= (len(self.participants) - even) * self.parameters.cycles

    def is_drop_in_allowed(self) -> bool:
        return False
