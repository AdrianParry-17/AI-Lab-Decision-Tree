# Decision Tree Improvement Report

## Objective

This experiment evaluates two proposed improvements against a fully grown decision-tree baseline:

1. Pre-pruning the tree with a maximum depth of 4.
2. Changing the split criterion from Gini impurity to Entropy while keeping the depth limit fixed at 4.

The individual generated results, including confusion matrices and complete tree shapes, are available in [RESULT_PURE.md](RESULT_PURE.md), [RESULT_DEPTH.md](RESULT_DEPTH.md), and [RESULT_DEPTH_CRI.md](RESULT_DEPTH_CRI.md). The recommended tree is visualized in [tree_visualization.html](tree_visualization.html), and its independent interpretation is in [ANALYSIS_RESULTING_TREE.md](ANALYSIS_RESULTING_TREE.md).

## Experimental controls

All three models use the same preprocessing and the same reproducible data partition. This ensures that changes in the results come from the model settings rather than different samples.

- Training set: 531 rows (75%), containing 375 distinct records.
- Testing set: 177 rows (25%), containing 125 distinct records.
- Split method: stratified random split with seed 42.
- Class counts: training has 266 `Fail` and 265 `Pass`; testing has 88 `Fail` and 89 `Pass`.
- Duplicate oversampled records remain in one partition, so identical labeled records do not leak between training and testing.
- `Student_ID` is excluded because it is an identifier.
- `Final_Exam_Score` is excluded because it directly determines or strongly reveals `Pass_Fail` and would create target leakage.

Accuracy and error rate are calculated as:

```text
Accuracy   = correct predictions / total predictions
Error rate = incorrect predictions / total predictions = 1 - accuracy
```

## Overall comparison

| Model | Criterion | Depth limit | Nodes | Leaves | Observed depth | Training accuracy | Training error | Testing accuracy | Testing error |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Fully grown baseline | Gini | None | 171 | 93 | 10 | 100.00% | 0.00% | 67.80% | 32.20% |
| Depth-limited | Gini | 4 | 35 | 19 | 4 | 85.50% | 14.50% | **76.84%** | **23.16%** |
| Depth-limited + criterion change | Entropy | 4 | 29 | 17 | 4 | 84.18% | 15.82% | 75.14% | 24.86% |

The depth-limited Gini model is the best overall model because it has the highest testing accuracy and lowest testing error rate.

## Baseline: fully grown Gini tree

The baseline has no configured depth limit. It continues splitting until a node is pure or no candidate split remains.

- Training result: 531/531 correct, giving 100.00% accuracy and 0.00% error.
- Testing result: 120/177 correct, giving 67.80% accuracy and 32.20% error.
- Tree shape: 171 nodes, 93 leaves, and maximum depth 10.
- Generalization gap: 100.00% - 67.80% = 32.20 percentage points.

The perfect training result does not mean this is the best model. The large training/testing gap and much weaker testing result show that the fully grown tree memorizes small details and noise in the training partition. Its 171-node shape is also substantially harder to interpret. This is the overfitting baseline that the proposed methods attempt to improve.

## Improvement 1: limit maximum depth

### Method

The first improvement keeps weighted Gini impurity but applies `max_depth=4`. This is pre-pruning: once a node reaches depth 4, it becomes a majority-class leaf rather than generating more branches.

### Updated result

- Training result: 454/531 correct, giving 85.50% accuracy and 14.50% error.
- Testing result: 136/177 correct, giving 76.84% accuracy and 23.16% error.
- Tree shape: 35 nodes, 19 leaves, and maximum depth 4.
- Generalization gap: 85.50% - 76.84% = 8.66 percentage points.

Compared with the fully grown baseline, testing accuracy increases by 9.04 percentage points and testing error decreases by 9.04 points. The tree removes 136 nodes and 74 leaves, while the generalization gap falls from 32.20 to 8.66 points.

### Why it improves the model

The unrestricted tree creates highly specific branches that perfectly classify training examples but do not transfer well to unseen records. The depth cap prevents those low-level splits. Training accuracy decreases, which is expected, but testing accuracy increases because the smaller tree captures broader relationships instead of training noise. Therefore, limiting depth is a successful improvement for this dataset.

## Improvement 2: change Gini to Entropy

### Method

The second improvement retains `max_depth=4` and changes only the split objective from weighted Gini impurity to weighted Entropy. Because the data split and depth are unchanged, the result isolates the effect of the criterion.

### Updated result

- Training result: 447/531 correct, giving 84.18% accuracy and 15.82% error.
- Testing result: 133/177 correct, giving 75.14% accuracy and 24.86% error.
- Tree shape: 29 nodes, 17 leaves, and maximum depth 4.
- Generalization gap: 84.18% - 75.14% = 9.04 percentage points.

Compared with the depth-limited Gini model, testing accuracy decreases by 1.70 percentage points and testing error increases by 1.70 points. Entropy produces a slightly smaller tree, with 6 fewer nodes and 2 fewer leaves, but it makes 3 more testing errors.

### Why it does not improve overall accuracy

Gini and Entropy rank some candidate splits differently. In the learned trees, both criteria choose `Past_Exam_Scores <= 72.5` at the root, but they choose different branches below it. Those Entropy-selected branches are slightly less effective for the overall holdout set.

The confusion matrices reveal a trade-off:

| Criterion at depth 4 | Fail recall | Pass recall | Overall testing accuracy |
| --- | ---: | ---: | ---: |
| Gini | 74/88 (84.09%) | 62/89 (69.66%) | 76.84% |
| Entropy | 64/88 (72.73%) | 69/89 (77.53%) | 75.14% |

Entropy recognizes 7 more passing students, but it correctly recognizes 10 fewer failing students. Thus, changing to Entropy does not improve overall accuracy on this split, although its higher `Pass` recall could be useful if missing a passing student were considered more costly than incorrectly predicting a pass.

## Conclusion

The fully grown tree clearly overfits. Limiting the depth to 4 is the strongest improvement: it substantially reduces tree complexity, narrows the generalization gap, raises testing accuracy from 67.80% to 76.84%, and reduces testing error from 32.20% to 23.16%.

Changing the criterion to Entropy at the same depth still performs better than the fully grown baseline, mainly because it retains depth pruning. However, it does not outperform depth-limited Gini. The recommended configuration is therefore a Gini decision tree with `max_depth=4`.

## Reproduction

Run the experiments from the repository root:

```powershell
python -m src.pure
python -m src.depth
python -m src.depth_cri
```
