# Decision Tree Model Library: Technical Report

## 1. Purpose and scope

This document is the technical reference for the decision-tree implementation in this repository. It describes the reusable model library, the student-data experiment built on top of it, the complete training and inference paths, the supported split objectives, extension points, runtime behavior, failure modes, complexity, and current limitations.

The implementation is an educational, dependency-free Python library. It supports:

- classification and regression;
- a single scalar input or an ordered collection of named attributes;
- numeric threshold splits and categorical multiway splits;
- Gini impurity, entropy, classification error, and sum of squared errors (SSE);
- configurable greedy split search;
- maximum-depth and minimum-data pre-pruning;
- custom objectives, split generators, comparators, leaf builders, partitioners, mappings, and forward strategies.

The API is intentionally component-oriented. A `DecisionTree` does not train itself. A training strategy owns the training data and constructs nodes, then installs the resulting root with `DecisionTree.SetRoot`. Prediction is performed with `DecisionTree.Execute`.

## 2. Runtime and repository layout

The library uses only the Python standard library. There is no `pyproject.toml`, `setup.py`, or dependency manifest, so it is intended to be run directly from the repository root.

Python 3.13 or newer is required by the source as written. In particular, [`model/data/attributes.py`](../model/data/attributes.py) uses default values for `typing.TypeVar`, a feature added to the standard library in Python 3.13. The repository has been verified locally with Python 3.14.

| Path | Responsibility |
| --- | --- |
| [`model/model.py`](../model/model.py) | Generic model interface. |
| [`model/data/`](../model/data/) | Generic data, supervised-data, and named-attribute abstractions. |
| [`model/train/`](../model/train/) | Generic objective, optimizer, and training-strategy interfaces. |
| [`model/models/decision_tree/`](../model/models/decision_tree/) | Decision-tree nodes, splits, mappings, objectives, optimizer, trainer, and standard factories. |
| [`data/loader.py`](../data/loader.py) | Validation and conversion of the project CSV into model inputs. |
| [`src/utils.py`](../src/utils.py) | Reproducible split, project-specific training, evaluation, tree rendering, and report generation. |
| [`src/pure.py`](../src/pure.py) | Fully grown Gini experiment. |
| [`src/depth.py`](../src/depth.py) | Depth-limited Gini experiment. |
| [`src/depth_cri.py`](../src/depth_cri.py) | Depth-limited entropy experiment. |
| [`docs/RESULT_*.md`](.) | Generated experiment outputs and comparisons. |

Package `__init__.py` files expose only a limited set of names. Importing concrete symbols from their defining modules, as the examples in this report do, is the most reliable usage pattern.

## 3. Architectural overview

The implementation separates what a tree is from how a tree is trained:

```text
raw records
    |
    v
input_getter / output_getter
    |
    v
DecisionTreeNodeTrainingState(Data, Depth)
    |
    +--> stopping criterion -----------> leaf builder --> ValueNode
    |
    +--> candidate generator
             |
             v
        split candidates
             |
             v
        objective + comparator
             |
             v
          best split
             |
             v
          partitioner
             |
             v
      recursively built children
             |
             v
 SplitDistributor(split, branch mapping)
             |
             v
    DistributorBranchNode
```

At inference time, the direction is much shorter:

```text
DecisionTree.Execute(input)
    -> forward strategy
    -> root.Execute(input)
    -> split computes a branch key
    -> branch mapping selects a child
    -> repeat until ValueNode
    -> return leaf output
```

This design uses several interchangeable abstractions:

- **Strategy:** training and forward behavior can be replaced without changing `DecisionTree`.
- **Builder:** objectives, leaves, and branch mappings are constructed behind interfaces.
- **Adapter:** function-backed classes turn ordinary callables into objectives, splits, criteria, extractors, and builders.
- **Composite:** `AnyStoppingCriterion` combines multiple stopping rules.

## 4. Data model

### 4.1. Generic data interfaces

[`model/data/data.py`](../model/data/data.py) defines the most general wrappers:

| Type | Behavior |
| --- | --- |
| `IData[DataT]` | Abstract interface with `GetData()`. |
| `ValueData[DataT]` | Dataclass that stores a value in `Data` and returns it from `GetData()`. |
| `TupleData[*DataTTuple]` | Tuple-valued `ValueData` with `GetSize()` and bounds-safe `GetAt()`. Out-of-range access returns `None`. |

These classes are infrastructure; the student experiment uses `ValueSupervisedData` instead.

### 4.2. Supervised data

