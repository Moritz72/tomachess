from pathlib import Path

from tomachess.participant import Player, Team
from tomachess.tournament.round_robin import RoundRobinTeamTournament
from tomachess.store import SqlStore

from helper_functions import print_tournament_teams

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

# Create the tournament
tournament = RoundRobinTeamTournament(participants=teams)

# Initialize SQL store
sql_store = SqlStore(Path("./examples/sql_store.db"))

# Save the tournament to the store
sql_store.save_team_tournaments("tournament_collection", [tournament])

# Load the tournament from the store
tournaments = sql_store.load_team_tournaments("tournament_collection")
loaded_tournament = tournaments[0]

# Print the tournament participants
print("--------------")
print(" Participants ")
print("--------------")
print_tournament_teams(loaded_tournament)
