from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, ClassVar, Generic, Sequence, TypeVar
from uuid import UUID

from tomachess.base.parameters_base import ParametersBase, TeamParametersBase
from tomachess.base.states_base import StatesBase, TeamStatesBase
from tomachess.classes import DefaultStandingsCalculator, PairingEngine, StandingsCalculator
from tomachess.exceptions import NotFoundError, PairingError, ResultError, TournamentPermissionError
from tomachess.models import Entity, Standings
from tomachess.participant import Participant, Player, Team
from tomachess.state import Pairings, TeamParings
from tomachess.state.results.round_result import RoundResult
from tomachess.state.team_pairings import TeamPairing
from tomachess.state.team_results import TeamGameResult, TeamRoundResult

if TYPE_CHECKING:
    from tomachess.union_type import Parameters, States

T = TypeVar("T", bound=Participant)


class AbstractTournamentBase(Entity, Generic[T], ABC):
    pairing_engine: ClassVar[PairingEngine[Any]]
    standings_calculator: ClassVar[StandingsCalculator[Any]] = DefaultStandingsCalculator()

    type: str
    participants: list[T] = []
    parameters: Parameters
    states: States

    def get_participant_uuids(self) -> set[UUID]:
        return {participant.uuid for participant in self.participants}

    def get_participant_dict(self) -> dict[UUID, T]:
        return {participant.uuid: participant for participant in self.participants}

    def get_pairings(self) -> Pairings | None:
        if self.states.pairings is None:
            return None
        return self.states.pairings.model_copy(deep=True)

    def get_standings(self) -> Standings:
        return self.standings_calculator.get_standings(self)

    def generate_pairings(self) -> None:
        if self.states.pairings is not None:
            raise PairingError("Pairings were already generated")
        if self.is_finished():
            raise PairingError("The tournament is already finished")
        self.states.pairings = self.pairing_engine.get_pairings(self)

    def clarify_pairings(self, pairings: Pairings) -> None:
        if self.states.pairings is None:
            raise PairingError("No pairings were generated")
        if not Pairings.is_valid(pairings):
            raise PairingError("The provided pairings are invalid")
        if not pairings.is_stricter_than(self.states.pairings):
            raise PairingError("The provided pairings are looser than the current ones")
        self.states.pairings = pairings

    def finalize_pairings(self, pairings: Pairings) -> None:
        if not Pairings.is_finalized(pairings):
            raise PairingError("The provided pairings are not final")
        self.clarify_pairings(pairings)

    @abstractmethod
    def is_finished(self) -> bool:
        pass

    def is_drop_out_allowed(self) -> bool:
        return True

    def is_drop_in_allowed(self) -> bool:
        return True

    def is_taking_byes_allowed(self) -> bool:
        return False

    def drop_out(self, participants: Sequence[T]) -> None:
        if not self.is_drop_out_allowed():
            raise TournamentPermissionError("Dropping out is not allowed")
        uuids = set(participant.uuid for participant in participants)
        if not uuids.issubset(self.get_participant_uuids()):
            raise NotFoundError("Some participants are not present")
        result_uuids = self.states.results.get_uuids()
        remove_uuids = uuids - result_uuids
        self.participants = [participant for participant in self.participants if participant.uuid not in remove_uuids]
        self.states.drop_outs |= (uuids - remove_uuids)

    def drop_in(self, participants: Sequence[T]) -> None:
        if not self.is_drop_in_allowed():
            raise TournamentPermissionError("Dropping in is not allowed")
        uuids = self.get_participant_uuids()
        for participant in participants:
            self.states.drop_outs.discard(participant.uuid)
            if participant.uuid not in uuids:
                self.participants.append(participant)
                uuids.add(participant.uuid)

    def take_byes(self, participants: Sequence[T]) -> None:
        if not self.is_taking_byes_allowed():
            raise TournamentPermissionError("Taking byes is not allowed")
        uuids = set(participant.uuid for participant in participants)
        if not uuids.issubset(self.get_participant_uuids()):
            raise NotFoundError("Some participants are not present")
        self.states.byes |= set(uuids)


class TournamentBase(AbstractTournamentBase[Player], ABC):
    parameters: ParametersBase
    states: StatesBase

    def add_round_result(self, round_result: RoundResult) -> None:
        pairings = round_result.get_pairings()
        if self.states.pairings is None:
            raise PairingError("No pairings were generated")
        if not pairings.is_stricter_than(self.states.pairings):
            raise PairingError("The provided round result does not match the pairings")
        if not RoundResult.is_valid(round_result):
            raise ResultError("Some game results are invalid")
        if not RoundResult.is_finalized(round_result):
            raise ResultError("Some game results are missing")
        self.states.results.rounds.append(round_result)
        self.states.pairings = None
        self.states.byes = set()


class TeamTournamentBase(AbstractTournamentBase[Team], ABC):
    parameters: TeamParametersBase
    states: TeamStatesBase

    def _initialize_team_pairings_and_results(self) -> None:
        assert self.states.pairings is not None
        if Pairings.is_finalized(self.states.pairings):
            self.states.team_pairings = TeamParings.from_pairings(self.states.pairings, self.parameters.boards)
            self.states.team_results.rounds.append(TeamRoundResult.get_empty_instance(self.states.team_pairings))

    def get_team_pairings(self) -> TeamParings | None:
        if self.states.team_pairings is None:
            return None
        return self.states.team_pairings.model_copy(deep=True)

    def generate_pairings(self) -> None:
        super().generate_pairings()
        self._initialize_team_pairings_and_results()

    def clarify_pairings(self, pairings: Pairings) -> None:
        super().clarify_pairings(pairings)
        self._initialize_team_pairings_and_results()

    def finalize_pairings(self, pairings: Pairings) -> None:
        super().finalize_pairings(pairings)
        self._initialize_team_pairings_and_results()

    def clarify_team_pairing(self, index: int, team_pairing: TeamPairing) -> None:
        if self.states.team_pairings is None:
            raise PairingError("No team pairings were generated")
        if not TeamPairing.is_valid(team_pairing):
            raise PairingError("The provided team pairing is invalid")
        if not team_pairing.is_stricter_than(self.states.team_pairings.items[index]):
            raise PairingError("The provided pairing is looser than the current one")
        self.states.team_pairings.items[index] = team_pairing

    def finalize_team_pairing(self, index: int, team_pairing: TeamPairing) -> None:
        if not TeamPairing.is_finalized(team_pairing):
            raise PairingError("The provided pairings are not final")
        self.clarify_team_pairing(index, team_pairing)

    def add_team_game_result(self, index: int, team_game_result: TeamGameResult) -> None:
        team_pairing = team_game_result.get_team_pairing()
        if self.states.team_pairings is None:
            raise PairingError("No team pairings were generated")
        if not team_pairing.is_stricter_than(self.states.team_pairings.items[index]):
            raise PairingError("The provided team game result does not match the team pairing")
        if not TeamGameResult.is_valid(team_game_result):
            raise ResultError("Some game results are invalid")
        if not TeamGameResult.is_finalized(team_game_result):
            raise ResultError("Some game results are missing")
        current_team_round_result = self.states.team_results.rounds[-1]
        current_team_round_result.items[index] = team_game_result
        if not TeamRoundResult.has_empty(current_team_round_result):
            round_result = current_team_round_result.get_round_result(self.parameters.board_scoring_system)
            self.states.results.rounds.append(round_result)
            self.states.pairings = None
            self.states.team_pairings = None
            self.states.byes = set()
