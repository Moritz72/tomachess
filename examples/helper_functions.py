import random
from typing import TypeVar
from uuid import UUID

from tomachess.state.pairings import FinalizedPairings
from tomachess.participant import Participant
from tomachess.state.results import GameResult, FinalizedRoundResult, IndividualResult
from tomachess.state.team_pairings import FinalizedTeamPairing
from tomachess.state.team_results import FinalizedTeamGameResult
from tomachess.union_type import Tournament, TeamTournament

T = TypeVar("T", bound=Participant)


def get_name_from_uuid(uuid: UUID | None, uuid_dict: dict[UUID, T]) -> str:
    """Get the participant's name from its UUID."""
    if uuid is None:
        return "bye"
    participant = uuid_dict[uuid]
    return participant.name


def get_result_character(individual_result: IndividualResult) -> str:
    """Get an appropriate character (1, ½, 0, etc.) for the result"""
    match individual_result:
        case IndividualResult.WIN:
            return "1"
        case IndividualResult.DRAW:
            return "½"
        case IndividualResult.LOSS:
            return "0"
        case IndividualResult.FORFEIT_WIN:
            return "+"
        case IndividualResult.FORFEIT_LOSS:
            return "-"
        case IndividualResult.VOLUNTARY_BYE:
            return "+"
        case IndividualResult.PAIRING_ALLOCATED_BYE:
            return "+"
        case _:
            return "-"


def assign_random_game_result(game_result: GameResult) -> None:
    """Assign a random result (white wins, draw or black wins) to a game."""
    # Assign a pairing allocated bye if there is no opponent
    if game_result.uuid_1 is None:
        game_result.result_1 = IndividualResult.UNDEFINED
        game_result.result_2 = IndividualResult.PAIRING_ALLOCATED_BYE
        return
    if game_result.uuid_2 is None:
        game_result.result_1 = IndividualResult.PAIRING_ALLOCATED_BYE
        game_result.result_2 = IndividualResult.UNDEFINED
        return

    # Assign a uniformly drawn result
    random_outcome = random.randint(1, 3)
    match random_outcome:
        case 1:
            game_result.result_1 = IndividualResult.WIN
            game_result.result_2 = IndividualResult.LOSS
        case 2:
            game_result.result_1 = IndividualResult.DRAW
            game_result.result_2 = IndividualResult.DRAW
        case _:
            game_result.result_1 = IndividualResult.LOSS
            game_result.result_2 = IndividualResult.WIN


def print_pairings(pairings: FinalizedPairings, tournament: Tournament) -> None:
    """Helper function to visualize pairings."""
    uuid_dict = tournament.get_participant_dict()
    for pairing in pairings.items:
        name_1 = get_name_from_uuid(pairing.uuid_1.content, uuid_dict)
        name_2 = get_name_from_uuid(pairing.uuid_2.content, uuid_dict)
        print(f"{name_1}\t  -  \t{name_2}")


def print_round_result(round_result: FinalizedRoundResult, tournament: Tournament) -> None:
    """Helper function to visualize round results."""
    uuid_dict = tournament.get_participant_dict()
    for game_result in round_result.items:
        name_1 = get_name_from_uuid(game_result.uuid_1, uuid_dict)
        name_2 = get_name_from_uuid(game_result.uuid_2, uuid_dict)
        result = f"{get_result_character(game_result.result_1)} - {get_result_character(game_result.result_2)}"
        print(f"{name_1}\t{result}\t{name_2}")


def print_team_pairing(team_pairing: FinalizedTeamPairing, tournament: TeamTournament) -> None:
    """Helper function to visualize team pairings."""
    uuid_dict = tournament.get_participant_dict()
    assert team_pairing.team_1 is not None and team_pairing.team_2 is not None
    team_1 = uuid_dict[team_pairing.team_1]
    team_2 = uuid_dict[team_pairing.team_2]
    member_dict_1 = team_1.get_member_dict()
    member_dict_2 = team_2.get_member_dict()
    for pairing in team_pairing.items:
        name_1 = get_name_from_uuid(pairing.uuid_1.content, member_dict_1)
        name_2 = get_name_from_uuid(pairing.uuid_2.content, member_dict_2)
        print(f"\t{name_1}\t  -  \t{name_2}")


def print_team_game_result(team_game_result: FinalizedTeamGameResult, tournament: TeamTournament) -> None:
    """Helper function to visualize team game results."""
    uuid_dict = tournament.get_participant_dict()
    assert team_game_result.team_1 is not None and team_game_result.team_2 is not None
    team_1 = uuid_dict[team_game_result.team_1]
    team_2 = uuid_dict[team_game_result.team_2]
    member_dict_1 = team_1.get_member_dict()
    member_dict_2 = team_2.get_member_dict()
    for game_result in team_game_result.items:
        name_1 = get_name_from_uuid(game_result.uuid_1, member_dict_1)
        name_2 = get_name_from_uuid(game_result.uuid_2, member_dict_2)
        result = f"{get_result_character(game_result.result_1)} - {get_result_character(game_result.result_2)}"
        print(f"\t{name_1}\t{result}\t{name_2}")
