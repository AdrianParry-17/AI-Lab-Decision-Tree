# Fully Grown Decision Tree (Baseline)

## Method

Train with Gini impurity and no configured depth limit. The tree grows until each reachable training node is pure or cannot be split further. This is the baseline used to measure overfitting.

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
- Splitting criterion: weighted Gini impurity
- Configured maximum depth: None (fully grown)
- Natural stopping: make a leaf when all local labels are identical or no split is available
- Nodes: 171
- Leaves: 93
- Observed maximum depth: 10

## Accuracy and error rate

| Dataset | Correct | Incorrect | Accuracy | Error rate |
| --- | ---: | ---: | ---: | ---: |
| Training | 531/531 | 0/531 | 100.00% | 0.00% |
| Testing | 120/177 | 57/177 | 67.80% | 32.20% |

## Confusion matrix (training data)

| Actual \ Predicted | Fail | Pass |
| --- | ---: | ---: |
| Fail | 266 | 0 |
| Pass | 0 | 265 |

## Confusion matrix (testing data)

| Actual \ Predicted | Fail | Pass |
| --- | ---: | ---: |
| Fail | 79 | 9 |
| Pass | 48 | 41 |

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
│   │   │   └── If `Study_Hours_per_Week` > `26.5`:
│   │   │       Split on `Past_Exam_Scores` at `63`
│   │   │       ├── If `Past_Exam_Scores` <= `63`: Predict `Fail`
│   │   │       └── If `Past_Exam_Scores` > `63`:
│   │   │           Split on categorical feature `Parental_Education_Level`
│   │   │           ├── If `Parental_Education_Level` = `Bachelors`:
│   │   │           │   Split on `Study_Hours_per_Week` at `30`
│   │   │           │   ├── If `Study_Hours_per_Week` <= `30`: Predict `Fail`
│   │   │           │   └── If `Study_Hours_per_Week` > `30`:
│   │   │           │       Split on `Attendance_Rate` at `82.8092`
│   │   │           │       ├── If `Attendance_Rate` <= `82.8092`: Predict `Pass`
│   │   │           │       └── If `Attendance_Rate` > `82.8092`: Predict `Fail`
│   │   │           ├── If `Parental_Education_Level` = `High School`: Predict `Fail`
│   │   │           ├── If `Parental_Education_Level` = `Masters`: Predict `Fail`
│   │   │           └── If `Parental_Education_Level` = `PhD`:
│   │   │               Split on categorical feature `Gender`
│   │   │               ├── If `Gender` = `Female`: Predict `Fail`
│   │   │               └── If `Gender` = `Male`: Predict `Pass`
│   │   └── If `Attendance_Rate` > `92.4714`:
│   │       Split on `Study_Hours_per_Week` at `26`
│   │       ├── If `Study_Hours_per_Week` <= `26`:
│   │       │   Split on `Past_Exam_Scores` at `67.5`
│   │       │   ├── If `Past_Exam_Scores` <= `67.5`:
│   │       │   │   Split on `Attendance_Rate` at `99.1297`
│   │       │   │   ├── If `Attendance_Rate` <= `99.1297`: Predict `Fail`
│   │       │   │   └── If `Attendance_Rate` > `99.1297`:
│   │       │   │       Split on categorical feature `Gender`
│   │       │   │       ├── If `Gender` = `Female`: Predict `Pass`
│   │       │   │       └── If `Gender` = `Male`: Predict `Fail`
│   │       │   └── If `Past_Exam_Scores` > `67.5`: Predict `Pass`
│   │       └── If `Study_Hours_per_Week` > `26`:
│   │           Split on `Past_Exam_Scores` at `53.5`
│   │           ├── If `Past_Exam_Scores` <= `53.5`: Predict `Fail`
│   │           └── If `Past_Exam_Scores` > `53.5`:
│   │               Split on `Past_Exam_Scores` at `67.5`
│   │               ├── If `Past_Exam_Scores` <= `67.5`:
│   │               │   Split on `Attendance_Rate` at `95.1809`
│   │               │   ├── If `Attendance_Rate` <= `95.1809`:
│   │               │   │   Split on `Attendance_Rate` at `93.6834`
│   │               │   │   ├── If `Attendance_Rate` <= `93.6834`: Predict `Pass`
│   │               │   │   └── If `Attendance_Rate` > `93.6834`: Predict `Fail`
│   │               │   └── If `Attendance_Rate` > `95.1809`: Predict `Pass`
│   │               └── If `Past_Exam_Scores` > `67.5`: Predict `Fail`
│   └── If `Study_Hours_per_Week` > `36`:
│       Split on `Attendance_Rate` at `72.7952`
│       ├── If `Attendance_Rate` <= `72.7952`: Predict `Fail`
│       └── If `Attendance_Rate` > `72.7952`:
│           Split on `Past_Exam_Scores` at `56`
│           ├── If `Past_Exam_Scores` <= `56`: Predict `Fail`
│           └── If `Past_Exam_Scores` > `56`:
│               Split on categorical feature `Parental_Education_Level`
│               ├── If `Parental_Education_Level` = `Bachelors`:
│               │   Split on `Attendance_Rate` at `79.3608`
│               │   ├── If `Attendance_Rate` <= `79.3608`: Predict `Pass`
│               │   └── If `Attendance_Rate` > `79.3608`: Predict `Fail`
│               ├── If `Parental_Education_Level` = `High School`:
│               │   Split on `Study_Hours_per_Week` at `37.5`
│               │   ├── If `Study_Hours_per_Week` <= `37.5`:
│               │   │   Split on `Attendance_Rate` at `91.9012`
│               │   │   ├── If `Attendance_Rate` <= `91.9012`: Predict `Pass`
│               │   │   └── If `Attendance_Rate` > `91.9012`: Predict `Fail`
│               │   └── If `Study_Hours_per_Week` > `37.5`: Predict `Fail`
│               ├── If `Parental_Education_Level` = `Masters`: Predict `Pass`
│               └── If `Parental_Education_Level` = `PhD`:
│                   Split on `Study_Hours_per_Week` at `38.5`
│                   ├── If `Study_Hours_per_Week` <= `38.5`: Predict `Pass`
│                   └── If `Study_Hours_per_Week` > `38.5`:
│                       Split on `Attendance_Rate` at `87.3508`
│                       ├── If `Attendance_Rate` <= `87.3508`: Predict `Fail`
│                       └── If `Attendance_Rate` > `87.3508`: Predict `Pass`
└── If `Past_Exam_Scores` > `72.5`:
    Split on `Study_Hours_per_Week` at `19.5`
    ├── If `Study_Hours_per_Week` <= `19.5`:
    │   Split on categorical feature `Parental_Education_Level`
    │   ├── If `Parental_Education_Level` = `Bachelors`:
    │   │   Split on `Attendance_Rate` at `89.1648`
    │   │   ├── If `Attendance_Rate` <= `89.1648`: Predict `Fail`
    │   │   └── If `Attendance_Rate` > `89.1648`:
    │   │       Split on `Study_Hours_per_Week` at `16.5`
    │   │       ├── If `Study_Hours_per_Week` <= `16.5`: Predict `Pass`
    │   │       └── If `Study_Hours_per_Week` > `16.5`: Predict `Fail`
    │   ├── If `Parental_Education_Level` = `High School`:
    │   │   Split on `Attendance_Rate` at `89.9956`
    │   │   ├── If `Attendance_Rate` <= `89.9956`: Predict `Fail`
    │   │   └── If `Attendance_Rate` > `89.9956`:
    │   │       Split on categorical feature `Gender`
    │   │       ├── If `Gender` = `Female`: Predict `Pass`
    │   │       └── If `Gender` = `Male`: Predict `Fail`
    │   ├── If `Parental_Education_Level` = `Masters`:
    │   │   Split on `Attendance_Rate` at `66.4159`
    │   │   ├── If `Attendance_Rate` <= `66.4159`: Predict `Fail`
    │   │   └── If `Attendance_Rate` > `66.4159`:
    │   │       Split on categorical feature `Extracurricular_Activities`
    │   │       ├── If `Extracurricular_Activities` = `No`:
    │   │       │   Split on `Attendance_Rate` at `89.2104`
    │   │       │   ├── If `Attendance_Rate` <= `89.2104`: Predict `Fail`
    │   │       │   └── If `Attendance_Rate` > `89.2104`: Predict `Pass`
    │   │       └── If `Extracurricular_Activities` = `Yes`: Predict `Pass`
    │   └── If `Parental_Education_Level` = `PhD`:
    │       Split on `Past_Exam_Scores` at `89.5`
    │       ├── If `Past_Exam_Scores` <= `89.5`: Predict `Fail`
    │       └── If `Past_Exam_Scores` > `89.5`:
    │           Split on `Study_Hours_per_Week` at `13.5`
    │           ├── If `Study_Hours_per_Week` <= `13.5`: Predict `Fail`
    │           └── If `Study_Hours_per_Week` > `13.5`:
    │               Split on `Attendance_Rate` at `66.675`
    │               ├── If `Attendance_Rate` <= `66.675`: Predict `Fail`
    │               └── If `Attendance_Rate` > `66.675`: Predict `Pass`
    └── If `Study_Hours_per_Week` > `19.5`:
        Split on `Attendance_Rate` at `74.7862`
        ├── If `Attendance_Rate` <= `74.7862`:
        │   Split on `Past_Exam_Scores` at `91`
        │   ├── If `Past_Exam_Scores` <= `91`:
        │   │   Split on `Study_Hours_per_Week` at `34.5`
        │   │   ├── If `Study_Hours_per_Week` <= `34.5`:
        │   │   │   Split on `Past_Exam_Scores` at `73.5`
        │   │   │   ├── If `Past_Exam_Scores` <= `73.5`:
        │   │   │   │   Split on categorical feature `Gender`
        │   │   │   │   ├── If `Gender` = `Female`: Predict `Fail`
        │   │   │   │   └── If `Gender` = `Male`: Predict `Pass`
        │   │   │   └── If `Past_Exam_Scores` > `73.5`:
        │   │   │       Split on `Attendance_Rate` at `73.8702`
        │   │   │       ├── If `Attendance_Rate` <= `73.8702`:
        │   │   │       │   Split on `Attendance_Rate` at `68.804`
        │   │   │       │   ├── If `Attendance_Rate` <= `68.804`: Predict `Fail`
        │   │   │       │   └── If `Attendance_Rate` > `68.804`:
        │   │   │       │       Split on `Attendance_Rate` at `69.3722`
        │   │   │       │       ├── If `Attendance_Rate` <= `69.3722`: Predict `Pass`
        │   │   │       │       └── If `Attendance_Rate` > `69.3722`: Predict `Fail`
        │   │   │       └── If `Attendance_Rate` > `73.8702`:
        │   │   │           Split on categorical feature `Gender`
        │   │   │           ├── If `Gender` = `Female`: Predict `Pass`
        │   │   │           └── If `Gender` = `Male`: Predict `Fail`
        │   │   └── If `Study_Hours_per_Week` > `34.5`:
        │   │       Split on categorical feature `Parental_Education_Level`
        │   │       ├── If `Parental_Education_Level` = `Bachelors`: Predict `Fail`
        │   │       ├── If `Parental_Education_Level` = `High School`:
        │   │       │   Split on `Study_Hours_per_Week` at `36`
        │   │       │   ├── If `Study_Hours_per_Week` <= `36`: Predict `Fail`
        │   │       │   └── If `Study_Hours_per_Week` > `36`: Predict `Pass`
        │   │       ├── If `Parental_Education_Level` = `Masters`:
        │   │       │   Split on categorical feature `Gender`
        │   │       │   ├── If `Gender` = `Female`: Predict `Fail`
        │   │       │   └── If `Gender` = `Male`: Predict `Pass`
        │   │       └── If `Parental_Education_Level` = `PhD`:
        │   │           Split on `Study_Hours_per_Week` at `36`
        │   │           ├── If `Study_Hours_per_Week` <= `36`: Predict `Pass`
        │   │           └── If `Study_Hours_per_Week` > `36`: Predict `Fail`
        │   └── If `Past_Exam_Scores` > `91`:
        │       Split on `Attendance_Rate` at `54.8046`
        │       ├── If `Attendance_Rate` <= `54.8046`:
        │       │   Split on `Study_Hours_per_Week` at `37`
        │       │   ├── If `Study_Hours_per_Week` <= `37`: Predict `Fail`
        │       │   └── If `Study_Hours_per_Week` > `37`: Predict `Pass`
        │       └── If `Attendance_Rate` > `54.8046`:
        │           Split on `Attendance_Rate` at `71.8985`
        │           ├── If `Attendance_Rate` <= `71.8985`:
        │           │   Split on `Study_Hours_per_Week` at `37.5`
        │           │   ├── If `Study_Hours_per_Week` <= `37.5`:
        │           │   │   Split on `Attendance_Rate` at `70.4227`
        │           │   │   ├── If `Attendance_Rate` <= `70.4227`:
        │           │   │   │   Split on `Past_Exam_Scores` at `99.5`
        │           │   │   │   ├── If `Past_Exam_Scores` <= `99.5`: Predict `Pass`
        │           │   │   │   └── If `Past_Exam_Scores` > `99.5`:
        │           │   │   │       Split on `Study_Hours_per_Week` at `36`
        │           │   │   │       ├── If `Study_Hours_per_Week` <= `36`: Predict `Fail`
        │           │   │   │       └── If `Study_Hours_per_Week` > `36`: Predict `Pass`
        │           │   │   └── If `Attendance_Rate` > `70.4227`:
        │           │   │       Split on `Attendance_Rate` at `71.5198`
        │           │   │       ├── If `Attendance_Rate` <= `71.5198`: Predict `Fail`
        │           │   │       └── If `Attendance_Rate` > `71.5198`: Predict `Pass`
        │           │   └── If `Study_Hours_per_Week` > `37.5`:
        │           │       Split on categorical feature `Gender`
        │           │       ├── If `Gender` = `Female`: Predict `Pass`
        │           │       └── If `Gender` = `Male`: Predict `Fail`
        │           └── If `Attendance_Rate` > `71.8985`: Predict `Fail`
        └── If `Attendance_Rate` > `74.7862`:
            Split on `Study_Hours_per_Week` at `27.5`
            ├── If `Study_Hours_per_Week` <= `27.5`:
            │   Split on `Past_Exam_Scores` at `83.5`
            │   ├── If `Past_Exam_Scores` <= `83.5`:
            │   │   Split on categorical feature `Internet_Access_at_Home`
            │   │   ├── If `Internet_Access_at_Home` = `No`:
            │   │   │   Split on categorical feature `Gender`
            │   │   │   ├── If `Gender` = `Female`: Predict `Pass`
            │   │   │   └── If `Gender` = `Male`:
            │   │   │       Split on `Past_Exam_Scores` at `82`
            │   │   │       ├── If `Past_Exam_Scores` <= `82`: Predict `Fail`
            │   │   │       └── If `Past_Exam_Scores` > `82`:
            │   │   │           Split on `Attendance_Rate` at `84.3677`
            │   │   │           ├── If `Attendance_Rate` <= `84.3677`: Predict `Pass`
            │   │   │           └── If `Attendance_Rate` > `84.3677`: Predict `Fail`
            │   │   └── If `Internet_Access_at_Home` = `Yes`: Predict `Fail`
            │   └── If `Past_Exam_Scores` > `83.5`:
            │       Split on categorical feature `Parental_Education_Level`
            │       ├── If `Parental_Education_Level` = `Bachelors`:
            │       │   Split on `Attendance_Rate` at `83.0537`
            │       │   ├── If `Attendance_Rate` <= `83.0537`: Predict `Fail`
            │       │   └── If `Attendance_Rate` > `83.0537`:
            │       │       Split on categorical feature `Gender`
            │       │       ├── If `Gender` = `Female`: Predict `Pass`
            │       │       └── If `Gender` = `Male`:
            │       │           Split on `Study_Hours_per_Week` at `21.5`
            │       │           ├── If `Study_Hours_per_Week` <= `21.5`: Predict `Pass`
            │       │           └── If `Study_Hours_per_Week` > `21.5`: Predict `Fail`
            │       ├── If `Parental_Education_Level` = `High School`: Predict `Pass`
            │       ├── If `Parental_Education_Level` = `Masters`: Predict `Pass`
            │       └── If `Parental_Education_Level` = `PhD`: Predict `Fail`
            └── If `Study_Hours_per_Week` > `27.5`:
                Split on `Attendance_Rate` at `80.8939`
                ├── If `Attendance_Rate` <= `80.8939`:
                │   Split on categorical feature `Parental_Education_Level`
                │   ├── If `Parental_Education_Level` = `Bachelors`: Predict `Fail`
                │   ├── If `Parental_Education_Level` = `High School`:
                │   │   Split on `Study_Hours_per_Week` at `34.5`
                │   │   ├── If `Study_Hours_per_Week` <= `34.5`: Predict `Fail`
                │   │   └── If `Study_Hours_per_Week` > `34.5`: Predict `Pass`
                │   ├── If `Parental_Education_Level` = `Masters`: Predict `Pass`
                │   └── If `Parental_Education_Level` = `PhD`:
                │       Split on `Past_Exam_Scores` at `77.5`
                │       ├── If `Past_Exam_Scores` <= `77.5`: Predict `Pass`
                │       └── If `Past_Exam_Scores` > `77.5`:
                │           Split on `Attendance_Rate` at `78.1152`
                │           ├── If `Attendance_Rate` <= `78.1152`:
                │           │   Split on `Past_Exam_Scores` at `80`
                │           │   ├── If `Past_Exam_Scores` <= `80`: Predict `Fail`
                │           │   └── If `Past_Exam_Scores` > `80`: Predict `Pass`
                │           └── If `Attendance_Rate` > `78.1152`: Predict `Fail`
                └── If `Attendance_Rate` > `80.8939`:
                    Split on categorical feature `Parental_Education_Level`
                    ├── If `Parental_Education_Level` = `Bachelors`: Predict `Pass`
                    ├── If `Parental_Education_Level` = `High School`:
                    │   Split on `Attendance_Rate` at `89.1347`
                    │   ├── If `Attendance_Rate` <= `89.1347`:
                    │   │   Split on `Study_Hours_per_Week` at `33`
                    │   │   ├── If `Study_Hours_per_Week` <= `33`: Predict `Fail`
                    │   │   └── If `Study_Hours_per_Week` > `33`: Predict `Pass`
                    │   └── If `Attendance_Rate` > `89.1347`: Predict `Pass`
                    ├── If `Parental_Education_Level` = `Masters`: Predict `Pass`
                    └── If `Parental_Education_Level` = `PhD`: Predict `Pass`
```
