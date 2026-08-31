"""Train and evaluate the repository's decision tree on the student CSV."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from random import Random
from typing import Sequence

from data.loader import (
    TARGET_COLUMN,
    FeatureValue,
    ModelInput,
    TrainingExample,
    load_data,
)
from model.models.decision_tree.split import (
    AttributeThresholdSplit,
    AttributeValueSplit,
)
from model.models.decision_tree.standard import (
    CreateAttributeClassificationTrainingStrategy,
)
from model.models.decision_tree.training_strategy import (
    AnyStoppingCriterion,
    FunctionStoppingCriterion,
)
from model.models.decision_tree.tree import (
    DecisionTree,
    DistributorBranchNode,
    INode,
    ValueNode,
)


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "student_data.csv"
RESULT_PATH = BASE_DIR / "RESULT.md"

TRAINING_FRACTION = 3 / 4
RANDOM_SEED = 42
MAX_DEPTH = 4


def _example_key(
    example: TrainingExample,
) -> tuple[tuple[tuple[str, FeatureValue], ...], str]:
    """Identify repeated labeled records without using them as model features."""
    return tuple(example.GetInput()), example.GetOutput()


def _allocate_training_groups(
    group_counts: dict[str, int],
    training_group_count: int,
) -> dict[str, int]:
    """Allocate an exact group count while preserving class proportions."""
    total_groups = sum(group_counts.values())
    allocations = {
        label: count * training_group_count // total_groups
        for label, count in group_counts.items()
    }
    groups_left = training_group_count - sum(allocations.values())
    remainder_order = sorted(
        group_counts,
        key=lambda label: (
            -(group_counts[label] * training_group_count % total_groups),
            repr(label),
        ),
    )

    for label in remainder_order[:groups_left]:
        allocations[label] += 1

    return allocations


def split_data(
    examples: Sequence[TrainingExample],
    training_fraction: float = TRAINING_FRACTION,
    random_seed: int = RANDOM_SEED,
) -> tuple[list[TrainingExample], list[TrainingExample]]:
    """Make a reproducible stratified split without leaking duplicate rows."""
    if not 0.0 < training_fraction < 1.0:
        raise ValueError("[training_fraction] must be between 0 and 1")

    duplicate_groups: dict[
        tuple[tuple[tuple[str, FeatureValue], ...], str],
        list[TrainingExample],
    ] = {}
    for example in examples:
        duplicate_groups.setdefault(_example_key(example), []).append(example)

    if len(duplicate_groups) < 2:
        raise ValueError("At least two distinct records are required for a split")

    groups_by_label: dict[str, list[list[TrainingExample]]] = {}
    for group in duplicate_groups.values():
        label = group[0].GetOutput()
        groups_by_label.setdefault(label, []).append(group)

    training_group_count = int(len(duplicate_groups) * training_fraction)
    if training_group_count == 0 or training_group_count == len(duplicate_groups):
        raise ValueError("The requested split would leave one partition empty")

    allocations = _allocate_training_groups(
        {label: len(groups) for label, groups in groups_by_label.items()},
        training_group_count,
    )
    random = Random(random_seed)
    training: list[TrainingExample] = []
    testing: list[TrainingExample] = []

    for label in sorted(groups_by_label, key=repr):
        groups = groups_by_label[label]
        random.shuffle(groups)
        split_index = allocations[label]
        training.extend(example for group in groups[:split_index] for example in group)
        testing.extend(example for group in groups[split_index:] for example in group)

    random.shuffle(training)
    random.shuffle(testing)
    return training, testing


def train(
    examples: Sequence[TrainingExample],
    max_depth: int = MAX_DEPTH,
) -> DecisionTree[ModelInput, str]:
    """Train through the custom library's standard classification strategy."""
    tree: DecisionTree[ModelInput, str] = DecisionTree()
    strategy = CreateAttributeClassificationTrainingStrategy(
        examples,
        input_getter=lambda example: example.GetInput(),
        output_getter=lambda example: example.GetOutput(),
        max_depth=max_depth,
    )
    pure_node_criterion = FunctionStoppingCriterion(
        lambda state: len({example.GetOutput() for example in state.Data}) == 1
    )
    if strategy.StoppingCriterion is None:
        strategy.StoppingCriterion = pure_node_criterion
    else:
        strategy.StoppingCriterion = AnyStoppingCriterion(
            (strategy.StoppingCriterion, pure_node_criterion)
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


def _evaluate(
    tree: DecisionTree[ModelInput, str],
    examples: Sequence[TrainingExample],
) -> tuple[int, Counter[tuple[str, str]]]:
    predictions = [tree.Execute(example.GetInput()) for example in examples]
    correct = sum(
        prediction == example.GetOutput()
        for example, prediction in zip(examples, predictions)
    )
    counts = Counter(
        (example.GetOutput(), prediction)
        for example, prediction in zip(examples, predictions)
    )
    return correct, counts


def _render_confusion_matrix(
    labels: Sequence[str],
    counts: Counter[tuple[str, str]],
) -> list[str]:
    header = "| Actual \\ Predicted | " + " | ".join(labels) + " |"
    rule = "| --- | " + " | ".join("---:" for _ in labels) + " |"
    rows = [
        f"| {actual} | "
        + " | ".join(str(counts[(actual, predicted)]) for predicted in labels)
        + " |"
        for actual in labels
    ]
    return [header, rule, *rows]


def _format_class_counts(examples: Sequence[TrainingExample]) -> str:
    counts = Counter(example.GetOutput() for example in examples)
    return ", ".join(
        f"`{label}`: {counts[label]}"
        for label in sorted(counts)
    )


def build_result(
    tree: DecisionTree[ModelInput, str],
    training_examples: Sequence[TrainingExample],
    testing_examples: Sequence[TrainingExample],
    feature_names: Sequence[str],
) -> str:
    root = tree.GetRoot()
    if root is None:
        raise RuntimeError("Training completed without producing a root node")

    all_examples = [*training_examples, *testing_examples]
    labels = sorted({example.GetOutput() for example in all_examples})
    training_correct, training_counts = _evaluate(tree, training_examples)
    testing_correct, testing_counts = _evaluate(tree, testing_examples)
    training_accuracy = training_correct / len(training_examples)
    testing_accuracy = testing_correct / len(testing_examples)
    nodes, leaves, max_depth = tree_statistics(root)
    training_confusion = _render_confusion_matrix(labels, training_counts)
    testing_confusion = _render_confusion_matrix(labels, testing_counts)
    distinct_training = len({_example_key(example) for example in training_examples})
    distinct_testing = len({_example_key(example) for example in testing_examples})
    distinct_total = len({_example_key(example) for example in all_examples})

    tree_text = "\n".join(render_tree(root))
    features = ", ".join(f"`{name}`" for name in feature_names)
    return "\n".join(
        [
            "# Decision Tree Result",
            "",
            "## Data and preprocessing",
            "",
            f"- Source: `data/{DATA_PATH.name}`",
            f"- Total rows: {len(all_examples)} ({distinct_total} distinct labeled records)",
            f"- Training set: {len(training_examples)} rows (75%); {distinct_training} distinct records",
            f"- Testing set: {len(testing_examples)} rows (25%); {distinct_testing} distinct records",
            f"- Training class counts: {_format_class_counts(training_examples)}",
            f"- Testing class counts: {_format_class_counts(testing_examples)}",
            f"- Split: stratified random split with seed `{RANDOM_SEED}`",
            "- Duplicate records were kept in the same partition to prevent train/test leakage.",
            f"- Target: `{TARGET_COLUMN}`",
            "- Excluded inputs: `Student_ID` (identifier), `Final_Exam_Score`",
            f"- Features ({len(feature_names)}): {features}",
            "- Numeric CSV values were converted to `int`/`float`; categorical values remain strings.",
            "",
            "## Model summary",
            "",
            "- Trainer: custom `CreateAttributeClassificationTrainingStrategy`",
            "- Split objective: weighted Gini impurity",
            f"- Pre-pruning: maximum depth `{MAX_DEPTH}`",
            "- Early stopping: make a leaf when all local labels are identical",
            f"- Nodes: {nodes}",
            f"- Leaves: {leaves}",
            f"- Learned maximum depth: {max_depth}",
            f"- Training accuracy: {training_correct}/{len(training_examples)} ({training_accuracy:.2%})",
            f"- Testing accuracy: {testing_correct}/{len(testing_examples)} ({testing_accuracy:.2%})",
            "",
            "## Confusion matrix (training data)",
            "",
            *training_confusion,
            "",
            "## Confusion matrix (testing data)",
            "",
            *testing_confusion,
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
    training_examples, testing_examples = split_data(examples)
    tree = train(training_examples)
    RESULT_PATH.write_text(
        build_result(tree, training_examples, testing_examples, feature_names),
        encoding="utf-8",
    )
    print(
        f"Trained on {len(training_examples)} rows, "
        f"tested on {len(testing_examples)} rows, and wrote {RESULT_PATH}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
