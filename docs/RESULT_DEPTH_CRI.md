# Depth-Limited Decision Tree (Entropy)

## Method

Keep the same `max_depth=4` pre-pruning used by the Gini experiment, but select splits with weighted Entropy. Holding depth and data constant isolates the effect of changing the criterion.

## Data and preprocessing

- Source: `data/student_data.csv`
- Total rows: 708 (500 distinct labeled records)
- Training set: 531 rows (75%); 375 distinct records
- Testing set: 177 rows (25%); 125 distinct records
- Training class counts: `Fail`: 266, `Pass`: 265
- Testing class counts: `Fail`: 88, `Pass`: 89
- Split: stratified random split with seed `42`
- Duplicate records were kept in the same partition to prevent train/test leakage.
- Target: `Pass_Fail`
- Excluded inputs: `Student_ID` (identifier), `Final_Exam_Score`
- Features (7): `Gender`, `Study_Hours_per_Week`, `Attendance_Rate`, `Past_Exam_Scores`, `Parental_Education_Level`, `Internet_Access_at_Home`, `Extracurricular_Activities`
- Numeric fields were converted to `int`/`float`; categorical fields remain strings.

## Model and tree shape

- Trainer: custom `CreateAttributeClassificationTrainingStrategy`
- Splitting criterion: weighted Entropy
- Configured maximum depth: 4
- Natural stopping: make a leaf when all local labels are identical or no split is available
- Nodes: 29
- Leaves: 17
- Observed maximum depth: 4

## Accuracy and error rate

| Dataset | Correct | Incorrect | Accuracy | Error rate |
| --- | ---: | ---: | ---: | ---: |
| Training | 447/531 | 84/531 | 84.18% | 15.82% |
| Testing | 133/177 | 44/177 | 75.14% | 24.86% |

## Confusion matrix (training data)

| Actual \ Predicted | Fail | Pass |
| --- | ---: | ---: |
| Fail | 207 | 59 |
| Pass | 25 | 240 |

## Confusion matrix (testing data)

| Actual \ Predicted | Fail | Pass |
| --- | ---: | ---: |
| Fail | 64 | 24 |
| Pass | 20 | 69 |

## Final tree

```text
Split on `Past_Exam_Scores` at `72.5`
├── If `Past_Exam_Scores` <= `72.5`:
│   Split on `Attendance_Rate` at `76.5781`
│   ├── If `Attendance_Rate` <= `76.5781`: Predict `Fail`
│   └── If `Attendance_Rate` > `76.5781`:
│       Split on `Study_Hours_per_Week` at `34.5`
│       ├── If `Study_Hours_per_Week` <= `34.5`:
│       │   Split on categorical feature `Parental_Education_Level`
│       │   ├── If `Parental_Education_Level` = `Bachelors`: Predict `Fail`
│       │   ├── If `Parental_Education_Level` = `High School`: Predict `Fail`
│       │   ├── If `Parental_Education_Level` = `Masters`: Predict `Fail`
│       │   └── If `Parental_Education_Level` = `PhD`: Predict `Fail`
│       └── If `Study_Hours_per_Week` > `34.5`:
│           Split on `Past_Exam_Scores` at `56`
│           ├── If `Past_Exam_Scores` <= `56`: Predict `Fail`
│           └── If `Past_Exam_Scores` > `56`: Predict `Pass`
└── If `Past_Exam_Scores` > `72.5`:
    Split on `Attendance_Rate` at `80.8939`
    ├── If `Attendance_Rate` <= `80.8939`:
    │   Split on `Study_Hours_per_Week` at `28.5`
    │   ├── If `Study_Hours_per_Week` <= `28.5`:
    │   │   Split on `Past_Exam_Scores` at `90.5`
    │   │   ├── If `Past_Exam_Scores` <= `90.5`: Predict `Fail`
    │   │   └── If `Past_Exam_Scores` > `90.5`: Predict `Pass`
    │   └── If `Study_Hours_per_Week` > `28.5`:
    │       Split on `Study_Hours_per_Week` at `30.5`
    │       ├── If `Study_Hours_per_Week` <= `30.5`: Predict `Pass`
    │       └── If `Study_Hours_per_Week` > `30.5`: Predict `Pass`
    └── If `Attendance_Rate` > `80.8939`:
        Split on `Study_Hours_per_Week` at `19.5`
        ├── If `Study_Hours_per_Week` <= `19.5`:
        │   Split on categorical feature `Parental_Education_Level`
        │   ├── If `Parental_Education_Level` = `Bachelors`: Predict `Pass`
        │   ├── If `Parental_Education_Level` = `High School`: Predict `Fail`
        │   ├── If `Parental_Education_Level` = `Masters`: Predict `Pass`
        │   └── If `Parental_Education_Level` = `PhD`: Predict `Fail`
        └── If `Study_Hours_per_Week` > `19.5`:
            Split on `Study_Hours_per_Week` at `27.5`
            ├── If `Study_Hours_per_Week` <= `27.5`: Predict `Pass`
            └── If `Study_Hours_per_Week` > `27.5`: Predict `Pass`
```
