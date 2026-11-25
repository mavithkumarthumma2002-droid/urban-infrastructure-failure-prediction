"""Runs the project pipeline.

    python main.py                 run every step in order
    python main.py STEP [STEP ...] run only the named steps (still in pipeline order)

Each step reads what the step before it saved, so on a fresh copy run
everything once first.
"""
import sys

from src import data

STEPS = {
    "explore": data.main,
}


def main(args):
    unknown = [a for a in args if a not in STEPS]
    if unknown:
        sys.exit(f"Unknown step(s): {', '.join(unknown)}. Choose from: {', '.join(STEPS)}")

    for name, step in STEPS.items():
        if args and name not in args:
            continue
        print(f"\n--- {name} ---")
        step()


if __name__ == "__main__":
    main(sys.argv[1:])