[`model/data/supervised.py`](../model/data/supervised.py) separates an example into input and output:

- `ISupervisedData[InputT, OutputT]` defines `GetInput()` and `GetOutput()`.
- `ValueSupervisedData` is the concrete dataclass used by the project. It stores `Input` and `Output` directly.
- `ISupervisedDataExtractor` extracts an `(input, output)` tuple from an `IData` object.
- `ISupervisedDataBuilder` constructs a supervised object from such a tuple.
- `ExtractBuildSupervisedDataParser` composes an extractor and builder.
- `FunctionSupervisedDataExtractor`, `FunctionSupervisedDataBuilder`, and `FunctionSupervisedDataParser` adapt Python callables to those interfaces.

The tree factories do not require instances of these interfaces. They accept arbitrary record objects plus `input_getter` and `output_getter` callables. A record may therefore be a dataclass, tuple, dictionary, or domain object.

### 4.3. Named attributes

[`model/data/attributes.py`](../model/data/attributes.py) provides optional adapters for named attributes:

- `IAttributeData` presents data as a list of `(name, value)` pairs and supports lookup, removal, and conversion to supervised data.
- `IAttributeSupervisedData` presents named input attributes plus a separate output.
- `RemoveAtAttributeData` is a view that omits one attribute. It supports negative indexes and raises `IndexError` for invalid accesses through the view.
- `AttributeAtConvertedSupervisedData` selects one attribute as the output and exposes all other attributes as inputs.

The project loader does not use these adapters. It directly builds inputs with this runtime shape:

```python
list[tuple[str, str | int | float]]
```

Attribute order is preserved. Duplicate names are not rejected; split lookup uses the first matching pair. For predictable behavior, every record should contain each feature name exactly once and use the same schema.

## 5. Public usage

### 5.1. Run the repository experiments

From the repository root:

```powershell
python -m src.pure
python -m src.depth
python -m src.depth_cri
```

Each command loads `data/student_data.csv`, creates the same deterministic train/test split, trains one tree, evaluates it, and rewrites its corresponding report in `docs/`.

For the project dataset, the shortest reusable entry point is `src.utils.train_tree`:

```python
from data.loader import load_data
from model.models.decision_tree.objective import Gini
from src.utils import DATA_PATH, split_data, train_tree

examples, feature_names = load_data(DATA_PATH)
training, testing = split_data(examples)

tree = train_tree(training, impurity=Gini, max_depth=4)
prediction = tree.Execute(testing[0].GetInput())
print(prediction)
```

`train_tree` is project-specific: it creates an attribute-classification strategy and adds a pure-label stopping criterion.

### 5.2. Use the library factory directly

The reusable API accepts any record type:

```python
from model.models.decision_tree.standard import (
    CreateAttributeClassificationTrainingStrategy,
)
from model.models.decision_tree.tree import DecisionTree

records = [
    ([('hours', 10), ('access', 'No')], 'Fail'),
    ([('hours', 18), ('access', 'Yes')], 'Fail'),
    ([('hours', 30), ('access', 'No')], 'Pass'),
    ([('hours', 36), ('access', 'Yes')], 'Pass'),
]

tree = DecisionTree()
strategy = CreateAttributeClassificationTrainingStrategy(
    records,
    input_getter=lambda row: row[0],
    output_getter=lambda row: row[1],
    max_depth=3,
)
strategy.Train(tree)

result = tree.Execute([('hours', 32), ('access', 'Yes')])
```

The standard factory does **not** add a pure-label stopping rule. Without `max_depth` or `min_data`, it can continue splitting a pure node until no valid candidate remains. This does not change a pure node's predicted class, but it can create an unnecessarily large tree. To stop pure nodes explicitly:

```python
from model.models.decision_tree.training_strategy import (
    AnyStoppingCriterion,
    FunctionStoppingCriterion,
)

pure = FunctionStoppingCriterion(
    lambda state: len({row[1] for row in state.Data}) == 1
)

if strategy.StoppingCriterion is None:
    strategy.StoppingCriterion = pure
else:
    strategy.StoppingCriterion = AnyStoppingCriterion(
        (strategy.StoppingCriterion, pure)
    )
```

For unhashable output values, use an equality-based purity check rather than a `set`.

### 5.3. Regression example

