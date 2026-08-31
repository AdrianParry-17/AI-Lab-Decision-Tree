"""Train the repository's decision tree on the student CSV and export it."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Sequence

from model.data.supervised import ValueSupervisedData
from model.models.decision_tree.split import (
    AttributeThresholdSplit,
    AttributeValueSplit,
)
from model.models.decision_tree.standard import (
    CreateAttributeClassificationTrainingStrategy,
)
from model.models.decision_tree.training_strategy import FunctionStoppingCriterion
from model.models.decision_tree.tree import (
    DecisionTree,
    DistributorBranchNode,
    INode,
    ValueNode,
)


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "student_data.csv"
RESULT_PATH = BASE_DIR / "RESULT.md"

ID_COLUMN = "Student_ID"
TARGET_COLUMN = "Pass_Fail"
EXCLUDED_FEATURE_COLUMNS = {ID_COLUMN, "Final_Exam_Score"}
INTEGER_COLUMNS = {
    "Study_Hours_per_Week",
    "Past_Exam_Scores",
}
FLOAT_COLUMNS = {"Attendance_Rate"}

FeatureValue = str | int | float
ModelInput = list[tuple[str, FeatureValue]]
TrainingExample = ValueSupervisedData[ModelInput, str]


def _parse_feature(name: str, raw_value: str) -> FeatureValue:
    """Convert numeric CSV fields while preserving categorical strings."""
    value = raw_value.strip()
    if value == "":
        raise ValueError(f"Missing value in feature {name!r}")
    if name in INTEGER_COLUMNS:
        return int(value)
    if name in FLOAT_COLUMNS:
        return float(value)
    return value


def load_data(path: Path) -> tuple[list[TrainingExample], list[str]]:
    """Load rows, exclude disallowed inputs, and map to library data objects."""
    with path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None:
            raise ValueError(f"{path} has no CSV header")

        required_columns = {ID_COLUMN, TARGET_COLUMN}
        missing_columns = required_columns.difference(reader.fieldnames)
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"CSV is missing required column(s): {missing}")

        feature_names = [
            name
            for name in reader.fieldnames
            if name not in EXCLUDED_FEATURE_COLUMNS | {TARGET_COLUMN}
        ]
        examples: list[TrainingExample] = []

        for line_number, row in enumerate(reader, start=2):
            try:
                inputs = [
                    (name, _parse_feature(name, row[name]))
                    for name in feature_names
                ]
                output = row[TARGET_COLUMN].strip()
                if output == "":
                    raise ValueError(f"Missing target {TARGET_COLUMN!r}")
            except (TypeError, ValueError) as error:
                raise ValueError(f"Invalid data on CSV line {line_number}: {error}") from error

            examples.append(ValueSupervisedData(inputs, output))

    if not examples:
        raise ValueError(f"{path} contains no data rows")

    return examples, feature_names


def train(examples: Sequence[TrainingExample]) -> DecisionTree[ModelInput, str]:
    """Train through the custom library's standard classification strategy."""
    tree: DecisionTree[ModelInput, str] = DecisionTree()
    strategy = CreateAttributeClassificationTrainingStrategy(
        examples,
        input_getter=lambda example: example.GetInput(),
        output_getter=lambda example: example.GetOutput(),
    )
    # The library intentionally leaves stopping policy to its caller.  Without
    # this, it can add a redundant split even after a node is already pure.
    strategy.StoppingCriterion = FunctionStoppingCriterion(
        lambda state: len({example.GetOutput() for example in state.Data}) == 1
    )
    strategy.Train(tree)
    return tree


def _split_title(split: object) -> str:
    if isinstance(split, AttributeThresholdSplit):
        return f"Split on `{split.AttributeName}` at `{split.Threshold:g}`"
    if isinstance(split, AttributeValueSplit):
        return f"Split on categorical feature `{split.AttributeName}`"
    return f"Split using `{type(split).__name__}`"


def _branch_condition(split: object, branch: object) -> str:
    if isinstance(split, AttributeThresholdSplit):
        operator = "<=" if branch is True else ">"
        return f"`{split.AttributeName}` {operator} `{split.Threshold:g}`"
    if isinstance(split, AttributeValueSplit):
        return f"`{split.AttributeName}` = `{branch}`"
    return f"branch `{branch!r}`"


def _ordered_children(items: Sequence[tuple[object, INode]]) -> list[tuple[object, INode]]:
    """Put a threshold's <= branch first and keep other exports deterministic."""
    return sorted(items, key=lambda item: (item[0] is not True, repr(item[0])))


