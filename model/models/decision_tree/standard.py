from typing import TypeVar, Callable, Optional, Sequence, Tuple, List
from .objective import (
    FunctionObjectiveBuilder,
    WeightedImpuritySplitObjective,
    SummedImpuritySplitObjective,
    Gini,
    SSE
)
from .optimizer import (
    BestSplitOptimizer,
    MinimizeEvaluationComparator,
    AttributeSplitCandidateGenerator,
    ScalarThresholdSplitCandidateGenerator
)
from .training_strategy import (
    RecursiveGreedyDecisionTreeTrainingStrategy,
    InputSplitPartitioner,
    SupervisedMajorityLeafBuilder,
    SupervisedMeanLeafBuilder,
    AnyStoppingCriterion,
    MaxDepthStoppingCriterion,
    MinDataStoppingCriterion
)

__all__ = [
    'CreateAttributeClassificationTrainingStrategy',
    'CreateAttributeRegressionTrainingStrategy',
    'CreateScalarClassificationTrainingStrategy',
    'CreateScalarRegressionTrainingStrategy'
]

DataT = TypeVar('DataT')
InputT = TypeVar('InputT')
OutputT = TypeVar('OutputT')
AttributeNameT = TypeVar('AttributeNameT')
AttributeValueT = TypeVar('AttributeValueT')


def _BuildStoppingCriterion(max_depth: Optional[int], min_data: Optional[int]):
    criteria = []

    if max_depth is not None:
        criteria.append(MaxDepthStoppingCriterion(max_depth))

    if min_data is not None:
        criteria.append(MinDataStoppingCriterion(min_data))

    return None if len(criteria) == 0 else AnyStoppingCriterion(criteria)


def CreateAttributeClassificationTrainingStrategy(
    data: Sequence[DataT],
    input_getter: Callable[[DataT], List[Tuple[AttributeNameT, AttributeValueT]]],
    output_getter: Callable[[DataT], OutputT],
    impurity: Callable[[Sequence[OutputT]], float] = Gini,
    continuous: Optional[Callable[[AttributeNameT, Sequence[AttributeValueT]], bool]] = None,
    max_depth: Optional[int] = None,
    min_data: Optional[int] = None
):
    generator = AttributeSplitCandidateGenerator(lambda state: state.Data, input_getter, continuous)
    optimizer = BestSplitOptimizer(generator, MinimizeEvaluationComparator())

    objective_builder = FunctionObjectiveBuilder(
        lambda state: WeightedImpuritySplitObjective(
            state.Data,
            lambda item: (input_getter(item), output_getter(item)),
            impurity
        )
    )

    return RecursiveGreedyDecisionTreeTrainingStrategy(
        data,
        optimizer,
        objective_builder,
        InputSplitPartitioner(input_getter),
        SupervisedMajorityLeafBuilder(output_getter),
        stopping_criterion=_BuildStoppingCriterion(max_depth, min_data)
    )


def CreateAttributeRegressionTrainingStrategy(
    data: Sequence[DataT],
    input_getter: Callable[[DataT], List[Tuple[AttributeNameT, AttributeValueT]]],
    output_getter: Callable[[DataT], float],
    continuous: Optional[Callable[[AttributeNameT, Sequence[AttributeValueT]], bool]] = None,
    max_depth: Optional[int] = None,
    min_data: Optional[int] = None
):
    generator = AttributeSplitCandidateGenerator(lambda state: state.Data, input_getter, continuous)
    optimizer = BestSplitOptimizer(generator, MinimizeEvaluationComparator())
    objective_builder = FunctionObjectiveBuilder(
        lambda state: SummedImpuritySplitObjective(
            state.Data,
            lambda item: (input_getter(item), output_getter(item)),
            SSE
        )
    )

    return RecursiveGreedyDecisionTreeTrainingStrategy(
        data,
        optimizer,
        objective_builder,
        InputSplitPartitioner(input_getter),
        SupervisedMeanLeafBuilder(output_getter),
        stopping_criterion=_BuildStoppingCriterion(max_depth, min_data)
    )


def CreateScalarClassificationTrainingStrategy(
    data: Sequence[DataT],
    input_getter: Callable[[DataT], float],
    output_getter: Callable[[DataT], OutputT],
    impurity: Callable[[Sequence[OutputT]], float] = Gini,
    max_depth: Optional[int] = None,
    min_data: Optional[int] = None
):
    generator = ScalarThresholdSplitCandidateGenerator(lambda state: state.Data, input_getter)
    optimizer = BestSplitOptimizer(generator, MinimizeEvaluationComparator())
    objective_builder = FunctionObjectiveBuilder(
        lambda state: WeightedImpuritySplitObjective(
            state.Data,
            lambda item: (input_getter(item), output_getter(item)),
            impurity
        )
    )

    return RecursiveGreedyDecisionTreeTrainingStrategy(
        data,
        optimizer,
        objective_builder,
        InputSplitPartitioner(input_getter),
        SupervisedMajorityLeafBuilder(output_getter),
        stopping_criterion=_BuildStoppingCriterion(max_depth, min_data)
    )


def CreateScalarRegressionTrainingStrategy(
    data: Sequence[DataT],
    input_getter: Callable[[DataT], float],
    output_getter: Callable[[DataT], float],
    max_depth: Optional[int] = None,
    min_data: Optional[int] = None
):
    generator = ScalarThresholdSplitCandidateGenerator(lambda state: state.Data, input_getter)
    optimizer = BestSplitOptimizer(generator, MinimizeEvaluationComparator())
    objective_builder = FunctionObjectiveBuilder(
        lambda state: SummedImpuritySplitObjective(
            state.Data,
            lambda item: (input_getter(item), output_getter(item)),
            SSE
        )
    )

    return RecursiveGreedyDecisionTreeTrainingStrategy(
        data,
        optimizer,
        objective_builder,
        InputSplitPartitioner(input_getter),
        SupervisedMeanLeafBuilder(output_getter),
        stopping_criterion=_BuildStoppingCriterion(max_depth, min_data)
    )