```python
from model.models.decision_tree.standard import (
    CreateScalarRegressionTrainingStrategy,
)
from model.models.decision_tree.tree import DecisionTree

samples = [
    (0.0, 0.0),
    (1.0, 1.0),
    (2.0, 4.0),
    (3.0, 9.0),
]

tree = DecisionTree()
strategy = CreateScalarRegressionTrainingStrategy(
    samples,
    input_getter=lambda row: row[0],
    output_getter=lambda row: row[1],
    max_depth=2,
)
strategy.Train(tree)

prediction = tree.Execute(2.5)
```

Regression leaves return the arithmetic mean of the local target values.

### 5.4. Standard factory matrix

[`model/models/decision_tree/standard.py`](../model/models/decision_tree/standard.py) exposes four convenience factories:

| Factory | Input | Leaf output | Split score | Candidate generator |
| --- | --- | --- | --- | --- |
| `CreateAttributeClassificationTrainingStrategy` | Named `(attribute, value)` pairs | Majority class | Weighted impurity; Gini by default | Attribute numeric thresholds or categorical multiway split |
| `CreateAttributeRegressionTrainingStrategy` | Named `(attribute, value)` pairs | Mean target | Sum of child SSE | Attribute numeric thresholds or categorical multiway split |
| `CreateScalarClassificationTrainingStrategy` | One numeric scalar | Majority class | Weighted impurity; Gini by default | Scalar thresholds |
| `CreateScalarRegressionTrainingStrategy` | One numeric scalar | Mean target | Sum of child SSE | Scalar thresholds |

All four accept optional `max_depth` and `min_data`. Attribute factories also accept `continuous`, a callback that overrides automatic numeric/categorical detection. Classification factories accept a custom impurity function.

## 6. Tree representation

### 6.1. Model interface

[`model/model.py`](../model/model.py) defines `IModel[InputT, OutputT]`, whose only operation is:

```python
Execute(x: InputT) -> OutputT
```

The library consistently uses PascalCase method names such as `Execute`, `Train`, `Evaluate`, `Optimize`, and `Split`.

### 6.2. Nodes and tree container

[`model/models/decision_tree/tree.py`](../model/models/decision_tree/tree.py) defines:

| Type | Purpose |
| --- | --- |
| `INode` | A model that can occupy a tree position. |
| `IBranchNode` | A node with a distributor. Its default `Execute` selects a child and invokes that child with the original input. |
| `ValueNode` | A leaf that always returns its stored `Output`. |
| `FunctionNode` | A leaf or custom node backed by an arbitrary callable. |
| `DistributorBranchNode` | Concrete branch node holding an `IDistributor`. |
| `DecisionTree` | Holds an optional root and a forward strategy. |

A newly constructed `DecisionTree()` has no root. Calling `Execute` before training or `SetRoot` raises `RuntimeError`. `SetRoot(None)` is permitted and returns the tree to that untrained state.

The default `StandardDecisionTreeForwardStrategy` calls `root.Execute(x)`. `FunctionDecisionTreeForwardStrategy` can replace that behavior, for example to instrument or wrap prediction.

### 6.3. Splits

[`model/models/decision_tree/split.py`](../model/models/decision_tree/split.py) defines how an input becomes a branch key:

| Split | Branch result |
| --- | --- |
| `FunctionSplit` | Result of an arbitrary callable. |
| `PredicateSplit` | Semantic alias for a Boolean `FunctionSplit`. |
| `ValueThresholdSplit(threshold)` | `True` when `x <= threshold`, otherwise `False`. |
| `AttributeValueSplit(name)` | Raw value of the named attribute; produces a multiway categorical split. |
| `AttributePredicateSplit(name, predicate)` | Result of applying a predicate to the named value. |
| `AttributeThresholdSplit(name, threshold)` | `True` when the named value is `<= threshold`, otherwise `False`. |

Attribute splits linearly scan the input pairs and use the first matching name. A missing name raises `KeyError`.

### 6.4. Branch mappings and distribution

A split only returns a branch key. [`model/models/decision_tree/distribution.py`](../model/models/decision_tree/distribution.py) and [`model/models/decision_tree/mapping.py`](../model/models/decision_tree/mapping.py) translate that key to a child:

```text
input -> ISplit.Split(input) -> branch key
      -> IBranchMapping.Map(key) -> child node
```

`SplitDistributor` composes an `ISplit` and an `IBranchMapping`. `FunctionDistributor` supports arbitrary routing.

The mapping implementations are:

- `ListBranchMapping`: ordered equality-based lookup; rejects duplicate equal keys and raises `KeyError` for an unknown key.
- `DictionaryBranchMapping`: dictionary lookup; branch keys must be hashable.
- `FunctionBranchMapping`: arbitrary callable lookup.
- `ListBranchMappingBuilder` and `FunctionBranchMappingBuilder`: construct mappings while the tree is being trained.

