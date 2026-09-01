// Report - Lab 2 Decision Tree - GROUP 6 - Format học từ references 2/TECHNICAL_REPORT.typ
#set document(
  title: "Lab 2 - Decision Tree Modeling and Improvement",
  author: ("Nguyen Minh Duc", "Van Phu Duc", "Huynh Minh Hung", "Hy Hue Hung"),
  keywords: ("decision tree", "Gini", "Entropy", "pre-pruning", "student performance"),
)
#let c-navy = rgb("#16324f")
#let c-accent = rgb("#2f6da3")
#let c-gray = rgb("#5a6472")
#let c-light-gray = rgb("#8a93a0")
#let c-rule = rgb("#c3ccd6")
#let c-tbl-head = rgb("#dde6f0")
#let c-tbl-zebra = rgb("#f3f6fa")
#let c-code-bg = rgb("#f5f6f8")
#let c-code-border = rgb("#d9dde2")

#set page(paper: "a4", margin: (top: 2.2cm, bottom: 2.2cm, left: 2.4cm, right: 2.4cm))
#set text(font: ("Times New Roman", "Liberation Serif"), size: 13pt, lang: "en", hyphenate: true)
#set par(justify: true, leading: 0.65em, spacing: 0.5em)
#set heading(numbering: "1.")
#show heading: set block(above: 0pt, below: 0pt)
#show heading.where(level: 1): it => block(
  above: 30pt,
  below: 18pt,
)[
  #set text(size: 20pt, weight: "bold", fill: c-navy, tracking: 0.3pt)
  #it
  #v(4pt)
  #line(length: 100%, stroke: 1pt + c-navy)
]
#show heading.where(level: 2): it => block(
  above: 20pt,
  below: 13pt,
)[
  #set text(size: 15pt, weight: "bold", fill: c-accent)
  #it
]
#show heading.where(level: 3): it => block(
  above: 16pt,
  below: 10pt,
)[
  #set text(size: 13.5pt, weight: "bold", fill: c-navy)
  #it
]
#show heading.where(level: 4): it => block(
  above: 14pt,
  below: 8pt,
)[
  #set text(size: 12pt, weight: "bold", fill: c-gray)
  #it
]
#set figure(numbering: "1", supplement: auto, placement: none)
#show figure: set align(center)
#show figure: set block(above: 1.1em, below: 1.1em)
#show figure.caption: it => {
  let num = numbering(it.numbering, it.counter.get().first())
  [#it.supplement #num. #it.body]
}
#show figure.caption: set text(size: 10.5pt, fill: c-gray)
#show link: set text(fill: c-accent)
#let report-title = "Lab 2 - Decision Tree Modeling and Improvement"
#let report-sub = "GROUP 6 - Class 24C03"
#let hdr = context {
  grid(columns: (1fr, auto), [#text(9.5pt, weight: "bold", fill: c-navy)[#report-title]], [#text(9.5pt, fill: c-light-gray)[#report-sub]])
  v(3pt)
  line(length: 100%, stroke: 0.4pt + c-rule)
  v(10pt)
}
#let ftr-body = context {
  let n = counter(page).get().first()
  let total = counter(page).final().first()
  align(center)[#text(10pt, fill: c-light-gray)[Page #n of #total]]
}
#let ftr-toc = context { align(center)[#text(10pt, fill: c-light-gray)[#counter(page).display("i")]] }
#show raw.where(block: true): it => block(
  width: 100%,
  fill: c-code-bg,
  inset: (x: 10pt, y: 8pt),
  radius: 3pt,
  stroke: 0.5pt + c-code-border,
  above: 0.8em,
  below: 1em,
)[
  #set text(font: ("Consolas", "Courier New"), size: 10.5pt)
  #it
]
#show raw.where(block: false): set text(font: ("Consolas", "Courier New"), size: 0.85em, fill: rgb("#7a2e2e"))
#set list(spacing: 0.32em)
#show table: it => {
  set table(inset: (x: 7pt, y: 5pt), stroke: 0.4pt + c-rule, fill: (x, y) => if y == 0 { c-tbl-head } else if calc.mod(y, 2) == 0 { c-tbl-zebra } else { white })
  it
}
#show table: set text(size: 10.5pt)
#show table.header: set text(weight: "bold", fill: c-navy)

