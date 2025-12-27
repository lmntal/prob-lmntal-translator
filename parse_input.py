import re
from typing import List, Tuple
from type import RawTransition, RawState, RawLabel


def parse_input(
    input_data: str,
) -> Tuple[int, int, str, List[RawTransition], List[RawState]]:
    """
    メタインタプリタの実行結果をパースして，状態数，遷移数，初期状態ID，遷移，状態を抽出します．
    """
    # Extract n (state count) and t (transition count)
    n_match = re.search(r"n\((\d+)\)", input_data)
    t_match = re.search(r"t\((\d+)\)", input_data)

    if not n_match or not t_match:
        raise ValueError("Error: Could not find state or transition count.")

    n = int(n_match.group(1))
    t = int(t_match.group(1))

    # Extract initial state ID
    initial_state_match = re.search(r"ret\(ss\((\d+),<state_map>", input_data)
    if not initial_state_match:
        raise ValueError("Error: Could not find initial state ID.")

    initial_state_id = initial_state_match.group(1)

    # Extract transitions
    transitions_match = re.search(r"transitions\(\[(.*?)\]\)", input_data, re.DOTALL)
    if not transitions_match:
        raise ValueError("Error: Could not find transitions.")

    transitions_raw = transitions_match.group(1)
    transitions_raw: List[RawTransition] = re.findall(
        r"\[(\d+)\|(\d+)\]", transitions_raw
    )

    # Extract states
    states_raw: List[RawState] = re.findall(
        r"state\((\d+),\{(.*?)\}\)", input_data, re.DOTALL
    )

    # Extract label
    labels_raw: List[RawLabel] = re.findall(r'label\((\d+),"([^"]+)"\)', input_data)

    return n, t, initial_state_id, transitions_raw, states_raw, labels_raw
