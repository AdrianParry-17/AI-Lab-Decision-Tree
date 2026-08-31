"""Run the depth-limited Gini decision-tree experiment."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.models.decision_tree.objective import Gini
from src.utils import DOCS_DIR, ExperimentConfig, run_experiment


MAX_DEPTH = 4
CONFIG = ExperimentConfig(
    title="Depth-Limited Decision Tree (Gini)",
    method=(
        f"Apply pre-pruning with `max_depth={MAX_DEPTH}` while retaining the "
        "baseline Gini criterion. Limiting growth should reduce variance and "
        "prevent the tree from memorizing small training partitions."
    ),
    criterion_name="weighted Gini impurity",
    impurity=Gini,
    max_depth=MAX_DEPTH,
)
RESULT_PATH = DOCS_DIR / "RESULT_DEPTH.md"


def main() -> int:
    outcome = run_experiment(CONFIG, RESULT_PATH)
    print(
        f"Wrote {RESULT_PATH}: test accuracy "
        f"{outcome.testing.accuracy:.2%}, error {outcome.testing.error_rate:.2%}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
