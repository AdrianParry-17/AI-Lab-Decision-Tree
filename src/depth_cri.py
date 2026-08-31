"""Run the depth-limited Entropy decision-tree experiment."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.models.decision_tree.objective import Entropy
from src.utils import DOCS_DIR, ExperimentConfig, run_experiment


MAX_DEPTH = 4
CONFIG = ExperimentConfig(
    title="Depth-Limited Decision Tree (Entropy)",
    method=(
        f"Keep the same `max_depth={MAX_DEPTH}` pre-pruning used by the Gini "
        "experiment, but select splits with weighted Entropy. Holding depth and "
        "data constant isolates the effect of changing the criterion."
    ),
    criterion_name="weighted Entropy",
    impurity=Entropy,
    max_depth=MAX_DEPTH,
)
RESULT_PATH = DOCS_DIR / "RESULT_DEPTH_CRI.md"


def main() -> int:
    outcome = run_experiment(CONFIG, RESULT_PATH)
    print(
        f"Wrote {RESULT_PATH}: test accuracy "
        f"{outcome.testing.accuracy:.2%}, error {outcome.testing.error_rate:.2%}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
