from pathlib import Path

from tomachess.participant import Player
from tomachess.tournament.round_robin import RoundRobinTournament
from tomachess.store import JsonStore

from helper_functions import print_tournament_players

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

# Initialize JSON store
json_store = JsonStore(Path("./examples/json_store"))

# Save the tournament to the store
json_store.save_tournaments("tournament_collection", [tournament])

# Load the tournament from the store
tournaments = json_store.load_tournaments("tournament_collection")
loaded_tournament = tournaments[0]

# Print the tournament participants
print("--------------")
print(" Participants ")
print("--------------")
print_tournament_players(loaded_tournament)