def render_tree(node: INode, indentation: str = "") -> list[str]:
    """Turn the inspectable custom tree nodes into a readable text tree."""
    if isinstance(node, ValueNode):
        return [f"{indentation}Predict `{node.Output}`"]

    if not isinstance(node, DistributorBranchNode):
        return [f"{indentation}{type(node).__name__}"]

    distributor = node.GetDistributor()
    split = distributor.GetSplit()
    children = _ordered_children(tuple(distributor.GetMapping().GetItems()))
    lines = [f"{indentation}{_split_title(split)}"]

    for index, (branch, child) in enumerate(children):
        is_last = index == len(children) - 1
        connector = "└──" if is_last else "├──"
        continuation = "    " if is_last else "│   "
        condition = _branch_condition(split, branch)

        if isinstance(child, ValueNode):
            lines.append(
                f"{indentation}{connector} If {condition}: Predict `{child.Output}`"
            )
        else:
            lines.append(f"{indentation}{connector} If {condition}:")
            lines.extend(render_tree(child, indentation + continuation))

    return lines


def tree_statistics(node: INode, depth: int = 0) -> tuple[int, int, int]:
    """Return total nodes, leaf nodes, and maximum root-based depth."""
    if isinstance(node, ValueNode):
        return 1, 1, depth
    if not isinstance(node, DistributorBranchNode):
        return 1, 0, depth

    child_stats = [
        tree_statistics(child, depth + 1)
        for _, child in node.GetDistributor().GetMapping().GetItems()
    ]
    return (
        1 + sum(nodes for nodes, _, _ in child_stats),
        sum(leaves for _, leaves, _ in child_stats),
        max(max_depth for _, _, max_depth in child_stats),
    )


def build_result(
    tree: DecisionTree[ModelInput, str],
    examples: Sequence[TrainingExample],
    feature_names: Sequence[str],
) -> str:
    root = tree.GetRoot()
    if root is None:
        raise RuntimeError("Training completed without producing a root node")

    labels = sorted({example.GetOutput() for example in examples})
    predictions = [tree.Execute(example.GetInput()) for example in examples]
    correct = sum(
        prediction == example.GetOutput()
        for example, prediction in zip(examples, predictions)
    )
    accuracy = correct / len(examples)
    counts = Counter(
        (example.GetOutput(), prediction)
        for example, prediction in zip(examples, predictions)
    )
    nodes, leaves, max_depth = tree_statistics(root)

    confusion_header = "| Actual \\ Predicted | " + " | ".join(labels) + " |"
    confusion_rule = "| --- | " + " | ".join("---:" for _ in labels) + " |"
    confusion_rows = [
        f"| {actual} | "
        + " | ".join(str(counts[(actual, predicted)]) for predicted in labels)
        + " |"
        for actual in labels
    ]

    tree_text = "\n".join(render_tree(root))
    features = ", ".join(f"`{name}`" for name in feature_names)
    return "\n".join(
        [
            "# Decision Tree Training Result",
            "",
            "## Data and preprocessing",
            "",
            f"- Source: `data/{DATA_PATH.name}`",
            f"- Training rows: {len(examples)}",
            f"- Target: `{TARGET_COLUMN}`",
            "- Excluded inputs: `Student_ID` (identifier), `Final_Exam_Score`",
            f"- Features ({len(feature_names)}): {features}",
            "- Numeric CSV values were converted to `int`/`float`; categorical values remain strings.",
            "",
            "## Model summary",
            "",
            "- Trainer: custom `CreateAttributeClassificationTrainingStrategy`",
            "- Split objective: weighted Gini impurity",
            "- Stopping rule: make a leaf when all local labels are identical",
            f"- Nodes: {nodes}",
            f"- Leaves: {leaves}",
            f"- Maximum depth: {max_depth}",
            f"- Training accuracy: {correct}/{len(examples)} ({accuracy:.2%})",
            "",
            "The accuracy above is measured on the training data; no holdout evaluation was requested.",
            "",
            "## Confusion matrix (training data)",
            "",
            confusion_header,
            confusion_rule,
            *confusion_rows,
            "",
            "## Final tree",
            "",
            "```text",
            tree_text,
            "```",
            "",
        ]
    )


def main() -> int:
    examples, feature_names = load_data(DATA_PATH)
    tree = train(examples)
    RESULT_PATH.write_text(
        build_result(tree, examples, feature_names),
        encoding="utf-8",
    )
    print(f"Trained on {len(examples)} rows and wrote {RESULT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
