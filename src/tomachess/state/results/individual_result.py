from enum import Enum


class IndividualResult(str, Enum):
    WIN = "win"
    DRAW = "draw"
    LOSS = "loss"
    FORFEIT_WIN = "forfeit_win"
    FORFEIT_LOSS = "forfeit_loss"
    VOLUNTARY_BYE = "voluntary_bye"
    PAIRING_ALLOCATED_BYE = "pairing_allocated_bye"
    UNDEFINED = "undefined"

    _UNPLAYED = {FORFEIT_WIN, FORFEIT_LOSS, VOLUNTARY_BYE, PAIRING_ALLOCATED_BYE, UNDEFINED}
    _VOLUNTARILY_UNPLAYED = {FORFEIT_LOSS, VOLUNTARY_BYE}

    @property
    def unplayed(self) -> bool:
        return self in self._UNPLAYED

    @property
    def voluntarily_unplayed(self) -> bool:
        return self in self._VOLUNTARILY_UNPLAYED