// COVER
#set page(header: none, footer: none, numbering: none)
#align(center)[#image("assets/Logo.png", width: 3.9cm)]
#v(0.4cm)
#align(center)[
  #text(12pt, weight: "bold", fill: c-navy, tracking: 0.5pt)[VIETNAM NATIONAL UNIVERSITY -- HO CHI MINH CITY]
  #v(2pt)
  #text(10.5pt, fill: c-gray)[University of Science]
  #v(1pt)
  #text(10.5pt, fill: c-gray)[Faculty of Information Technology]
]
#v(1fr)
#align(center)[
  #text(13.5pt, weight: "medium", tracking: 4pt, fill: c-accent)[LABORATORY REPORT]
  #v(10pt)
  #text(26pt, weight: "bold", fill: c-navy)[Decision Tree Modeling and Improvement]
  #v(10pt)
  #block(width: 80%)[#text(12.5pt, style: "italic", fill: c-gray)[Student Performance Prediction -- Pass/Fail Classification on Kaggle Dataset]]
]
#v(1fr)
#align(center)[#line(length: 44%, stroke: 0.8pt + c-navy)]
#v(0.7cm)
#align(center)[
  #grid(columns: (auto, auto), column-gutter: 1.0cm, row-gutter: 9pt, align: (right, left),
    [#text(11.5pt, weight: "bold", fill: c-navy)[Coursework]], [#text(11.5pt)[Introduction to Artificial Intelligence -- Lab 2]],
    [#text(11.5pt, weight: "bold", fill: c-navy)[Report status]], [#text(11.5pt)[Final version]],
    [#text(11.5pt, weight: "bold", fill: c-navy)[Prepared on]], [#text(11.5pt)[September 2026]],
    [#text(11.5pt, weight: "bold", fill: c-navy)[Repository]], [#text(11.5pt)[github.com/AdrianParry-17/AI-Lab-Decision-Tree]],
  )
]
#v(1fr)
#align(center)[#line(length: 44%, stroke: 0.8pt + c-navy)]
#v(0.7cm)
#align(center)[
  #text(14pt, weight: "bold", fill: c-navy)[GROUP 6]
  #v(3pt)
  #text(11pt, fill: c-gray)[Class / section 24C03]
  #v(12pt)
  #grid(columns: (auto, auto), column-gutter: 1.4cm, row-gutter: 9pt, align: (right, left),
    [#text(11.5pt)[Nguyen Minh Duc]], [#text(11.5pt, fill: c-gray)[24127345 -- Visualize, Analysis]],
    [#text(11.5pt)[Van Phu Duc]], [#text(11.5pt, fill: c-gray)[24127346 -- Video]],
    [#text(11.5pt)[Huynh Minh Hung]], [#text(11.5pt, fill: c-gray)[24127385 -- Train, Improvement]],
    [#text(11.5pt)[Hy Hue Hung]], [#text(11.5pt, fill: c-gray)[24127388 -- Dataset, Report]],
  )
]
#v(1fr)
#align(center)[#text(9.5pt, fill: c-light-gray)[HCMC University of Science]]
#v(0.5cm)
#pagebreak()

// TOC
#set page(header: hdr, footer: ftr-toc, numbering: "i")
#counter(page).update(1)
#show outline.entry: set text(size: 10.5pt)
#show outline.entry.where(level: 2): set text(weight: "bold", fill: c-navy)
#align(center)[#text(17pt, weight: "bold", fill: c-navy, tracking: 1pt)[Contents] #v(3pt) #line(length: 100%, stroke: 0.6pt + c-navy)]
#v(16pt)
#outline(depth: 3, title: none, indent: auto)
#pagebreak()

// BODY
#set page(header: hdr, footer: ftr-body, numbering: "1")
#counter(page).update(1)

= Group Introduction
The contributions below reflect the group's final task allocation as required by Lab 2 - Decision Tree.pdf:4.

#figure(align(center)[#table(columns: (auto, 1fr, auto, 1fr), align: (auto,auto,auto,auto), table.header([No.], [Full Name], [Student ID], [Contribution]), table.hline(), [1], [Nguyen Minh Duc], [24127345], [Visualize, Analysis], [2], [Van Phu Duc], [24127346], [Video presentation], [3], [Huynh Minh Hung], [24127385], [Train, Improvement], [4], [Hy Hue Hung], [24127388], [Dataset, Report])], caption: [Group members and contributions], kind: table)

#figure(align(center)[#table(columns: (50%, 50%), align: (auto,auto), table.header([Field], [Value]), table.hline(), [Group name], [GROUP 6], [Class / section], [24C03], [Project repository], [https://github.com/AdrianParry-17/AI-Lab-Decision-Tree], [Report status], [Final version])], caption: [Group information], kind: table)

= Introduction
== Decision Trees
A decision tree is a non-parametric supervised learning model that recursively partitions the data by choosing the attribute and threshold that best reduces impurity. Two common impurity measures for classification are Gini impurity and Entropy:

$ "Gini" = 1 - sum_i p_i^2 $
$ "Entropy" = - sum_i p_i log_2 p_i $

At each node the algorithm tests all possible splits and selects the one that minimizes weighted impurity. Splitting stops when a node becomes pure, no useful split remains, or a stopping criterion such as maximum depth is reached. Each leaf predicts the majority class of its training samples, so every root-to-leaf path can be read as an intuitive if-then rule. The custom implementation in this project handles categorical strings directly via value-based splits and numerical features via threshold splits.

Decision trees are especially attractive because they are interpretable, handle mixed-type features without scaling, and capture non-linear, conditional relationships.

#figure(grid(columns: (1fr, 1fr, 1fr), gutter: 8pt,
  box(fill: rgb("#f0f7ff"), stroke: 0.6pt + rgb("#c2d6f0"), radius: 5pt, inset: 8pt, height: 2.2cm)[#align(center + horizon)[#text(weight: "bold", fill: c-navy)[INPUT] \ #v(3pt) #text(size: 10pt)[7 features \ Mixed types]]],
  box(fill: rgb("#eef7ee"), stroke: 0.6pt + rgb("#b9d9b9"), radius: 5pt, inset: 8pt, height: 2.2cm)[#align(center + horizon)[#text(weight: "bold", fill: rgb("#2a6b2a"))[SPLIT] \ #v(3pt) #text(size: 10pt)[Gini / Entropy]]],
  box(fill: rgb("#fff7e8"), stroke: 0.6pt + rgb("#e0c0a0"), radius: 5pt, inset: 8pt, height: 2.2cm)[#align(center + horizon)[#text(weight: "bold", fill: rgb("#8a5a2a"))[LEAF] \ #v(3pt) #text(size: 10pt)[Majority vote]]],
), caption: [Decision-tree pipeline: Input -> Split -> Leaf.])

== Project Objective
The objectives of this lab are to understand how a decision tree works, apply it to a real dataset, evaluate its performance with appropriate metrics, analyze the resulting tree, propose and test two to three improvements, and practice technical writing and teamwork.

= Dataset Description
== Source
The dataset used in this project is the public *Student Performance Prediction* dataset from Kaggle: https://www.kaggle.com/datasets/amrmaree/student-performance-prediction. A local copy is stored as `data/student_data.csv` for reproducibility. The task is binary classification: predicting whether a student will Pass or Fail.

== Samples, Features and Target
*Samples*

#figure(align(center)[#table(columns: 2, align: (auto,right), table.header([Statistic], [Count]), table.hline(), [Total rows], [708], [Distinct records], [500], [Duplicate rows (oversampled)], [208], [Training set (75%)], [531 rows (375 distinct)], [Testing set (25%)], [177 rows (125 distinct)], [Missing values], [0])], caption: [Sample counts. Stratified split, seed 42, duplicates grouped to avoid leakage.], kind: table)

The overall dataset is perfectly balanced, with equal numbers of Fail and Pass samples. The training and testing partitions are nearly balanced, and duplicate-group verification shows zero overlap.

#figure(align(center)[#table(columns: 4, align: (auto,auto,auto,auto), table.header([Partition], [Fail], [Pass], [Total]), table.hline(), [Overall], [354 (50.0%)], [354 (50.0%)], [708], [Training], [266 (50.1%)], [265 (49.9%)], [531], [Testing], [88 (49.7%)], [89 (50.3%)], [177])], caption: [Class distribution.], kind: table)

#figure(image("assets/dataset_overview.png", width: 90%), caption: [Dataset overview: balanced classes and feature types.])

*Features* -- 10 raw columns, 7 usable after excluding `Student_ID` and `Final_Exam_Score` (leakage):

#figure(align(center)[#table(columns: 3, align: (auto,auto,auto), table.header([Column], [Type], [Description]), table.hline(), [Gender], [Categorical], [Male, Female], [Study_Hours_per_Week], [Numerical], [10--39, mean Pass 28.8, Fail 23.5], [Attendance_Rate], [Numerical], [50.1--99.9, mean Pass 83.6, Fail 72.6], [Past_Exam_Scores], [Numerical], [50--100, mean Pass 84.2, Fail 71.6], [Parental_Education_Level], [Categorical], [High School, Bachelors, Masters, PhD], [Internet_Access_at_Home], [Categorical], [Yes / No], [Extracurricular_Activities], [Categorical], [Yes / No])], caption: [The 7 features used for modeling (3 numerical, 4 categorical).], kind: table)

Target variable: `Pass_Fail` with two classes, Pass and Fail.

== Preprocessing
1. Validate header and required columns.
2. Remove `Student_ID` and `Final_Exam_Score`.
3. Convert numerical columns to int/float and keep categorical strings via `AttributeValueSplit` (no one-hot needed).
4. Check for missing values.
5. Stratified 75/25 split with seed 42, duplicates grouped.
6. No scaling needed.

== Why This Dataset Fits Decision Trees
This dataset is well suited for decision trees. It is a classification problem where interpretability matters. It contains mixed numerical and categorical features with natural thresholds, which the custom tree handles directly. Study time and attendance interact conditionally with past scores, and trees model such non-linear interactions naturally. The size is moderate (708 rows, 500 distinct), large enough to learn but small enough to visualize and demonstrate pre-pruning (171 nodes depth 10 -> 35 nodes depth 4).

= Baseline Model
== Model Description
- *Algorithm:* Weighted Gini impurity (custom implementation).
- *Maximum depth:* None (fully grown).
- *Stopping condition:* Pure node or no improving split, or `max_depth` (pre-pruning via `MaxDepthStoppingCriterion`).
- *Features:* 7.

== Training and Testing Procedure
Same pipeline for all experiments: load, duplicate-group stratified split (75/25, seed 42), train, evaluate. Keeping split identical isolates model effects.

- Training: 531 rows (375 distinct) -- Fail 266, Pass 265
- Testing: 177 rows (125 distinct) -- Fail 88, Pass 89

Reproduction:

```python
python -m src.pure
python -m src.depth
python -m src.depth_cri
```

== Resulting Tree
The baseline tree has 171 nodes, 93 leaves, depth 10. Root split is `Past_Exam_Scores <= 72.5`. The figure shows an excerpt captured from the visualization; the full tree is in the appendix and interactive HTML.

#figure(image("assets/1.png", width: 100%), caption: [Excerpt of the baseline fully grown tree (171 nodes, depth 10). Full tree in appendix and interactive HTML.])

== Accuracy and Error Rate
#figure(align(center)[#table(columns: 5, align: (auto,auto,auto,auto,auto), table.header([Dataset], [Correct], [Incorrect], [Accuracy], [Error Rate]), table.hline(), [Training], [531/531], [0/531], [100.00%], [0.00%], [Testing], [120/177], [57/177], [67.80%], [32.20%])], caption: [Baseline accuracy and error rate.], kind: table)

Confusion matrices, with `Actual \ Predicted` layout:

#figure(align(center)[#table(columns: 3, align: (auto,auto,auto), table.header([Actual \ Predicted], [Fail], [Pass]), table.hline(), [Fail], [266], [0], [Pass], [0], [265])], caption: [Training -- 100% accuracy.], kind: table)
#figure(align(center)[#table(columns: 3, align: (auto,auto,auto), table.header([Actual \ Predicted], [Fail], [Pass]), table.hline(), [Fail], [79], [9], [Pass], [48], [41])], caption: [Testing -- 67.80% accuracy. Fail recall 89.77%, Pass recall 46.07%, gap 32.20 pp.], kind: table)

Extended metrics: Fail Precision 62.20% Recall 89.77% F1 73.49%; Pass Precision 82.00% Recall 46.07% F1 58.99%; Macro F1 66.24%, Balanced accuracy 67.92%. ROC-AUC not reported (hard labels only).

#figure(image("assets/confusion_test.png", width: 95%), caption: [Confusion matrices for the three models on the held-out test set.])

= Analysis of the Resulting Tree
== Overall Structure
The tree is constructed top-down greedily: each node evaluates all value and threshold splits and picks the one most reducing impurity. With depth 10 and 93 leaves, the baseline is much larger than depth-limited models.

== Important Decision Rules
1. *Strongest root-level separation.* Threshold 72.5 selected in all three experiments, indicating best impurity reduction at root.
2. *Study time is conditional.* 36 hours in low-score branch vs 19.5 hours in high-score branch -- weaker past scores need more hours to compensate.
3. *Attendance resolves borderline.* Higher attendance generally leads to Pass, but threshold varies by branch.
4. *Deep branches use secondary features.* Gender and other categorical splits at depth 5--10 separate only a few samples (baseline avg 5.7 samples/leaf vs 27.9/31.2 after pruning) and likely capture noise.


== Feature Usage and Impurity Analysis

The baseline tree uses all 7 features but with highly skewed frequency: Attendance_Rate 27 times (34.6% of splits), Study_Hours 19 times (24.4%), Past_Exam_Scores 14 times (17.9%), Gender 9 times (11.5%), Parental_Education 7 times (9.0%), Internet and Extracurricular only once each (1.3%). This confirms numerical features dominate early splits while categorical features are relegated to deep, small leaves. At the root, the Gini impurity drops from 0.5000 (balanced) to a weighted 0.4223 after the Past_Exam_Scores <= 72.5 split (reduction 0.0777; Entropy reduction 0.1161, from 1.0000 to 0.8839; left branch n=202 Fail 152/Pass 50, right branch n=329 Fail 114/Pass 215) -- a clear separation that explains why this threshold is consistently chosen.

All 93 leaves of the baseline are pure (100% contain only one class), averaging 5.7 samples/leaf -- direct evidence of memorization rather than generalization.

== Strengths and Weaknesses
*Strengths:* Fully transparent, perfect training fit, intuitive root, captures conditional interactions.
*Weaknesses:* Too deep for 7 features, gap 32.20 pp indicates overfitting, biased toward Fail, deep secondary splits likely noise. The tree overfits and motivates pre-pruning.

#figure(image("assets/4.png", width: 100%), caption: [Analysis view from the interactive visualization.])

= Improvement Methods
Two improvements keep data, split, and seed unchanged.

== Improvement 1 -- Depth Limiting (Gini, max_depth = 4) -- Pre-pruning
*Method:* Pre-pruned by limiting maximum depth to 4 via `MaxDepthStoppingCriterion`. Other settings remain Gini.

*Results:* 35 nodes, 19 leaves, depth 4 (approx. 79.5% fewer nodes than baseline). Training 454/531 (85.50% / 14.50%), Testing 136/177 (76.84% / 23.16%).

#figure(image("assets/2.png", width: 100%), caption: [Excerpt of the depth-limited Gini tree (35 nodes, depth 4).])

Confusion matrix (held-out test):

#figure(align(center)[#table(columns: 3, align: (auto,auto,auto), table.header([Actual \ Predicted], [Fail], [Pass]), table.hline(), [Fail], [74], [14], [Pass], [27], [62])], caption: [Gini depth=4 -- held-out test.], kind: table)

Extended: Fail 73.27/84.09/78.31; Pass 81.58/69.66/75.15; Macro F1 76.73%, Balanced 76.88%. Gap reduced 32.20 -> 8.66 pp, +9.04 pp test. Bias-variance trade-off: larger leaves (27.9 vs 5.7 samples/leaf) reduce variance.

== Improvement 2 -- Criterion Change (Gini to Entropy, depth = 4)
*Method:* Keep depth 4, change Gini to Entropy.

*Results:* 29 nodes, 17 leaves, depth 4 -- smallest. Training 447/531 (84.18% / 15.82%), Testing 133/177 (75.14% / 24.86%).

#figure(image("assets/3.png", width: 100%), caption: [Excerpt of the depth-limited Entropy tree (29 nodes, depth 4).])

Confusion matrix (held-out test):

#figure(align(center)[#table(columns: 3, align: (auto,auto,auto), table.header([Actual \ Predicted], [Fail], [Pass]), table.hline(), [Fail], [64], [24], [Pass], [20], [69])], caption: [Entropy depth=4 -- held-out test.], kind: table)

Extended: Fail 76.19/72.73/74.42; Pass 74.19/77.53/75.82; Macro F1 75.12%.

#figure(align(center)[#table(columns: 4, align: (auto,auto,auto,auto), table.header([Criterion (depth 4)], [Fail recall], [Pass recall], [Test Accuracy]), table.hline(), [Gini], [74/88 (84.09%)], [62/89 (69.66%)], [76.84%], [Entropy], [64/88 (72.73%)], [69/89 (77.53%)], [75.14%])], caption: [Gini vs Entropy at depth 4.], kind: table)

Entropy is slightly less effective overall (-1.70 pp, 3 more errors) on this balanced data, is more sensitive to pure splits, creates smaller tree (29 vs 35 nodes) and earlier Attendance splits, helping Pass recall (+7) but harming Fail recall (-10).

= Comparison of Results
#figure(align(center)[#table(columns: 11, align: (auto,auto,auto,auto,auto,auto,auto,auto,auto,auto,auto), table.header([Model], [Criterion], [Depth], [Nodes], [Leaves], [Depth], [Train Acc.], [Train Err.], [Test Acc.], [Test Err.], [Gap]), table.hline(), [Baseline], [Gini], [None], [171], [93], [10], [100.00%], [0.00%], [67.80%], [32.20%], [32.20], [Depth-limited], [Gini], [4], [35], [19], [4], [85.50%], [14.50%], [76.84%], [23.16%], [8.66], [Depth-limited], [Entropy], [4], [29], [17], [4], [84.18%], [15.82%], [75.14%], [24.86%], [9.04])], caption: [Overall comparison on the held-out test set. Best in bold. Nodes decrease by approx. 79.5% (171 -> 35).], kind: table)

#figure(image("assets/comparison_accuracy.png", width: 88%), caption: [Training vs held-out testing accuracy and gap.])
#figure(image("assets/comparison_nodes.png", width: 78%), caption: [Model complexity -- pre-pruning reduces size by about 80%.])
#figure(image("assets/gap.png", width: 72%), caption: [Generalization gap reduced from 32.20 to 8.66 points.])

Best on held-out test: depth-limited Gini, max_depth=4 (76.84%, 23.16% error).

= Conclusion
This project shows how decision trees learn thresholds directly from data and how easily a fully grown tree can overfit (100% train vs 67.80% test, 171 nodes). Limiting depth to 4 with pre-pruning proved most effective: removed 136 nodes (approx. 79.5% fewer), reduced gap 32.20 -> 8.66, raised held-out test to 76.84%. Changing Gini to Entropy at same depth produced a slightly smaller tree with different recall trade-off but did not beat Gini. Recommended: Gini, max_depth=4 (76.84% on held-out test, 23.16% error, 35 nodes, 19 leaves). With depth limiting, trees reach about 77% on this held-out split, suggesting usefulness for early warning while remaining transparent. This is limited to the reported split.

= References
1. Lab 2 -- Decision Tree Modeling and Improvement, HCMUS.
2. Dataset: Amr Maree -- Student Performance Prediction, Kaggle. https://www.kaggle.com/datasets/amrmaree/student-performance-prediction (local copy: data/student_data.csv, 708 rows, 500 distinct).
3. Breiman et al. -- Classification and Regression Trees (1984).
4. Quinlan -- Induction of Decision Trees (1986) and Mitchell -- Machine Learning, Ch. 3 (1997).
5. Scikit-learn -- Decision Trees (background).
6. Project implementation: Custom framework in model/ and src/utils.py, src/pure.py, src/depth.py, src/depth_cri.py.
7. Visualization: docs/tree_visualization.html and report/assets/ (1.png-4.png and generated charts).

#pagebreak()
= Appendices
== Appendix A -- Baseline Tree (detailed excerpt)
The full baseline tree has 171 nodes, 93 leaves, depth 10. Top 4 levels:

#block(fill: c-code-bg, inset: 8pt, radius: 3pt, stroke: 0.5pt + c-code-border)[
  #text(font: ("Consolas", "Courier New"), size: 8pt)[
    Split on Past_Exam_Scores at 72.5 \
    ├── If <= 72.5: Split on Study_Hours_per_Week at 36 \
    │   ├── If <= 36: Split on Attendance_Rate at 92.47 \
    │   │   ├── If <= 92.47: Split on Study_Hours at 26.5 ... \
    │   └── If > 36: Split on Attendance_Rate at 72.79 ... \
    └── If > 72.5: Split on Study_Hours at 19.5 ... \
    Leaf avg 5.7/leaf (4.0 distinct) -- many 1-2 sample leaves.
  ]
]
Full text: docs/RESULT_PURE.md. Interactive: docs/tree_visualization.html and report/assets/1.png.

== Appendix B -- Depth-limited Gini Tree
Top 4 levels (35 nodes, 19 leaves):

#block(fill: c-code-bg, inset: 8pt, radius: 3pt, stroke: 0.5pt + c-code-border)[
  #text(font: ("Consolas", "Courier New"), size: 8pt)[
    Split on Past_Exam_Scores at 72.5 \
    ├── If <= 72.5: Split on Study_Hours at 36 ... \
    └── If > 72.5: Split on Study_Hours at 19.5 ... \
    Leaf avg 27.9/leaf (19.7 distinct).
  ]
]
Full text: docs/RESULT_DEPTH.md and report/assets/2.png.

== Appendix C -- Depth-limited Entropy Tree
Top 4 levels (29 nodes, 17 leaves):

#block(fill: c-code-bg, inset: 8pt, radius: 3pt, stroke: 0.5pt + c-code-border)[
  #text(font: ("Consolas", "Courier New"), size: 8pt)[
    Split on Past_Exam_Scores at 72.5 \
    ├── If <= 72.5: Split on Attendance at 76.57 ... \
    └── If > 72.5: Split on Attendance at 80.89 ... \
    Leaf avg 31.2/leaf (22.0 distinct).
  ]
]
Full text: docs/RESULT_DEPTH_CRI.md and report/assets/3.png.

== Appendix D -- Reproduction
From repository root (verified):

#block(fill: c-code-bg, inset: 8pt, radius: 3pt, stroke: 0.5pt + c-code-border)[
  #text(font: ("Consolas", "Courier New"), size: 9pt)[
    python -m src.pure \ 
    python -m src.depth \ 
    python -m src.depth_cri \ 
    Outputs: docs/RESULT_PURE.md, docs/RESULT_DEPTH.md, docs/RESULT_DEPTH_CRI.md \ 
    Assets: python report/assets/generate_assets.py \ 
    Report: typst compile report/Report.typ report/Report.pdf
  ]
]
Settings: duplicate-group aware split, 75/25, seed 42, Gini/Entropy, max_depth, AttributeValueSplit/ThresholdSplit, pre-pruning only.

#align(center)[#v(1em) #text(size: 10pt, fill: c-light-gray)[-- End of Report -- GROUP 6 / 24C03 / 2026 --]]