The standard trainer uses `ListBranchMapping`. This preserves deterministic branch order and permits equality-comparable, unhashable categorical values.

## 7. How the tree is built

Training is implemented by `RecursiveGreedyDecisionTreeTrainingStrategy` in [`training_strategy.py`](../model/models/decision_tree/training_strategy.py). The strategy copies the top-level training sequence to a tuple when constructed. `Train(tree)` rejects an empty dataset and builds a new root recursively.

For a node with local dataset `D` and root-based depth `d`, the exact algorithm is:

```text
BuildNode(D, d):
    if a configured stopping criterion says stop:
        return LeafBuilder.Build(D)

    objective = ObjectiveBuilder.Build(state(D, d))

    try:
        split = Optimizer.Optimize(state(D, d), objective)
    except NoSplitCandidateError:
        return LeafBuilder.Build(D)

    partitions = Partitioner.Partition(D, split)
    discard empty partitions

    if fewer than two non-empty partitions remain:
        return LeafBuilder.Build(D)

    for each (branch, child_data), in partition encounter order:
        child = BuildNode(child_data, d + 1)

    mapping = MappingBuilder.Build((branch, child) pairs)
    return DistributorBranchNode(SplitDistributor(split, mapping))
```

This is a **top-down, recursive, locally greedy** algorithm:

- top-down: construction begins at the root;
- recursive: the same process is applied independently to each partition;
- locally greedy: each node chooses its best immediate split without backtracking or optimizing the final whole-tree score.

The trained node graph stores splits, mappings, and leaf values. It does not retain node-level training examples. The training strategy itself does retain its original `Data` tuple.

## 8. Candidate split generation

### 8.1. Scalar numeric input

`ScalarThresholdSplitCandidateGenerator` obtains all local scalar input values, removes duplicates, and sorts them. For adjacent unique values

```text
v[0] < v[1] < ... < v[u - 1]
```

it generates `u - 1` thresholds:

```text
t[i] = (v[i] + v[i + 1]) / 2
```

Each threshold creates the binary branches `x <= t[i]` and `x > t[i]`. Zero or one unique value produces no candidate.

### 8.2. Named attributes

`AttributeSplitCandidateGenerator` first takes candidate attribute names from the first record at the current node, preserving their order and removing equal duplicate names. An attribute is skipped if any local record lacks it. Attributes that appear only in later records are ignored.

For each usable attribute:

1. Collect the first matching value from every local record.
2. Decide whether the attribute is continuous.
3. Generate numeric midpoint thresholds or one categorical value split.

By default, an attribute is continuous only when it has at least one value and every value is an `int` or `float`, excluding `bool`. A caller-supplied `continuous(name, values)` callback completely replaces that decision.

Continuous values are converted to `float`, deduplicated, and sorted before midpoint generation. The resulting `AttributeThresholdSplit` still compares the original inference value to the floating-point threshold.

A categorical feature produces exactly one `AttributeValueSplit`. That split creates one branch for every distinct value observed in the local training partition. It does not search binary subsets of category values.

### 8.3. Candidate order and deterministic ties

Candidate order is deterministic for a fixed data sequence:

- named attributes follow their order in the first local record;
- numeric thresholds are ascending;
- a categorical feature contributes one candidate at its position in feature order.

`BestSplitOptimizer` replaces the current best candidate only when the comparator reports a strict improvement. `MinimizeEvaluationComparator` uses `<`; therefore, equal-scoring candidates keep the first generated split. Changing feature order can consequently change a tree when scores tie.

## 9. Split objectives

Objective functions are implemented in [`model/models/decision_tree/objective.py`](../model/models/decision_tree/objective.py). They receive raw output values, not a precomputed frequency array.

### 9.1. Classification impurity

For a local output sequence `Y` of size `n`, let `p_k` be the fraction belonging to class `k`.

Entropy:

```text
H(Y) = - sum_k p_k log2(p_k)
```

Gini impurity:

```text
Gini(Y) = 1 - sum_k p_k^2
```

Classification error:

```text
Error(Y) = 1 - max_k p_k
```

All three return `0.0` for an empty sequence. Class counting uses equality comparisons rather than hashing, so labels do not have to be hashable.

For a candidate split with non-empty output groups `Y_b`, `WeightedImpuritySplitObjective` computes:

