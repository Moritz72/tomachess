from __future__ import annotations

from typing import TYPE_CHECKING

from tomachess.registry.generic_registry import GenericRegistry

if TYPE_CHECKING:
    from tomachess.base import TournamentBase, TeamTournamentBase


class TournamentRegistry(GenericRegistry["TournamentBase"]):
    pass


class TeamTournamentRegistry(GenericRegistry["TeamTournamentBase"]):
    pass
