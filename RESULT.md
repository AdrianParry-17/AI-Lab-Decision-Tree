# Decision Tree Result

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
- Numeric CSV values were converted to `int`/`float`; categorical values remain strings.

## Model summary

- Trainer: custom `CreateAttributeClassificationTrainingStrategy`
- Split objective: weighted Gini impurity
- Pre-pruning: maximum depth `4`
- Early stopping: make a leaf when all local labels are identical
- Nodes: 35
- Leaves: 19
- Learned maximum depth: 4
- Training accuracy: 454/531 (85.50%)
- Testing accuracy: 136/177 (76.84%)

## Confusion matrix (training data)

| Actual \ Predicted | Fail | Pass |
| --- | ---: | ---: |
| Fail | 225 | 41 |
| Pass | 36 | 229 |

## Confusion matrix (testing data)

| Actual \ Predicted | Fail | Pass |
| --- | ---: | ---: |
| Fail | 74 | 14 |
| Pass | 27 | 62 |

## Final tree

```text
Split on `Past_Exam_Scores` at `72.5`
├── If `Past_Exam_Scores` <= `72.5`:
│   Split on `Study_Hours_per_Week` at `36`
│   ├── If `Study_Hours_per_Week` <= `36`:
│   │   Split on `Attendance_Rate` at `92.4714`
│   │   ├── If `Attendance_Rate` <= `92.4714`:
│   │   │   Split on `Study_Hours_per_Week` at `26.5`
│   │   │   ├── If `Study_Hours_per_Week` <= `26.5`: Predict `Fail`
│   │   │   └── If `Study_Hours_per_Week` > `26.5`: Predict `Fail`
│   │   └── If `Attendance_Rate` > `92.4714`:
│   │       Split on `Study_Hours_per_Week` at `26`
│   │       ├── If `Study_Hours_per_Week` <= `26`: Predict `Fail`
│   │       └── If `Study_Hours_per_Week` > `26`: Predict `Pass`
│   └── If `Study_Hours_per_Week` > `36`:
│       Split on `Attendance_Rate` at `72.7952`
│       ├── If `Attendance_Rate` <= `72.7952`: Predict `Fail`
│       └── If `Attendance_Rate` > `72.7952`:
│           Split on `Past_Exam_Scores` at `56`
│           ├── If `Past_Exam_Scores` <= `56`: Predict `Fail`
│           └── If `Past_Exam_Scores` > `56`: Predict `Pass`
└── If `Past_Exam_Scores` > `72.5`:
    Split on `Study_Hours_per_Week` at `19.5`
    ├── If `Study_Hours_per_Week` <= `19.5`:
    │   Split on categorical feature `Parental_Education_Level`
    │   ├── If `Parental_Education_Level` = `Bachelors`:
    │   │   Split on `Attendance_Rate` at `89.1648`
    │   │   ├── If `Attendance_Rate` <= `89.1648`: Predict `Fail`
    │   │   └── If `Attendance_Rate` > `89.1648`: Predict `Pass`
    │   ├── If `Parental_Education_Level` = `High School`:
    │   │   Split on `Attendance_Rate` at `89.9956`
    │   │   ├── If `Attendance_Rate` <= `89.9956`: Predict `Fail`
    │   │   └── If `Attendance_Rate` > `89.9956`: Predict `Pass`
    │   ├── If `Parental_Education_Level` = `Masters`:
    │   │   Split on `Attendance_Rate` at `66.4159`
    │   │   ├── If `Attendance_Rate` <= `66.4159`: Predict `Fail`
    │   │   └── If `Attendance_Rate` > `66.4159`: Predict `Pass`
    │   └── If `Parental_Education_Level` = `PhD`:
    │       Split on `Past_Exam_Scores` at `89.5`
    │       ├── If `Past_Exam_Scores` <= `89.5`: Predict `Fail`
    │       └── If `Past_Exam_Scores` > `89.5`: Predict `Fail`
    └── If `Study_Hours_per_Week` > `19.5`:
        Split on `Attendance_Rate` at `74.7862`
        ├── If `Attendance_Rate` <= `74.7862`:
        │   Split on `Past_Exam_Scores` at `91`
        │   ├── If `Past_Exam_Scores` <= `91`: Predict `Fail`
        │   └── If `Past_Exam_Scores` > `91`: Predict `Pass`
        └── If `Attendance_Rate` > `74.7862`:
            Split on `Study_Hours_per_Week` at `27.5`
            ├── If `Study_Hours_per_Week` <= `27.5`: Predict `Pass`
            └── If `Study_Hours_per_Week` > `27.5`: Predict `Pass`
```