```text
Score(split) = sum_b (|Y_b| / |Y|) * Impurity(Y_b)
```

The standard classification strategy minimizes this value. This is equivalent to maximizing impurity reduction at the current node because the parent impurity is constant across all candidate splits. The implementation evaluates the weighted child impurity directly; it does not explicitly calculate information gain.

### 9.2. Regression impurity

For numeric outputs with mean `y_bar`, `SSE` computes:

```text
SSE(Y) = sum_i (y_i - y_bar)^2
```

`SummedImpuritySplitObjective` computes the unweighted sum of each child's SSE:

```text
Score(split) = sum_b SSE(Y_b)
```

The standard regression strategy minimizes that sum. Since SSE already scales with group size, no additional child-size weight is applied.

### 9.3. Generic objective infrastructure

The generic training layer in [`model/train/objective.py`](../model/train/objective.py) defines:

- `IObjective`, with `Evaluate(output)`;
- `FunctionObjective`, backed by a callable;
- `IDataObjective`, for an objective that exposes data;
- `IValueDataObjective` and `FunctionValueDataObjective`, which store data directly.

The decision-tree layer adds `IObjectiveBuilder`, `FunctionObjectiveBuilder`, `ISplitObjective`, and `SupervisedSplitObjective`. The builder creates a node-local objective bound to that node's data.

[`model/utils.py`](../model/utils.py) contains a separate legacy `ObjectiveFunction` whose methods consume frequency counts. The active decision-tree factories do not use it. New code should use the raw-label functions in `model.models.decision_tree.objective`, which also define safe empty-input behavior.

## 10. Split optimization and partitioning

[`model/models/decision_tree/optimizer.py`](../model/models/decision_tree/optimizer.py) separates candidate generation from comparison:

- `ISplitCandidateGenerator.Generate(state)` yields candidates lazily.
- `BestSplitOptimizer` evaluates every yielded candidate exactly once.
- `MinimizeEvaluationComparator` chooses lower scores.
- `MaximizeEvaluationComparator` chooses higher scores.
- `FunctionEvaluationComparator` supports custom ordering.
- `NoSplitCandidateError` signals that the generator yielded nothing.

The standard factories always use minimization. There is no minimum-gain check: if candidates exist, the optimizer selects the best one even when it does not improve on the unsplit node. The trainer's protection against non-progress is structural: a split that yields fewer than two non-empty partitions becomes a leaf.

After selection, `InputSplitPartitioner` applies the split to every local record's input. Branch groups use equality comparison and retain:

- records in their original local order;
- branches in first-observed order.

Each child receives a tuple containing only its partition and a depth incremented by one.

## 11. Stopping rules and leaf construction

Stopping rules are evaluated before candidate generation.

| Criterion | Stops when | Detail |
| --- | --- | --- |
| `MaxDepthStoppingCriterion(max_depth)` | `state.Depth >= max_depth` | Root depth is `0`; `max_depth=0` produces one root leaf. Negative limits are rejected. |
| `MinDataStoppingCriterion(min_data)` | `len(state.Data) <= min_data` | This is inclusive. Values below `1` are rejected. |
| `FunctionStoppingCriterion(function)` | Callable returns truthy | Supports custom logic such as purity or impurity thresholds. |
| `AnyStoppingCriterion(criteria)` | Any child criterion stops | Logical OR composition. An empty collection never stops. |

The standard factories combine configured `max_depth` and `min_data` using `AnyStoppingCriterion`. If neither is supplied, `StoppingCriterion` is `None`.

There are two unconditional fallback cases:

- the candidate generator produces no split;
- the selected split produces fewer than two non-empty partitions.

Leaf behavior depends on task type:

- `SupervisedMajorityLeafBuilder` returns the most frequent class;
- `SupervisedMeanLeafBuilder` returns the arithmetic mean target;
- `FunctionLeafBuilder` permits arbitrary leaf nodes or outputs.

A classification frequency tie is resolved by first occurrence in the local data because the majority builder updates its winner only for a strictly larger count. Both standard leaf builders reject empty data.

## 12. Prediction semantics

Prediction starts at the root and repeatedly performs the following operations:

1. The current branch node's split reads the input and returns a branch key.
2. Its mapping finds the child associated with that key.
3. The child receives the original, unchanged input.
4. A `ValueNode` returns its constant output.

Numeric branches use `<=` for `True` and `>` for `False`. Categorical branches use the raw category value as the key.

The library has no fallback branch. Consequently:

