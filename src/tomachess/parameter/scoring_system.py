from tomachess.models.parameter import Parameter
from tomachess.state.results import IndividualResult


class ScoringSystem(Parameter):
    win: float = 1.0
    draw: float = 0.5
    loss: float = 0.0
    bye: float = 0.0

    def get_points(self, individual_result: IndividualResult) -> float:
        match individual_result:
            case IndividualResult.WIN | IndividualResult.FORFEIT_WIN | IndividualResult.PAIRING_ALLOCATED_BYE:
                return self.win
            case IndividualResult.DRAW:
                return self.draw
            case IndividualResult.LOSS | IndividualResult.FORFEIT_LOSS:
                return self.loss
            case IndividualResult.VOLUNTARY_BYE:
                return self.bye
            case _:
                return 0.0
