from tomachess.base import ParametersBase, StatesBase, TournamentBase
from tomachess.parameter.tiebreaks import Tiebreaks
from tomachess.parameter.tiebreaks.criteria import SonnebornBerger, TiebreakCriterium
from tomachess.registry import TournamentRegistry
from tomachess.tournament.round_robin.pairing_engine import RoundRobinPairingEngine


class RoundRobinParameters(ParametersBase):
    tiebreaks: Tiebreaks[TiebreakCriterium] = Tiebreaks(criteria=[SonnebornBerger()])
    cycles: int = 1


class RoundRobinStates(StatesBase):
    pass


@TournamentRegistry.register
class RoundRobinTournament(TournamentBase):
    type = "round_robin"
    pairing_engine = RoundRobinPairingEngine()

    parameters: RoundRobinParameters = RoundRobinParameters()
    states: RoundRobinStates = RoundRobinStates()

    def is_finished(self) -> bool:
        even = len(self.participants) % 2 == 0
        return len(self.states.results) >= (len(self.participants) - even) * self.parameters.cycles

    def is_drop_in_allowed(self) -> bool:
        return False
