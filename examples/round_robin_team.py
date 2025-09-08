from tomachess.participant import Player, Team
from tomachess.state import Pairings
from tomachess.state.team_pairings import TeamPairing
from tomachess.state.team_results import TeamGameResult
from tomachess.tournament.round_robin import RoundRobinTeamTournament

from helper_functions import assign_random_game_result, print_team_pairing, print_team_game_result


# Create some dummy players to put into teams
players = [
    Player(name="Alice"),
    Player(name="Bob"),
    Player(name="Charlie"),
    Player(name="Diana"),
    Player(name="Ethan"),
    Player(name="Fiona"),
    Player(name="George"),
    Player(name="Hannah"),
    Player(name="Ian"),
    Player(name="Jack"),
    Player(name="Karen"),
    Player(name="Liam"),
    Player(name="Mia"),
    Player(name="Noah"),
    Player(name="Olivia"),
    Player(name="Peter")
]
# Create some dummy teams
teams = [
    Team(name="Raptors", members=players[:4]),
    Team(name="Sharks", members=players[4:8]),
    Team(name="Pumas", members=players[8:12]),
    Team(name="Owls", members=players[12:])
]

# Create the team tournament with four boards per game
tournament = RoundRobinTeamTournament(participants=teams)
tournament.parameters.boards = 4

# Get dictionaries to help later on
team_dict = tournament.get_participant_dict()
members_dict = {team.uuid: team.members for team in tournament.participants}

# Loop through rounds until the tournament is finished
round_number = 1
while not tournament.is_finished():
    # Get pairings
    tournament.generate_pairings()
    pairings = tournament.get_pairings()
    assert pairings is not None
    assert Pairings.is_finalized(pairings)
    team_pairings = tournament.get_team_pairings()
    assert team_pairings is not None

    # Assign players to boards
    for i, team_pairing in enumerate(team_pairings.items):
        for j, game_pairing in enumerate(team_pairing.items):
            assert team_pairing.team_1 is not None and team_pairing.team_2 is not None
            game_pairing.uuid_1.content = members_dict[team_pairing.team_1][j].uuid
            game_pairing.uuid_2.content = members_dict[team_pairing.team_2][j].uuid
        tournament.finalize_team_pairing(i, team_pairing)

    # Print pairing
    print("--------------------------------")
    print(f"      Pairing for round {round_number}      ")
    print("--------------------------------")
    for team_pairing in team_pairings.items:
        assert TeamPairing.is_finalized(team_pairing)
        assert team_pairing.team_1 is not None and team_pairing.team_2 is not None
        team_1 = team_dict[team_pairing.team_1]
        team_2 = team_dict[team_pairing.team_2]
        print(f"{team_1.name} vs {team_2.name}:")
        print_team_pairing(team_pairing, tournament)

    # Add results
    for i, team_pairing in enumerate(team_pairings.items):
        assert TeamPairing.is_finalized(team_pairing)
        team_game_result = TeamGameResult.from_team_pairing(team_pairing)
        for game_result in team_game_result.items:
            assign_random_game_result(game_result)
        tournament.add_team_game_result(i, team_game_result)
    round_result = tournament.states.results.rounds[-1]

    # Print results
    print("--------------------------------")
    print(f"      Results for round {round_number}      ")
    print("--------------------------------")
    for team_game_result in tournament.states.team_results.rounds[-1].items:
        assert TeamGameResult.is_finalized(team_game_result)
        assert team_game_result.team_1 is not None and team_game_result.team_2 is not None
        team_1 = team_dict[team_game_result.team_1]
        team_2 = team_dict[team_game_result.team_2]
        print(f"{team_1.name} vs {team_2.name}:")
        print_team_game_result(team_game_result, tournament)

    round_number += 1

# Print out the final standings
standings = tournament.get_standings()
print("")
print("-----------------------------")
print("       Final Standings       ")
print("-----------------------------")
print(f"No.  Name\tPoints\tBoPo")
for i, item in enumerate(standings.items):
    print(f"{i + 1:<3}  {item.participant.name}\t{item.scores[0]}\t{item.scores[1]}")
