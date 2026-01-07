from collections import Counter
from typing import Dict, List, Tuple
from lib.round_sig_6 import round_sig_6
from type import (
    Transition,
    State,
    Label,
    ModifiedTransition,
    TransitionForDTMC,
    TransitionForMDP,
    TransitionForCTMC,
)


def output_results(n, t, transitions: List[Transition], states: List[State]) -> None:
    # Print state and transition counts in one line
    print(f"{n} {t}")

    # Print transitions with new state IDs, sorted by source and destination IDs
    transition_counter = Counter(transitions)
    for (src, dest), count in transition_counter.items():
        print(f"{src} {dest} {count}")

    # Print states with new state IDs, sorted by new state ID
    for state_id, state_content in states:
        print(f"{state_id} {{{state_content.strip()}}}")


def output_modified_results(
    n,
    t,
    transitions: List[ModifiedTransition],
    states: List[State],
    labels: List[Label],
) -> None:
    # Print state and transition counts in one line
    print("nodes transitions")
    print(f"{n} {t}")

    # Print modified transitions with new state IDs, sorted by source and destination IDs
    print("\nsrc dest count rule_name action weight rate reward")
    for src, dest, count, rule_name, action, weight, rate, reward in transitions:
        print(f"{src} {dest} {count} {rule_name} {action} {weight} {rate} {reward}")

    # Print states with new state IDs, sorted by new state ID
    print("\nstate_id state_content")
    for state_id, state_content in states:
        print(f"{state_id} {{{state_content.strip()}}}")

    # Print labels
    print("\nstate_id label")
    for state_id, label in labels:
        print(f"{state_id} {label}")


def output_dtmc(n: int, t: int, prob_transitions: List[TransitionForDTMC]) -> None:
    """
    遷移確率データを指定された形式で出力します。

    Args:
        prob_transitions (List[ProbTransition]): 確率付き遷移系
    """
    # Prepare output
    output_lines = []
    output_lines.append(f"{n} {t}")
    for from_state, to_state, prob in sorted(prob_transitions):
        prob_str = round_sig_6(prob)
        output_lines.append(f"{from_state} {to_state} {prob_str}")

    # Print output
    print("\n".join(output_lines))


def output_mdp(n: int, t: int, mdp_transitions: List[TransitionForMDP]) -> None:
    """
    MDP遷移確率データを指定された形式で出力します。

    Args:
        mdp_transitions (List[TransitionForMDP]): MDP遷移系
    """
    # Prepare output
    output_lines = []
    choice_count = 0
    choice_bf = -1

    for from_state, choice_id, to_state, prob, _ in sorted(mdp_transitions):
        prob_str = round_sig_6(prob)
        if choice_id != choice_bf:
            choice_count += 1
            choice_bf = choice_id
        output_lines.append(f"{from_state} {choice_id} {to_state} {prob_str}")

    # Print output
    print(f"{n} {choice_count} {t}")
    print("\n".join(output_lines))


def output_ctmc(n: int, t: int, rate_transitions: List[TransitionForCTMC]) -> None:
    """
    遷移率データを指定された形式で出力します。

    Args:
        rate_transitions (List[TransitionForCTMC]): レート付き遷移系
    """
    # Prepare output
    output_lines = []
    output_lines.append(f"{n} {t}")
    for from_state, to_state, rate in sorted(rate_transitions):
        output_lines.append(f"{from_state} {to_state} {rate}")

    # Print output
    print("\n".join(output_lines))


def output_labels(labels: List[Label]) -> None:
    """
    ラベルデータを出力します。

    Args:
        labels (List[Label]): ラベルデータ
    """
    # Create a dictionary to store labels for each state
    labelId2LabelStr: Dict[int, str] = {0: "init"}  # Default label
    labelStr2labelId: Dict[str, int] = {"init": 0}
    stateId2LabelIds: Dict[int, List[int]] = {0: [0]}

    labelStrSet = set()
    currentLabelId = 1
    for state_id, label in labels:
        if label not in labelStrSet:
            labelStrSet.add(label)
            labelStr2labelId[label] = currentLabelId
            labelId2LabelStr[currentLabelId] = label
            currentLabelId += 1
        if state_id not in stateId2LabelIds:
            stateId2LabelIds[state_id] = []
        stateId2LabelIds[state_id].append(labelStr2labelId[label])

    # Output labels in the format: 0="init" 1="one" ...
    label_strings = [
        f'{label_id}="{label}"' for label_id, label in sorted(labelId2LabelStr.items())
    ]
    print(" ".join(label_strings))

    # Output state-to-label mapping in the format: 0: 0
    for state_id in sorted(stateId2LabelIds.keys()):
        print(
            f"{state_id}: "
            + " ".join(str(label_id) for label_id in stateId2LabelIds[state_id])
        )


