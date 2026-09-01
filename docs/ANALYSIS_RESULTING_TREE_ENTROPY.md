# Analysis of the Resulting Tree — Depth-Limited Entropy

## 1. Model overview

The analyzed model is the **depth-limited Entropy decision tree** trained to predict whether a student will `Pass` or `Fail`. It is identical to the depth-limited Gini model in data, depth, and stopping rules; only the split criterion changes.

| Property | Value |
| --- | ---: |
| Splitting criterion | Weighted Entropy |
| Maximum depth | 4 |
| Nodes | 29 |
| Leaves | 17 |
| Training accuracy | 84.18% |
| Testing accuracy | 75.14% |
| Testing error rate | 24.86% |

The complete tree visualization is available in [tree_visualization.html](tree_visualization.html) (Improved Entropy tab). The exact text representation is available in [RESULT_DEPTH_CRI.md](RESULT_DEPTH_CRI.md).

## 2. Overall structure

The root node again splits on `Past_Exam_Scores <= 72.5`, identical to the Gini tree. This confirms that previous exam performance is the strongest feature regardless of criterion. Differences appear below the root, where Entropy chooses different features and thresholds.

- For `Past_Exam_Scores <= 72.5`, the first refinement is `Attendance_Rate <= 76.5781`. Students below this directly become `Fail`; the rest are refined using `Study_Hours_per_Week` and, at the deepest level, `Past_Exam_Scores`.
- For `Past_Exam_Scores > 72.5`, the tree first checks `Attendance_Rate <= 80.8939`, then uses `Study_Hours_per_Week` (with thresholds `28.5`, `30.5`, `19.5`, `27.5`) and `Parental_Education_Level`.

Compared with the Gini tree, the Entropy tree is slightly smaller (29 nodes, 17 leaves vs 35 nodes, 19 leaves) and places `Attendance_Rate` earlier in both main branches.

## 3. Important decision rules

### Rule 1: Previous exam score is the primary separator

The root condition is `Past_Exam_Scores <= 72.5`, the same as the Gini tree. Students below enter a branch refined mainly by attendance and study time; students above enter a branch focused on attendance and study time as well, but with different thresholds.

### Rule 2: Attendance appears very early in both branches

Unlike the Gini tree, the Entropy tree uses `Attendance_Rate` as the first refinement in both the low-score and high-score subtrees:

- `Attendance_Rate <= 76.5781` → `Fail` in the low-score branch.
- `Attendance_Rate <= 80.8939` → a more selective high-score branch.

This shows that attendance is the single most informative second-level feature according to the Entropy criterion. Generally, low attendance tends toward `Fail` and high attendance allows more detailed study-time and parental-education rules.

### Rule 3: Study time is conditional on the score and attendance context

`Study_Hours_per_Week` is used at several levels with thresholds `19.5`, `27.5`, `28.5`, `30.5`, and `34.5`. As in the Gini tree, there is no single global study-hours cutoff; the relevant threshold depends on the student's previous score and attendance branch.

Notably, in the high-score branch with `Attendance_Rate > 80.8939` and `Study_Hours_per_Week > 19.5`, the tree predicts `Pass` for both further splits (27.5 and beyond). Study time matters most for students with moderate attendance and lower previous scores.

### Rule 4: Parental education refines only narrow subgroups

`Parental_Education_Level` is used in two places:

- In the low-score branch, after `Attendance_Rate > 76.5781` and `Study_Hours_per_Week <= 34.5`, all four parental-education categories predict `Fail`.
- In the high-score branch, after `Attendance_Rate > 80.8939` and `Study_Hours_per_Week <= 19.5`, the predictions differ by category: `Bachelors` and `Masters` → `Pass`, while `High School` and `PhD` → `Fail`.

The second subgroup is an example of a genuinely learned interaction: for high-scoring students who study little, parental education separates those predicted to pass from those predicted to fail.

## 4. Performance and error analysis

The test confusion matrix is:

| Actual \ Predicted | Fail | Pass |
| --- | ---: | ---: |
| Fail | 64 | 24 |
| Pass | 20 | 69 |

The model correctly classifies 64 of 88 failing students and 69 of 89 passing students:

- `Fail` recall: `64 / 88 = 72.73%`
- `Pass` recall: `69 / 89 = 77.53%`

The Entropy tree is roughly balanced: it recognizes a slightly higher share of passing students than failing ones. Compared with the Gini depth-limited tree, it recognizes 7 more passing students but 10 fewer failing students, yielding a lower overall testing accuracy (75.14% vs 76.84%).

## 5. Strengths

- The root split, `Past_Exam_Scores <= 72.5`, is stable and consistent with the Gini tree and the baseline.
- The tree is the smallest of the three (29 nodes, 17 leaves), so it is the easiest to visualize and interpret.
- It has the highest `Pass` recall (77.53%) of the models tested, so it misses relatively few students who actually pass.
- The `Past_Exam_Scores` and `Parental_Education_Level` branches form interpretable, conditional rules.
- Depth 4 removes the overfitting seen in the baseline and keeps the generalization gap small (9.04 points).

## 6. Weaknesses and overfitting assessment

The Entropy tree has a 9.04-point generalization gap (84.18% training vs 75.14% testing), similar to the Gini tree's 8.66 points. Both are far below the baseline's 32.20-point gap, so the depth limit successfully reduces overfitting.

However, the Entropy tree does not outperform the Gini tree on overall testing accuracy. It makes 3 more holdout errors (44 vs 41) for the added benefit of higher `Pass` recall. The categorical `Parental_Education_Level` splits rely on small leaf groups. For example, in the low-score branch where all categories predict `Fail`, the split adds no discrimination and only fragments the data; this reflects the interaction between the small sample and the criterion rather than a robust pattern.

As with all models here, the thresholds are dataset-specific associations, not causal rules, and results should be validated on additional data.

## 7. Conclusion

The depth-limited Entropy tree is a compact, interpretable model that fixes the baseline overfitting and slightly shifts predictions toward `Pass` (higher `Pass` recall). Its root and general structure are consistent with the other models, but it achieves a slightly lower overall testing accuracy (75.14%) than depth-limited Gini (76.84%). The choice between them depends on the goal: Entropy is preferable if recognizing passing students matters more, while Gini gives the best overall accuracy.
