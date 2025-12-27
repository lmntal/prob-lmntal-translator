import re
from collections import Counter, deque
from typing import List, Tuple
from type import (
    RawTransition,
    RawState,
    RawLabel,
    Transition,
    State,
    Label,
    ModifiedTransition,
)


def normalize(
    initial_state_id: str,
    raw_transitions: List[RawTransition],
    raw_states: List[RawState],
    raw_labels: List[RawLabel],
) -> Tuple[List[Transition], List[State], List[Label]]:
    """
    状態の ID が 0 から昇順になるように正規化します．
    """
    # Build adjacency list for BFS
    adjacency_list = {}
    for src, dest in raw_transitions:
        if src not in adjacency_list:
            adjacency_list[src] = []
        adjacency_list[src].append(dest)

    # Perform BFS to assign new state IDs
    state_id_map = {}
    queue = deque([initial_state_id])
    state_id_map[initial_state_id] = 0
    next_id = 1

    while queue:
        current = queue.popleft()
        for neighbor in adjacency_list.get(current, []):
            if neighbor not in state_id_map:
                state_id_map[neighbor] = next_id
                next_id += 1
                queue.append(neighbor)

    # Normalize and sort transitions
    normalized_transitions: List[Transition] = sorted(
        [(state_id_map[src], state_id_map[dest]) for src, dest in raw_transitions],
        key=lambda x: (x[0], x[1]),
    )

    # Normalize and sort states
    normalized_states: List[State] = sorted(
        [
            (state_id_map[state_id], state_content)
            for state_id, state_content in raw_states
            if state_id in state_id_map
        ],
        key=lambda x: x[0],
    )

    # Normalize and sort labels
    normalized_labels: List[Label] = sorted(
        [
            (state_id_map[state_id], label)
            for state_id, label in raw_labels
            if state_id in state_id_map
        ],
        key=lambda x: x[0],
    )

    return normalized_transitions, normalized_states, normalized_labels


def modify_transitions(
    transitions: List[Transition], states: List[State], labels: List[Label]
) -> Tuple[int, int, List[ModifiedTransition], List[State], List[Label]]:
    """
    ルール情報などの付加のために追加されて中間ステップを削除した遷移系を生成する

    Args:
        transitions (list[tuple[int, int]]): 遷移
        states (list[tuple[int, str]]): 状態

    Returns:
        n (int): 状態数
        t (int): 遷移数
        modified_transitions (list[tuple[int, int, int, str, str, float, float, float]]):
            遷移 (src, dest, count, rule_name, action, weight, rate, reward)
        modified_states (list[tuple[int, str]]): 状態
        modified_labels (list[tuple[int, str]]): ラベル
    """

    new_transitions = []

    # Build adjacency list for BFS
    adjacency_list = {}
    for src, dest in transitions:
        if src not in adjacency_list:
            adjacency_list[src] = []
        adjacency_list[src].append(dest)

    state_id_map = {}
    queue = deque([0])
    state_id_map[0] = 0  # Ensure the initial state is mapped
    next_id = 1

    tra_rule_map = {}
    tra_action_map = {}
    tra_weight_map = {}
    tra_rate_map = {}
    tra_reward_map = {}

    while queue:
        current = queue.popleft()
        for way_point in adjacency_list.get(current, []):
            for neighbor in adjacency_list.get(way_point, []):
                new_transitions.append((current, neighbor))

                state_content = states[int(way_point)][1]

                # rule_name
                rule_name_match = re.search(r'rule_name\("([^"]+)"\)', state_content)
                if rule_name_match:
                    rule_name = rule_name_match.group(1)
                    tra_rule_map[(current, neighbor)] = rule_name

                # action
                action_match = re.search(r'action\("([^"]+)"\)', state_content)
                if action_match:
                    action = action_match.group(1)
                    tra_action_map[(current, neighbor)] = action

                # weight
                weight_match = re.search(r"weight\(([\d\.]+)\)", state_content)
                if weight_match:
                    weight = float(weight_match.group(1))
                    tra_weight_map[(current, neighbor)] = weight

                # rate
                rate_match = re.search(r"rate\(([\d\.]+)\)", state_content)
                if rate_match:
                    rate = float(rate_match.group(1))
                    tra_rate_map[(current, neighbor)] = rate

                # reward
                reward_match = re.search(r"reward\(([\d\.]+)\)", state_content)
                if reward_match:
                    reward = float(reward_match.group(1))
                    tra_reward_map[(current, neighbor)] = reward

                if neighbor not in state_id_map:
                    state_id_map[neighbor] = next_id
                    next_id += 1
                    queue.append(neighbor)

    n = len(state_id_map)
    t = len(Counter(new_transitions))

    modified_transitions: List[ModifiedTransition] = []
    for (src, dest), count in Counter(new_transitions).items():
        modified_transitions.append(
            (
                state_id_map.get(src, "UNKNOWN"),
                state_id_map.get(dest, "UNKNOWN"),
                count,
                tra_rule_map.get((src, dest), "UNKNOWN"),
                tra_action_map.get((src, dest), "UNKNOWN"),
                tra_weight_map.get((src, dest), 1.0),
                tra_rate_map.get((src, dest), 1.0),
                tra_reward_map.get((src, dest), 0.0),
            )
        )

    modified_states: List[State] = []
    for state_id, state_content in states:
        if state_id in state_id_map:
            modified_states.append((state_id_map[state_id], state_content.strip()))

    modified_labels: List[Label] = []
    for state_id, label in labels:
        if state_id in state_id_map:
            modified_labels.append((state_id_map[state_id], label.strip()))

    return n, t, modified_transitions, modified_states, modified_labels