- a missing named attribute raises `KeyError` in the split;
- an unseen categorical value raises `KeyError` in the branch mapping;
- incompatible comparison types propagate `TypeError`;
- a malformed custom split or mapping propagates its own exception.

There is no batch-prediction method. Call `Execute` once per input or wrap it in a comprehension.

## 13. Student-data pipeline

### 13.1. CSV loading

[`data/loader.py`](../data/loader.py) loads `data/student_data.csv` with `csv.DictReader` and applies these rules:

- require a header;
- require `Student_ID` and target `Pass_Fail`;
- exclude `Student_ID` and `Final_Exam_Score` from model features;
- parse `Study_Hours_per_Week` and `Past_Exam_Scores` as `int`;
- parse `Attendance_Rate` as `float`;
- keep all other feature values as stripped strings;
- reject missing or empty features and target values with a line-numbered `ValueError`;
- reject a dataset with no usable features or no rows.

The loader returns `(examples, feature_names)`. Each example is a `ValueSupervisedData` whose input is a list of named pairs and whose output is the `Pass_Fail` string.

The active seven features are:

1. `Gender`
2. `Study_Hours_per_Week`
3. `Attendance_Rate`
4. `Past_Exam_Scores`
5. `Parental_Education_Level`
6. `Internet_Access_at_Home`
7. `Extracurricular_Activities`

No normalization or one-hot encoding is performed. Numeric values are handled by thresholds and strings by categorical branches.

### 13.2. Reproducible train/test split

`src.utils.split_data` defaults to a 75/25 split with seed `42`. Its unit of allocation is a **distinct labeled record**, not a CSV row:

1. Build a key from the complete ordered feature list plus label.
2. Group identical labeled examples.
3. Group those duplicate groups by class label.
4. Allocate exactly `int(distinct_group_count * training_fraction)` groups to training while approximating class proportions with largest-remainder allocation.
5. Shuffle groups within each label with a local `random.Random(seed)`.
6. Keep every copy of one distinct record on the same side.
7. Shuffle the final training and testing row lists.

This prevents duplicate-row leakage. For the checked-in dataset it yields 531 training rows and 177 testing rows, containing 375 and 125 distinct labeled records respectively. With other duplicate-group sizes, the requested fraction is exact for distinct groups but not necessarily exact for physical rows.

The function rejects fractions outside the open interval `(0, 1)`, fewer than two distinct records, and allocations that would leave one partition empty.

### 13.3. Project training wrapper

`src.utils.train_tree` wires:

- `CreateAttributeClassificationTrainingStrategy`;
- the selected classification impurity;
- the selected maximum depth;
- a pure-label `FunctionStoppingCriterion`;
- `AnyStoppingCriterion` when both depth and purity rules are present.

This wrapper is why the generated experiment reports correctly describe natural stopping on pure nodes. That behavior belongs to the project wrapper, not the standard library factory by itself.

### 13.4. Evaluation and reporting

`src.utils.evaluate` calls `Execute` for every example and returns:

- total count;
- correct count;
- derived incorrect count;
- accuracy;
- error rate;
- a `Counter[(actual, predicted)]` confusion matrix.

The report utilities inspect the concrete node graph to render splits and compute total nodes, leaf count, and maximum root-based depth. They recognize `ValueNode` and `DistributorBranchNode`; a custom node is counted but cannot be structurally expanded by those utilities.

The current deterministic experiment results are:

| Configuration | Nodes | Leaves | Depth | Train accuracy | Test accuracy |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fully grown, Gini | 171 | 93 | 10 | 100.00% | 67.80% |
| `max_depth=4`, Gini | 35 | 19 | 4 | 85.50% | 76.84% |
| `max_depth=4`, Entropy | 29 | 17 | 4 | 84.18% | 75.14% |

These results are experiment outputs, not guarantees of the general-purpose library.

## 14. Extension points

The component boundaries permit several kinds of customization.

### 14.1. Custom stopping policy

```python
from model.models.decision_tree.training_strategy import (
    FunctionStoppingCriterion,
)

strategy.StoppingCriterion = FunctionStoppingCriterion(
    lambda state: state.Depth >= 5 or len(state.Data) <= 10
)
```

### 14.2. Custom impurity

Classification factories accept `Callable[[Sequence[OutputT]], float]`:

```python
def misclassification_rate(values):
    if not values:
        return 0.0
    best = max(values.count(value) for value in values)
    return 1.0 - best / len(values)
```

For nontrivial custom criteria, implement `IObjective` and, when it depends on local data, provide an `IObjectiveBuilder`.

