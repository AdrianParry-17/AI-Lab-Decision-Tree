# Analysis of the Resulting Tree

## 1. Model overview

The analyzed model is the **fully grown baseline Gini decision tree** trained to predict whether a student will `Pass` or `Fail`.

| Property | Value |
| --- | ---: |
| Splitting criterion | Weighted Gini impurity |
| Maximum depth | None (fully grown) |
| Nodes | 171 |
| Leaves | 93 |
| Observed maximum depth | 10 |
| Training accuracy | 100.00% |
| Testing accuracy | 67.80% |
| Testing error rate | 32.20% |

The complete tree visualization is available in [tree_visualization.html](tree_visualization.html) (Baseline tab). The exact text representation is available in [RESULT_PURE.md](RESULT_PURE.md).

## 2. Overall structure

The root node splits on `Past_Exam_Scores <= 72.5`. This is the first and most influential decision rule selected by the Gini criterion. From the root, the tree forms two main subtrees:

- For `Past_Exam_Scores <= 72.5`, the tree uses `Study_Hours_per_Week` and `Attendance_Rate`, then continues splitting with additional features such as `Parental_Education_Level` and `Gender` at deeper levels.
- For `Past_Exam_Scores > 72.5`, the tree uses `Study_Hours_per_Week` first, then `Parental_Education_Level`, `Attendance_Rate`, `Gender`, `Internet_Access_at_Home`, and `Extracurricular_Activities` at successive levels.

The tree has an observed maximum depth of 10, with 171 nodes and 93 leaves. This is substantially larger than the improved models that limit depth to 4 (35 nodes and 19 leaves for the depth-limited Gini tree).

## 3. Important decision rules

### Rule 1: Previous exam score is the primary separator

The root condition is:

```text
Past_Exam_Scores <= 72.5
```

Students below this threshold enter a branch where study time and attendance are examined. Students above it enter a branch where the model expects stronger academic outcomes. This rule is consistent across all three experiments (baseline, depth-limited Gini, and depth-limited Entropy), confirming that previous exam performance is the most informative single feature in this dataset.

### Rule 2: Study time refines both score groups

The tree repeatedly uses `Study_Hours_per_Week` at multiple levels:

- In the lower-score branch, the first threshold is `36` hours per week.
- In the higher-score branch, the first threshold is `19.5` hours per week.
- Deeper branches use thresholds around `26`–`30` hours per week.

This shows that the effect of study time is conditional on previous exam performance. The model does not use one global study-hours rule for every student.

### Rule 3: Attendance resolves borderline cases

`Attendance_Rate` appears in several branches with learned thresholds. Generally, higher attendance supports a `Pass` prediction, especially when combined with sufficient study time. Lower attendance tends to lead to `Fail` in the corresponding local branch.

### Rule 4: Deep branches use secondary features

At deeper levels (depth 5–10), the tree uses features such as `Gender`, `Internet_Access_at_Home`, and `Extracurricular_Activities`. These splits separate very small groups of training records and are a sign of overfitting. For example, one branch splits on `Gender = Male` vs `Female` after already using five other features, which likely captures noise rather than a meaningful pattern.

## 4. Performance and error analysis

The test confusion matrix is:

| Actual \ Predicted | Fail | Pass |
| --- | ---: | ---: |
| Fail | 79 | 9 |
| Pass | 48 | 41 |

The baseline correctly classifies 79 of 88 failing students and 41 of 89 passing students:

- `Fail` recall: `79 / 88 = 89.77%`
- `Pass` recall: `41 / 89 = 46.07%`

The tree is heavily biased toward predicting `Fail`. It correctly identifies nearly 90% of failing students, but it misclassifies 48 out of 89 passing students as `Fail` — more than half of the passing class. The Pass precision is also low: many students predicted as Pass are actually Fail (9 misclassifications out of 50 Pass predictions, so Pass precision is 41/50 = 82.00%). This asymmetry is important: the model is conservative and flags many students as failing, even when they would actually pass.

## 5. Strengths

- The rules are fully transparent and can be traced from root to leaf.
- The tree achieves 100.00% training accuracy, perfectly fitting the training data.
- The root split on `Past_Exam_Scores <= 72.5` is intuitive and consistent with domain knowledge.
- The model captures non-linear interactions among features, such as the conditional effect of study time on exam scores.

## 6. Weaknesses and overfitting assessment

The tree has an observed maximum depth of 10 and contains 171 nodes and 93 leaves. This is a very large and complex structure for a dataset with only 7 input features.

The generalization gap is 32.20 percentage points (100.00% training accuracy vs 67.80% testing accuracy). This is strong evidence of overfitting: the tree memorizes the training data instead of learning generalizable patterns. The perfect training score means the tree has learned not only the signal but also the noise in the training partition.

The deep branches that use `Gender`, `Internet_Access_at_Home`, and `Extracurricular_Activities` are unlikely to generalize. These features appear at depth 5–10 and separate very small subsets of the training data. For example, one branch at depth 8 splits on `Gender` after already using `Past_Exam_Scores`, `Study_Hours_per_Week`, and `Attendance_Rate`. Another branch uses `Extracurricular_Activities` in a similarly narrow context. These splits are likely fitting noise, not real structure.

The tree is not too simple — it is the opposite. It is too deep and too complex for this dataset. The 171-node tree is difficult to interpret, and the 93 leaves mean that many predictions are made on very small groups of training records (on average fewer than 6 training records per leaf, and many leaves contain only 1–2 records). This granularity reduces the model's ability to generalize to unseen data.

## 7. Conclusion

The fully grown baseline tree is a clear case of overfitting. It achieves perfect training accuracy but has a 32.20-point testing gap, is heavily biased toward the `Fail` class, and uses deep splits on secondary features that are unlikely to generalize. These weaknesses motivate the improvements tested in this project, particularly limiting the tree depth to reduce complexity and improve generalization.