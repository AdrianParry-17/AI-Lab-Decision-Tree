"""Shared data, training, evaluation, and report utilities."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from random import Random
from typing import Callable, Sequence

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


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "data" / "student_data.csv"
DOCS_DIR = ROOT_DIR / "docs"

TRAINING_FRACTION = 3 / 4
RANDOM_SEED = 42

ImpurityFunction = Callable[[Sequence[str]], float]


@dataclass(frozen=True)
class ExperimentConfig:
    """The one controlled model configuration used by an experiment."""

    title: str
    method: str
    criterion_name: str
    impurity: ImpurityFunction
    max_depth: int | None


@dataclass(frozen=True)
class EvaluationMetrics:
    """Classification counts for one dataset partition."""

    total: int
    correct: int
    confusion: Counter[tuple[str, str]]

    @property
    def incorrect(self) -> int:
        return self.total - self.correct

    @property
    def accuracy(self) -> float:
        return self.correct / self.total

    @property
    def error_rate(self) -> float:
        return self.incorrect / self.total


@dataclass(frozen=True)
class ExperimentOutcome:
    """The metrics and tree shape produced by an experiment."""

    training: EvaluationMetrics
    testing: EvaluationMetrics
    nodes: int
    leaves: int
    maximum_depth: int


def _example_key(
    example: TrainingExample,
) -> tuple[tuple[tuple[str, FeatureValue], ...], str]:
    """Identify repeated labeled records without using them as features."""
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
    """Make a reproducible stratified split without duplicate-row leakage."""
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
        training.extend(
            example
            for group in groups[:split_index]
            for example in group
        )
        testing.extend(
            example
            for group in groups[split_index:]
            for example in group
        )

    random.shuffle(training)
    random.shuffle(testing)
    return training, testing


def train_tree(
    examples: Sequence[TrainingExample],
    impurity: ImpurityFunction,
    max_depth: int | None,
) -> DecisionTree[ModelInput, str]:
    """Train a classification tree with the requested controlled settings."""
    tree: DecisionTree[ModelInput, str] = DecisionTree()
    strategy = CreateAttributeClassificationTrainingStrategy(
        examples,
        input_getter=lambda example: example.GetInput(),
        output_getter=lambda example: example.GetOutput(),
        impurity=impurity,
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


def _ordered_children(
    items: Sequence[tuple[object, INode]],
) -> list[tuple[object, INode]]:
    """Put a threshold's <= branch first and keep output deterministic."""
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

    child_statistics = [
        tree_statistics(child, depth + 1)
        for _, child in node.GetDistributor().GetMapping().GetItems()
    ]
    return (
        1 + sum(nodes for nodes, _, _ in child_statistics),
        sum(leaves for _, leaves, _ in child_statistics),
        max(maximum_depth for _, _, maximum_depth in child_statistics),
    )


def evaluate(
    tree: DecisionTree[ModelInput, str],
    examples: Sequence[TrainingExample],
) -> EvaluationMetrics:
    """Evaluate a trained tree without changing it."""
    predictions = [tree.Execute(example.GetInput()) for example in examples]
    correct = sum(
        prediction == example.GetOutput()
        for example, prediction in zip(examples, predictions)
    )
    confusion = Counter(
        (example.GetOutput(), prediction)
        for example, prediction in zip(examples, predictions)
    )
    return EvaluationMetrics(len(examples), correct, confusion)


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
    config: ExperimentConfig,
    tree: DecisionTree[ModelInput, str],
    training_examples: Sequence[TrainingExample],
    testing_examples: Sequence[TrainingExample],
    feature_names: Sequence[str],
) -> tuple[str, ExperimentOutcome]:
    """Build one complete Markdown experiment result and its summary."""
    root = tree.GetRoot()
    if root is None:
        raise RuntimeError("Training completed without producing a root node")

    all_examples = [*training_examples, *testing_examples]
    labels = sorted({example.GetOutput() for example in all_examples})
    training_metrics = evaluate(tree, training_examples)
    testing_metrics = evaluate(tree, testing_examples)
    nodes, leaves, maximum_depth = tree_statistics(root)
    outcome = ExperimentOutcome(
        training_metrics,
        testing_metrics,
        nodes,
        leaves,
        maximum_depth,
    )

    training_confusion = _render_confusion_matrix(
        labels,
        training_metrics.confusion,
    )
    testing_confusion = _render_confusion_matrix(
        labels,
        testing_metrics.confusion,
    )
    distinct_training = len({_example_key(example) for example in training_examples})
    distinct_testing = len({_example_key(example) for example in testing_examples})
    distinct_total = len({_example_key(example) for example in all_examples})
    depth_limit = "None (fully grown)" if config.max_depth is None else str(config.max_depth)
    features = ", ".join(f"`{name}`" for name in feature_names)
    tree_text = "\n".join(render_tree(root))

    markdown = "\n".join(
        [
            f"# {config.title}",
            "",
            "## Method",
            "",
            config.method,
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
            "- Numeric fields were converted to `int`/`float`; categorical fields remain strings.",
            "",
            "## Model and tree shape",
            "",
            "- Trainer: custom `CreateAttributeClassificationTrainingStrategy`",
            f"- Splitting criterion: {config.criterion_name}",
            f"- Configured maximum depth: {depth_limit}",
            "- Natural stopping: make a leaf when all local labels are identical or no split is available",
            f"- Nodes: {nodes}",
            f"- Leaves: {leaves}",
            f"- Observed maximum depth: {maximum_depth}",
            "",
            "## Accuracy and error rate",
            "",
            "| Dataset | Correct | Incorrect | Accuracy | Error rate |",
            "| --- | ---: | ---: | ---: | ---: |",
            f"| Training | {training_metrics.correct}/{training_metrics.total} | {training_metrics.incorrect}/{training_metrics.total} | {training_metrics.accuracy:.2%} | {training_metrics.error_rate:.2%} |",
            f"| Testing | {testing_metrics.correct}/{testing_metrics.total} | {testing_metrics.incorrect}/{testing_metrics.total} | {testing_metrics.accuracy:.2%} | {testing_metrics.error_rate:.2%} |",
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
    return markdown, outcome


def run_experiment(
    config: ExperimentConfig,
    result_path: Path,
) -> ExperimentOutcome:
    """Load, split, train, evaluate, and write one experiment report."""
    examples, feature_names = load_data(DATA_PATH)
    training_examples, testing_examples = split_data(examples)
    tree = train_tree(
        training_examples,
        impurity=config.impurity,
        max_depth=config.max_depth,
    )
    markdown, outcome = build_result(
        config,
        tree,
        training_examples,
        testing_examples,
        feature_names,
    )
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(markdown, encoding="utf-8")
    return outcome
