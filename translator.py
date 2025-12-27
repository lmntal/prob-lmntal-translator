import sys
import argparse
from parse_input import parse_input
from modifier import normalize, modify_transitions
from transition_generator import (
    generate_transitions_adjacency_list,
    generate_dtmc,
    generate_ctmc,
)
from output import (
    output_results,
    output_modified_results,
    output_dtmc,
    output_ctmc,
    output_labels,
    output_trew,
    output_for_state_viewer,
)
from type import (
    TransitionsAdjacencyList,
)


def main() -> None:
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process transition data.")

    parser.add_argument(
        "--model-type",
        type=str,
        choices=["dtmc", "mdp", "ctmc"],
        default="dtmc",
        help="Specify the type of model (dtmc, mdp, ctmc). Default is dtmc.",
    )
    parser.add_argument(
        "--output-normalized",
        action="store_true",
        help="Output normalized transitions and states.",
    )
    parser.add_argument(
        "--output-modified",
        action="store_true",
        help="Output modified transitions and states.",
    )
    parser.add_argument(
        "--output-for-prism", action="store_true", help="Output DTMC transitions."
    )
    parser.add_argument(
        "--output-state-viewer",
        action="store_true",
        help="Output data for state viewer.",
    )
    parser.add_argument(
        "--tra", type=str, help="Specify output file for --output-for-prism."
    )
    parser.add_argument(
        "--lab", type=str, help="Specify output file for --output-for-prism."
    )
    parser.add_argument(
        "--trew", type=str, help="Specify output file for --output-for-prism."
    )
    args = parser.parse_args()

    # Read input from stdin
    input_data = sys.stdin.read()

    try:
        n, t, initial_state_id, raw_transitions, raw_states, raw_labels = parse_input(
            input_data
        )
        normalized_transitions, normalized_states, normalized_labels = normalize(
            initial_state_id, raw_transitions, raw_states, raw_labels
        )

        if args.output_normalized:
            output_results(n, t, normalized_transitions, normalized_states)
        elif args.output_modified:
            n, t, transitions, states, labels = modify_transitions(
                normalized_transitions, normalized_states, normalized_labels
            )
            output_modified_results(n, t, transitions, states, labels)
        elif args.output_for_prism:
            n, t, transitions_with_info, _, labels = modify_transitions(
                normalized_transitions, normalized_states, normalized_labels
            )
            transitions: TransitionsAdjacencyList = generate_transitions_adjacency_list(
                transitions_with_info
            )

            if args.model_type == "dtmc":
                dtmc_transitions = generate_dtmc(transitions)

                if args.tra:
                    with open(args.tra, "w") as f:
                        sys.stdout = f  # Redirect stdout to file
                        output_dtmc(n, t, dtmc_transitions)
                        sys.stdout = sys.__stdout__  # Reset stdout
                else:
                    output_dtmc(n, t, dtmc_transitions)

                if args.lab:
                    with open(args.lab, "w") as f:
                        sys.stdout = f  # Redirect stdout to file
                        output_labels(labels)
                        sys.stdout = sys.__stdout__  # Reset stdout
                else:
                    output_labels(labels)

                if args.trew:
                    with open(args.trew, "w") as f:
                        sys.stdout = f  # Redirect stdout to file
                        output_trew(t, transitions_with_info)
                        sys.stdout = sys.__stdout__  # Reset stdout
            elif args.model_type == "mdp":
                print("MDP output not implemented yet.", file=sys.stderr)
            elif args.model_type == "ctmc":
                ctmc_transitions = generate_ctmc(transitions)

                if args.tra:
                    with open(args.tra, "w") as f:
                        sys.stdout = f  # Redirect stdout to file
                        output_ctmc(n, t, ctmc_transitions)
                        sys.stdout = sys.__stdout__  # Reset stdout
                else:
                    output_ctmc(n, t, ctmc_transitions)

                if args.lab:
                    with open(args.lab, "w") as f:
                        sys.stdout = f  # Redirect stdout to file
                        output_labels(labels)
                        sys.stdout = sys.__stdout__  # Reset stdout
                else:
                    output_labels(labels)

        elif args.output_state_viewer:
            n, t, transitions_with_info, states, labels = modify_transitions(
                normalized_transitions, normalized_states, normalized_labels
            )
            transitions: TransitionsAdjacencyList = generate_transitions_adjacency_list(
                transitions_with_info
            )
            if args.model_type == "dtmc":
                dtmc_transitions = generate_dtmc(transitions)
                output_for_state_viewer(
                    n, t, transitions_with_info, states, dtmc_transitions, labels
                )
            elif args.model_type == "mdp":
                print(
                    "MDP output for state viewer not implemented yet.", file=sys.stderr
                )
            elif args.model_type == "ctmc":
                print(
                    "CTMC output for state viewer not implemented yet.", file=sys.stderr
                )
        else:
            print("Error: No valid output option provided.", file=sys.stderr)
    except ValueError as e:
        print(e, file=sys.stderr)


if __name__ == "__main__":
    main()
