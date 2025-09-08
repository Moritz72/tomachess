from tomachess.participant.player import Player
from tomachess.participant.team import Team

Participant = Player | Team

__all__ = ["Participant", "Player", "Team"]
