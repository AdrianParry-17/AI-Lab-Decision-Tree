"""Run the fully grown Gini decision-tree baseline."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.models.decision_tree.objective import Gini
from src.utils import DOCS_DIR, ExperimentConfig, run_experiment


CONFIG = ExperimentConfig(
    title="Fully Grown Decision Tree (Baseline)",
    method=(
        "Train with Gini impurity and no configured depth limit. The tree grows "
        "until each reachable training node is pure or cannot be split further. "
        "This is the baseline used to measure overfitting."
    ),
    criterion_name="weighted Gini impurity",
    impurity=Gini,
    max_depth=None,
)
RESULT_PATH = DOCS_DIR / "RESULT_PURE.md"


def main() -> int:
    outcome = run_experiment(CONFIG, RESULT_PATH)
    print(
        f"Wrote {RESULT_PATH}: test accuracy "
        f"{outcome.testing.accuracy:.2%}, error {outcome.testing.error_rate:.2%}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