def output_trew(t: int, transitions: List[ModifiedTransition]) -> None:
    """
    報酬付き遷移データを指定された形式で出力します。

    Args:
        t (int): 遷移数
        transitions (List[ModifiedTransition]): 変更された遷移
    """
    trew = []
    for src, dest, _, _, _, _, _, reward in transitions:
        if reward == 0.0:
            continue
        reward_str = round_sig_6(reward)
        trew.append(f"{src} {dest} {reward_str}")

    print(f"{t} {len(trew)}\n" + "\n".join(trew))


def output_dtmc_for_state_viewer(
    n: int,
    t: int,
    transitions: List[ModifiedTransition],
    states: List[State],
    dtmc_transitions: List[TransitionForDTMC],
    labels: List[Label],
) -> None:
    """
    状態ビューア用の出力を生成します。

    Args:
        n (int): 状態数
        t (int): 遷移数
        transitions (List[ModifiedTransition]): 変更された遷移
        states (List[State]): 状態
        prob_transitions (List[ProbTransition]): 確率付き遷移系
    """
    # Print state and transition counts in one line
    print(f"{n} {t}")

    # (src, dest) -> probability map
    prob_map: Dict[Tuple[int, int], float] = {}
    for from_state, to_state, prob in dtmc_transitions:
        prob_map[(from_state, to_state)] = prob

    # Print modified transitions with new state IDs, sorted by source and destination IDs
    for src, dest, _, rule_name, _, _, _, _ in transitions:
        prob_str = round_sig_6(prob_map.get((src, dest), 0.0))
        print(f"{src} {dest} {rule_name} {prob_str}")

    # Print states with new state IDs, sorted by new state ID
    printStates(labels, states)


def output_mdp_for_state_viewer(
    n: int,
    t: int,
    transitions: List[ModifiedTransition],
    states: List[State],
    mdp_transitions: List[TransitionForMDP],
    labels: List[Label],
) -> None:
    """
    状態ビューア用のMDP出力を生成します。
    """
    print(f"{n} {t}")

    # (src, action, dest) -> probability map
    prob_map: Dict[Tuple[int, str, int], float] = {}
    for from_state, _, to_state, prob, action in mdp_transitions:
        prob_map[(from_state, action, to_state)] = prob

    # Print modified transitions with new state IDs, sorted by source and destination IDs
    for src, dest, _, rule_name, action, _, _, _ in transitions:
        prob_str = round_sig_6(prob_map.get((src, action, dest), 0.0))
        print(f"{src} {dest} {rule_name} {action},{prob_str}")

    # Print states with new state IDs, sorted by new state ID
    printStates(labels, states)


def output_ctmc_for_state_viewer(
    n: int,
    t: int,
    transitions: List[ModifiedTransition],
    states: List[State],
    ctmc_transitions: List[TransitionForCTMC],
    labels: List[Label],
) -> None:
    """
    状態ビューア用のCTMC出力を生成します。
    """
    print(f"{n} {t}")

    # (src, dest) -> rate map
    rate_map: Dict[Tuple[int, int], float] = {}
    for from_state, to_state, rate in ctmc_transitions:
        rate_map[(from_state, to_state)] = rate

    # Print modified transitions with new state IDs, sorted by source and destination IDs
    for src, dest, _, rule_name, _, _, _, _ in transitions:
        print(f"{src} {dest} {rule_name} {rate_map.get((src, dest), 1.0)}")

    # Print states with new state IDs, sorted by new state ID
    printStates(labels, states)


def printStates(labels: List[Label], states: List[State]) -> None:
    """
    状態とラベルを標準出力に出力します。

    Args:
        labels (List[Label]): ラベルデータ
        states (List[State]): 状態データ
    """
    # label Dictionary
    label_map: Dict[int, List[str]] = {}
    for state_id, label in labels:
        if state_id not in label_map:
            label_map[state_id] = []
        label_map[state_id].append(label)

    # Print states with new state IDs, sorted by new state ID
    for state_id, state_content in states:
        label_str = ""
        if state_id in label_map:
            label_str = " " + ",".join(label_map[state_id])
        print(f"{state_id} {{{state_content.strip()}}}{label_str}")
