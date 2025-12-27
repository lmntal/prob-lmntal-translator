from typing import Dict, List, Tuple

RawTransition = Tuple[str, str]  # (src, dest)
RawState = Tuple[str, str]  # (state_id, state_content)
RawLabel = Tuple[str, str]  # (state_id, label)

Transition = Tuple[int, int]  # (src, dest)
State = Tuple[int, str]  # (state_id, state_content)
Label = Tuple[int, str]  # (state_id, label)

ModifiedTransition = Tuple[
    int, int, int, str, str, float, float, float
]  # (src, dest, count, rule_name, action, weight, rate, reward)


class AdjacencyItem:
    def __init__(
        self, dest: int, count: int, action: str, weight: float, rate: float
    ) -> None:
        self.dest = dest
        self.count = count
        self.action = action
        self.weight = weight
        self.rate = rate


TransitionsAdjacencyList = Dict[
    int, List[AdjacencyItem]
]  # from_state -> List of (to_state, weight, match_count)

TransitionForDTMC = Tuple[int, int, float]  # (from_state, to_state, probability)
TransitionForMDP = Tuple[int, int, int, float] # (from_state, choice_id, to_state, probability)
TransitionForCTMC = Tuple[int, int, float]  # (from_state, to_state, rate)