### 14.3. Custom candidate search

Use `FunctionSplitCandidateGenerator` for state-dependent generation or `SequenceSplitCandidateGenerator` for a fixed candidate collection. Combine it with `BestSplitOptimizer` and either a built-in or custom comparator.

### 14.4. Custom node behavior

- `FunctionNode` can calculate an output instead of returning a constant.
- `FunctionSplit` can produce arbitrary branch keys.
- `FunctionBranchMapping` and `FunctionDistributor` can implement fallback or probabilistic routing.
- `FunctionDecisionTreeForwardStrategy` can wrap root execution.
- `FunctionLeafBuilder`, `FunctionSplitPartitioner`, and `FunctionBranchMappingBuilder` allow custom training output without subclassing every interface.

### 14.5. Fully custom training composition

Construct `RecursiveGreedyDecisionTreeTrainingStrategy` directly when the four standard factories do not fit. It requires:

1. a training sequence;
2. a split optimizer;
3. a node-local objective builder;
4. a partitioner;
5. a leaf builder;

and optionally a mapping builder and stopping criterion. All supplied components are validated against `None` at construction time.

## 15. Validation, errors, and invariants

The library relies on runtime checks rather than a separate validation pass.

| Condition | Result |
| --- | --- |
| Train with `model is None` | `ValueError` |
| Train with empty data | `ValueError` |
| Predict with no root | `RuntimeError` |
| Candidate generator yields nothing | `NoSplitCandidateError`, caught by the recursive trainer and converted to a leaf |
| Selected split creates fewer than two non-empty groups | Converted to a leaf |
| Missing input attribute during prediction | `KeyError` |
| Unseen categorical branch during prediction | `KeyError` |
| Duplicate branch keys in `ListBranchMapping` | `ValueError` |
| Negative `max_depth` | `ValueError` |
| `min_data < 1` | `ValueError` |
| Empty data passed to majority/mean leaf builder | `ValueError` |
| Required collaborator or callable is `None` | Usually `ValueError` at construction |

Type hints describe expected composition but are not enforced at runtime. Callers are responsible for ensuring that getters, splits, objectives, partitioners, mappings, nodes, and tree input types agree.

## 16. Determinism

Training is deterministic when all of the following are deterministic:

- input record order;
- feature order within the first record at each node;
- getters and custom callbacks;
- equality and ordering behavior of values;
- custom candidate generation and objective evaluation.

There is no random feature selection or random threshold selection in the model library. Randomness in the project enters only through `split_data`, which uses a fixed local seed by default.

Important deterministic tie rules are:

- equal split scores keep the first candidate;
- equal majority-class counts keep the class first encountered in local data;
- partition order follows first branch occurrence;
- threshold display order in generated reports places the `True` (`<=`) branch first.

## 17. Complexity and storage

Let:

- `n` be the number of records at a node;
- `p` be the number of named attributes;
- `u_j` be the number of unique numeric values of attribute `j`;
- `B` be the number of branches produced by a candidate;
- `K` be the number of distinct output values;
- `h` be prediction depth.

At one attribute-based node:

- collecting values is proportional to scanning records and their attribute lists;
- numeric candidate preparation costs `O(n log n)` per numeric attribute because values are deduplicated and sorted;
- numeric attribute `j` generates `u_j - 1` candidates;
- a categorical attribute generates one candidate;
- every candidate rescans the local data to construct output groups.

Grouping and class counting use equality-based lists, not hash tables. Candidate evaluation is therefore approximately `O(n(B + K))` in terms of equality comparisons, and can become quadratic in `n` when branch or label cardinality is also proportional to `n`. For continuous data with many unique values, evaluating every midpoint can make a node expensive because there are `O(n)` candidates. This implementation favors clarity and generic equality semantics over the sorted incremental statistics used by production tree libraries.

For named-attribute inference, each level scans up to `p` input pairs to find the attribute and up to `B` mapping entries to locate the branch, giving approximately `O(h(p + B))`. Scalar threshold inference is `O(h)`.

The final model stores one split and branch mapping per internal node and one output per leaf. It does not store training rows in nodes. Training uses recursive call depth equal to tree depth and temporary local partitions/objectives; an extremely deep tree may reach Python's recursion limit.

## 18. Current limitations and operational cautions

The following behavior should be understood before using the library outside this lab:

