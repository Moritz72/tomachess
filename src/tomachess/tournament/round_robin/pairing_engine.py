from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar
from uuid import UUID

from tomachess.classes import PairingEngine
from tomachess.state import Pairings
from tomachess.state.pairings import FinalizedGamePairing

if TYPE_CHECKING:
    from tomachess.tournament.round_robin.tournament import RoundRobinTournament
    from tomachess.tournament.round_robin.team_tournament import RoundRobinTeamTournament

T = TypeVar("T", bound="RoundRobinTournament | RoundRobinTeamTournament")


class RoundRobinPairingEngine(PairingEngine[T], Generic[T]):
    @staticmethod
    def _get_cycle(tournament: T) -> int:
        even = len(tournament.participants) % 2 == 0
        return len(tournament.states.results) // (len(tournament.participants) - even) + 1

    @staticmethod
    def _get_modulo_round(tournament: T) -> int:
        even = len(tournament.participants) % 2 == 0
        return len(tournament.states.results) % (len(tournament.participants) - even) + 1

    @staticmethod
    def _get_berger_indices(participant_number: int, round_number: int) -> list[tuple[int, int]]:
        assert participant_number % 2 == 0
        assert round_number < participant_number

        m = participant_number - 1
        half = participant_number // 2
        i = ((round_number - 1) * half) % m + 1
        pairs = []

        if i <= half:
            pairs.append((i, participant_number))
        else:
            pairs.append((participant_number, i))

        for k in range(1, half):
            a = ((i + k - 1) % m) + 1
            b = ((i - k - 1) % m) + 1
            pairs.append((a, b))

        return pairs

    @staticmethod
    def _get_pairing(indices: tuple[int, int], uuids: list[UUID]) -> tuple[UUID | None, UUID | None]:
        match (indices[0] > len(uuids), indices[1] > len(uuids)):
            case (False, False):
                return uuids[indices[0] - 1], uuids[indices[1] - 1]
            case (True, False):
                return None, uuids[indices[1] - 1]
            case(False, True):
                return uuids[indices[0] - 1], None
            case _:
                assert False

    @classmethod
    def get_pairings(cls, tournament: T) -> Pairings:
        uuids = list(tournament.get_participant_uuids())
        participant_number = len(uuids)
        odd = participant_number % 2
        cycle = cls._get_cycle(tournament)
        round_number = cls._get_modulo_round(tournament)
        pairing_indices = cls._get_berger_indices(participant_number + odd, round_number)

        if cycle % 2 == 0:
            pairing_indices = [indices[::-1] for indices in pairing_indices]

        if tournament.parameters.cycles == 1:
            round_index = [round_number]
        else:
            round_index = [cycle, round_number]

        pairing_indices = [(a, b) for a, b in pairing_indices if a <= participant_number and b <= participant_number]
        pairing_uuids = tuple(cls._get_pairing(indices, uuids) for indices in pairing_indices)
        items = tuple(FinalizedGamePairing.from_uuids(uuid_1=uuid_1, uuid_2=uuid_2) for uuid_1, uuid_2 in pairing_uuids)

        return Pairings(index=round_index, items=items)
