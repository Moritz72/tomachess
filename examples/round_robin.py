from tomachess.participant import Player
from tomachess.state import Pairings
from tomachess.state.results import RoundResult
from tomachess.tournament.round_robin import RoundRobinTournament

from helper_functions import assign_random_game_result, print_pairings, print_round_result


# Create some dummy players
players = [
    Player(name="Alice"),
    Player(name="Bob"),
    Player(name="Charlie"),
    Player(name="Diana"),
    Player(name="Ethan"),
    Player(name="Fiona"),
    Player(name="George"),
    Player(name="Hannah"),
    Player(name="Ian")
]

# Create the tournament
tournament = RoundRobinTournament(participants=players)

# Loop through rounds until the tournament is finished
round_number = 1
while not tournament.is_finished():
    # Get pairings
    tournament.generate_pairings()
    pairings = tournament.get_pairings()
    assert pairings is not None
    assert Pairings.is_finalized(pairings)

    # Print pairing
    print("------------------------")
    print(f"  Pairing for round {round_number}  ")
    print("------------------------")
    print_pairings(pairings, tournament)

    # Add results
    round_result = RoundResult.from_pairings(pairings)
    for game_result in round_result.items:
        assign_random_game_result(game_result)
    assert RoundResult.is_finalized(round_result)
    tournament.add_round_result(round_result)

    # Print results
    print("------------------------")
    print(f"  Results for round {round_number}  ")
    print("------------------------")
    print_round_result(round_result, tournament)

    round_number += 1

# Print out the final standings
standings = tournament.get_standings()
print("")
print("-----------------------------")
print("       Final Standings       ")
print("-----------------------------")
print(f"No.  Name\tPoints\tSoBe")
for i, item in enumerate(standings.items):
    print(f"{i + 1:<3}  {item.participant.name}\t{item.scores[0]}\t{item.scores[1]}")
