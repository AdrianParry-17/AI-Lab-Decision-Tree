# Analysis of the Resulting Tree — Depth-Limited Gini

## 1. Model overview

The analyzed model is the **depth-limited Gini decision tree** trained to predict whether a student will `Pass` or `Fail`.

| Property | Value |
| --- | ---: |
| Splitting criterion | Weighted Gini impurity |
| Maximum depth | 4 |
| Nodes | 35 |
| Leaves | 19 |
| Training accuracy | 85.50% |
| Testing accuracy | **76.84%** |
| Testing error rate | **23.16%** |

The complete tree visualization is available in [tree_visualization.html](tree_visualization.html) (Improved Gini tab). The exact text representation is available in [RESULT_DEPTH.md](RESULT_DEPTH.md).

## 2. Overall structure

The root node splits on `Past_Exam_Scores <= 72.5`. This is the first and most influential decision rule selected by the Gini criterion. From the root, the tree forms two main subtrees:

- For `Past_Exam_Scores <= 72.5`, the tree uses `Study_Hours_per_Week` and then `Attendance_Rate` to distinguish students with lower previous scores.
- For `Past_Exam_Scores > 72.5`, the tree uses `Study_Hours_per_Week` first. It then uses `Parental_Education_Level`, `Attendance_Rate`, or another previous-score threshold for more specific cases.

The tree has maximum depth 4, so no prediction requires following more than four decision levels. Compared with the fully grown baseline (171 nodes, 93 leaves, depth 10), this tree is much more compact and easier to explain.

## 3. Important decision rules

### Rule 1: Previous exam score is the primary separator

The root condition is:

```text
Past_Exam_Scores <= 72.5
```

Students below this threshold enter a branch where study time and attendance are examined. Students above it enter a branch where the model expects stronger academic outcomes, but still checks study time and other contextual features.

This rule should not be interpreted as a universal causal boundary. It is a threshold learned from the available training data and identifies an association between previous performance and the target label.

### Rule 2: Study time refines both score groups

The tree repeatedly uses `Study_Hours_per_Week`:

- In the lower-score branch, the important threshold is `36` hours per week.
- In the higher-score branch, the first threshold is `19.5` hours per week.
- Lower branches use thresholds around `26`–`27.5` hours per week.

This shows that the effect of study time is conditional on previous exam performance. The model does not use one global study-hours rule for every student.

### Rule 3: Attendance resolves borderline cases

`Attendance_Rate` appears in several branches, with learned thresholds such as `72.80`, `74.79`, and `92.47`. Generally, higher attendance supports a `Pass` prediction, especially when combined with sufficient study time. Lower attendance tends to lead to `Fail` in the corresponding local branch.

Because the thresholds differ by branch, attendance is being used to resolve groups with different academic backgrounds rather than acting as a single independent pass/fail cutoff.

### Rule 4: Parental education is a local decision factor

For students with `Past_Exam_Scores > 72.5` and `Study_Hours_per_Week <= 19.5`, the tree checks `Parental_Education_Level`. It then uses attendance or previous exam scores to make the final prediction. This feature therefore contributes to a narrower subgroup instead of controlling the whole tree.

## 4. Performance and error analysis

The test confusion matrix is:

| Actual \ Predicted | Fail | Pass |
| --- | ---: | ---: |
| Fail | 74 | 14 |
| Pass | 27 | 62 |

The model correctly classifies 74 of 88 failing students and 62 of 89 passing students:

- `Fail` recall: `74 / 88 = 84.09%`
- `Pass` recall: `62 / 89 = 69.66%`

The tree is better at identifying failing students than passing students. There are 27 `Pass` records predicted as `Fail`, compared with 14 `Fail` records predicted as `Pass`. If the purpose of the system is to identify students who may need support, this conservative behavior can be useful; however, it may incorrectly flag many students who would actually pass.

## 5. Strengths

- The rules are transparent and can be explained without a black-box model.
- A depth of 4 limits the number of decisions required for each prediction.
- The model captures non-linear interactions among previous scores, study time, attendance and parental education.
- Testing accuracy improves from 67.80% for the fully grown baseline to 76.84%.
- The smaller tree is less prone to memorizing individual training records.

## 6. Limitations and overfitting assessment

The fully grown baseline achieves 100.00% training accuracy but only 67.80% testing accuracy. Its generalization gap is 32.20 percentage points, which is strong evidence of overfitting.

The depth-limited tree has 85.50% training accuracy and 76.84% testing accuracy, reducing the gap to 8.66 percentage points. The lower gap suggests better generalization, although the model still makes 23.16% test errors and should be validated on additional data.

The learned thresholds are dataset-specific associations rather than causal rules. The data also contains repeated records, so results should be interpreted together with the documented duplicate-aware split. Finally, a single train/test split cannot establish how the model will perform in every future population.

## 7. Conclusion

The resulting depth-limited Gini tree provides the best balance between predictive performance and interpretability among the tested configurations. `Past_Exam_Scores` is the dominant first decision, while `Study_Hours_per_Week` and `Attendance_Rate` provide important branch-specific refinements. Limiting the depth makes the tree substantially easier to visualize and reduces overfitting, increasing testing accuracy to **76.84%**.
