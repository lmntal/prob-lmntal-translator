from typing import List
from type import (
    AdjacencyItem,
    ModifiedTransition,
    TransitionsAdjacencyList,
    TransitionForDTMC,
    TransitionForCTMC,
)


def generate_transitions_adjacency_list(
    modified_transitions: List[ModifiedTransition],
) -> TransitionsAdjacencyList:
    transitions: TransitionsAdjacencyList = {}
    for src, dest, count, _, action, weight, rate, _ in modified_transitions:
        if src not in transitions:
            transitions[src] = []
        transitions[src].append(
            AdjacencyItem(
                dest=dest, count=count, action=action, weight=weight, rate=rate
            )
        )
    return transitions


def generate_dtmc(
    transitions: TransitionsAdjacencyList,
) -> List[TransitionForDTMC]:
    """
    遷移データと重みから遷移確率を計算します．

    Args:
        transitions (TransitionsAdjacencyList): 遷移データ

    Returns:
        List[TransitionForDTMC]: (開始状態, 終了状態, 確率)のタプルのリスト
    """
    dtmc_transitions: List[TransitionForDTMC] = []

    for from_state, to_states in transitions.items():
        if not to_states:
            continue

        # Calculate total weight
        total_weight = sum(
            adjacency.weight * adjacency.count for adjacency in to_states
        )

        # Calculate probability for each transition
        for adjacency in to_states:
            prob = (adjacency.weight * adjacency.count) / total_weight
            dtmc_transitions.append((from_state, adjacency.dest, prob))

    return dtmc_transitions


def generate_ctmc(
    transitions: TransitionsAdjacencyList,
) -> List[TransitionForCTMC]:
    """
    遷移データとレートから遷移率を計算します．

    Args:
        transitions (TransitionsAdjacencyList): 遷移データ

    Returns:
        List[TransitionForCTMC]: (開始状態, 終了状態, レート)のタプルのリスト
    """
    ctmc_transitions: List[TransitionForCTMC] = []

    for from_state, to_states in transitions.items():
        if not to_states:
            continue

        # Calculate rate for each transition
        for adjacency in to_states:
            ctmc_transitions.append(
                (from_state, adjacency.dest, adjacency.rate * (float)(adjacency.count))
            )

    return ctmc_transitions