1. **No automatic purity stop in standard factories.** Add one explicitly or use the project `train_tree` wrapper.
2. **No minimum improvement requirement.** A best available split may be selected even if its impurity is no better than the parent.
3. **No post-pruning.** Only pre-pruning through stopping criteria is built in.
4. **No missing-value policy.** Training may skip an attribute missing from any local row; prediction fails when a required attribute is absent.
5. **No unseen-category fallback.** A new categorical value raises `KeyError`.
6. **First-record schema discovery.** Attribute candidates come only from names in the first local record.
7. **Simple numeric detection.** Only built-in `int` and `float` values, excluding `bool`, are automatically continuous. `Decimal`, third-party numeric scalars, numeric strings, and custom numeric types need a `continuous` callback and compatible arithmetic/comparison behavior.
8. **Floating-point threshold conversion.** Attribute numeric candidates are converted to `float`, which may lose precision for very large integers or custom numeric values.
9. **No explicit NaN handling.** IEEE NaN comparisons generally route to the `False` threshold branch rather than being treated as missing.
10. **Multiway-only categorical search.** The generator does not search category subsets or order categories by target statistics.
11. **No sample weights.** Every row contributes equally; repeated rows effectively carry repeated weight.
12. **No class probabilities.** Classification leaves return only one majority label and do not retain distributions.
13. **No feature importance, calibration, confidence, or explanation API.** Tree inspection is performed by project-specific utilities.
14. **No serialization format.** Persisting trained trees is not part of the API.
15. **No batch or scikit-learn-style interface.** There is no `fit`, `predict`, `predict_proba`, parameter search, or cross-validation integration.
16. **No built-in tests in the repository.** Verification currently depends on compilation, smoke checks, and deterministic experiment reproduction.
17. **Recursive construction and inference.** Very deep trees can exceed Python's recursion limit.

These are not hidden behaviors: most can be addressed by supplying custom components through the existing interfaces. Production use would additionally require schema validation, robust missing/unseen routing, test coverage, serialization, optimized split scanning, and stable packaging.

## 19. Module and symbol reference

### 19.1. Generic training layer

| Module | Main symbols |
| --- | --- |
| [`model/train/training_strategy.py`](../model/train/training_strategy.py) | `ITrainingStrategy.Train(model)` |
| [`model/train/optimizer.py`](../model/train/optimizer.py) | `IOptimizer.Optimize(state, objective)` |
| [`model/train/objective.py`](../model/train/objective.py) | `IObjective`, `FunctionObjective`, `IDataObjective`, `IValueDataObjective`, `FunctionValueDataObjective` |

### 19.2. Decision-tree layer

| Module | Main symbols |
| --- | --- |
| [`tree.py`](../model/models/decision_tree/tree.py) | `DecisionTree`, `INode`, `IBranchNode`, `ValueNode`, `FunctionNode`, `DistributorBranchNode` |
| [`forward.py`](../model/models/decision_tree/forward.py) | `IDecisionTreeForwardStrategy`, `StandardDecisionTreeForwardStrategy`, `FunctionDecisionTreeForwardStrategy` |
| [`split.py`](../model/models/decision_tree/split.py) | `ISplit`, function/predicate, scalar threshold, attribute value/predicate/threshold splits |
| [`mapping.py`](../model/models/decision_tree/mapping.py) | Mapping interfaces, list/dictionary/function mappings, mapping builders |
| [`distribution.py`](../model/models/decision_tree/distribution.py) | `IDistributor`, `FunctionDistributor`, `SplitDistributor` |
| [`objective.py`](../model/models/decision_tree/objective.py) | Objective builders, split objectives, `Entropy`, `Gini`, `ClassificationError`, `SSE` |
| [`optimizer.py`](../model/models/decision_tree/optimizer.py) | Candidate generators, comparators, `BestSplitOptimizer`, `NoSplitCandidateError` |
| [`training_strategy.py`](../model/models/decision_tree/training_strategy.py) | Training state, criteria, leaf builders, partitioners, recursive trainer |
| [`standard.py`](../model/models/decision_tree/standard.py) | Four ready-made classification/regression factory functions |

## 20. Verification checklist

The following checks were run against the documented revision:

```powershell
python -m compileall -q model data src
```

The model, loader, and experiment modules compile successfully under Python 3.14. The loader and splitter reproduce 708 total rows, seven active features, 531 training rows, and 177 testing rows. Smoke checks exercised attribute classification and scalar regression. Independent in-memory reproduction matched the node counts, depths, and train/test accuracies shown in Section 13.4.

When implementation behavior changes, update this report together with the affected code and rerun all three experiment commands so the generated reports remain consistent.
