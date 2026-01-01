from tomachess.base import TeamParametersBase, TeamStatesBase,TeamTournamentBase
from tomachess.parameter import TeamTiebreaks
from tomachess.parameter.tiebreaks.criteria import BoardPoints, TeamTiebreakCriterium
from tomachess.registry import TeamTournamentRegistry
from tomachess.tournament.round_robin.pairing_engine import RoundRobinPairingEngine


class RoundRobinTeamParameters(TeamParametersBase):
    tiebreaks: TeamTiebreaks[TeamTiebreakCriterium] = TeamTiebreaks(criteria=[BoardPoints()])
    cycles: int = 1


class RoundRobinTeamStates(TeamStatesBase):
    pass


@TeamTournamentRegistry.register
class RoundRobinTeamTournament(TeamTournamentBase):
    type = "round_robin"
    pairing_engine = RoundRobinPairingEngine()

    parameters: RoundRobinTeamParameters = RoundRobinTeamParameters()
    states: RoundRobinTeamStates = RoundRobinTeamStates()

    def is_finished(self) -> bool:
        even = len(self.participants) % 2 == 0
        return len(self.states.results) >= (len(self.participants) - even) * self.parameters.cycles

    def is_drop_in_allowed(self) -> bool:
        return not bool(self.states.results)
