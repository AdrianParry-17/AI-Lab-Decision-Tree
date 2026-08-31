# Decision Tree Training Result

## Data and preprocessing

- Source: `data/student_data.csv`
- Training rows: 708
- Target: `Pass_Fail`
- Excluded inputs: `Student_ID` (identifier), `Final_Exam_Score`
- Features (7): `Gender`, `Study_Hours_per_Week`, `Attendance_Rate`, `Past_Exam_Scores`, `Parental_Education_Level`, `Internet_Access_at_Home`, `Extracurricular_Activities`
- Numeric CSV values were converted to `int`/`float`; categorical values remain strings.

## Model summary

- Trainer: custom `CreateAttributeClassificationTrainingStrategy`
- Split objective: weighted Gini impurity
- Stopping rule: make a leaf when all local labels are identical
- Nodes: 221
- Leaves: 121
- Maximum depth: 11
- Training accuracy: 708/708 (100.00%)

The accuracy above is measured on the training data; no holdout evaluation was requested.

## Confusion matrix (training data)

| Actual \ Predicted | Fail | Pass |
| --- | ---: | ---: |
| Fail | 354 | 0 |
| Pass | 0 | 354 |

## Final tree

```text
Split on `Past_Exam_Scores` at `82.5`
├── If `Past_Exam_Scores` <= `82.5`:
│   Split on `Attendance_Rate` at `74.8619`
│   ├── If `Attendance_Rate` <= `74.8619`:
│   │   Split on `Study_Hours_per_Week` at `37.5`
│   │   ├── If `Study_Hours_per_Week` <= `37.5`:
│   │   │   Split on `Attendance_Rate` at `66.918`
│   │   │   ├── If `Attendance_Rate` <= `66.918`: Predict `Fail`
│   │   │   └── If `Attendance_Rate` > `66.918`:
│   │   │       Split on `Attendance_Rate` at `67.0209`
│   │   │       ├── If `Attendance_Rate` <= `67.0209`: Predict `Pass`
│   │   │       └── If `Attendance_Rate` > `67.0209`:
│   │   │           Split on `Study_Hours_per_Week` at `34.5`
│   │   │           ├── If `Study_Hours_per_Week` <= `34.5`:
│   │   │           │   Split on `Attendance_Rate` at `74.1481`
│   │   │           │   ├── If `Attendance_Rate` <= `74.1481`: Predict `Fail`
│   │   │           │   └── If `Attendance_Rate` > `74.1481`:
│   │   │           │       Split on `Attendance_Rate` at `74.2784`
│   │   │           │       ├── If `Attendance_Rate` <= `74.2784`: Predict `Pass`
│   │   │           │       └── If `Attendance_Rate` > `74.2784`: Predict `Fail`
│   │   │           └── If `Study_Hours_per_Week` > `34.5`:
│   │   │               Split on `Past_Exam_Scores` at `71.5`
│   │   │               ├── If `Past_Exam_Scores` <= `71.5`: Predict `Fail`
│   │   │               └── If `Past_Exam_Scores` > `71.5`:
│   │   │                   Split on `Attendance_Rate` at `73.7717`
│   │   │                   ├── If `Attendance_Rate` <= `73.7717`: Predict `Pass`
│   │   │                   └── If `Attendance_Rate` > `73.7717`: Predict `Fail`
│   │   └── If `Study_Hours_per_Week` > `37.5`:
│   │       Split on `Past_Exam_Scores` at `68.5`
│   │       ├── If `Past_Exam_Scores` <= `68.5`: Predict `Fail`
│   │       └── If `Past_Exam_Scores` > `68.5`:
│   │           Split on `Past_Exam_Scores` at `79.5`
│   │           ├── If `Past_Exam_Scores` <= `79.5`: Predict `Pass`
│   │           └── If `Past_Exam_Scores` > `79.5`: Predict `Fail`
│   └── If `Attendance_Rate` > `74.8619`:
│       Split on `Study_Hours_per_Week` at `26.5`
│       ├── If `Study_Hours_per_Week` <= `26.5`:
│       │   Split on `Attendance_Rate` at `93.2628`
│       │   ├── If `Attendance_Rate` <= `93.2628`:
│       │   │   Split on `Past_Exam_Scores` at `79.5`
│       │   │   ├── If `Past_Exam_Scores` <= `79.5`:
│       │   │   │   Split on `Study_Hours_per_Week` at `22.5`
│       │   │   │   ├── If `Study_Hours_per_Week` <= `22.5`: Predict `Fail`
│       │   │   │   └── If `Study_Hours_per_Week` > `22.5`:
│       │   │   │       Split on categorical feature `Parental_Education_Level`
│       │   │   │       ├── If `Parental_Education_Level` = `Bachelors`: Predict `Fail`
│       │   │   │       ├── If `Parental_Education_Level` = `High School`: Predict `Fail`
│       │   │   │       ├── If `Parental_Education_Level` = `Masters`: Predict `Fail`
│       │   │   │       └── If `Parental_Education_Level` = `PhD`:
│       │   │   │           Split on categorical feature `Gender`
│       │   │   │           ├── If `Gender` = `Female`: Predict `Pass`
│       │   │   │           └── If `Gender` = `Male`: Predict `Fail`
│       │   │   └── If `Past_Exam_Scores` > `79.5`:
│       │   │       Split on categorical feature `Parental_Education_Level`
│       │   │       ├── If `Parental_Education_Level` = `Bachelors`: Predict `Pass`
│       │   │       ├── If `Parental_Education_Level` = `High School`:
│       │   │       │   Split on `Study_Hours_per_Week` at `18.5`
│       │   │       │   ├── If `Study_Hours_per_Week` <= `18.5`: Predict `Pass`
│       │   │       │   └── If `Study_Hours_per_Week` > `18.5`: Predict `Fail`
│       │   │       └── If `Parental_Education_Level` = `PhD`: Predict `Fail`
│       │   └── If `Attendance_Rate` > `93.2628`:
│       │       Split on `Attendance_Rate` at `96.2691`
│       │       ├── If `Attendance_Rate` <= `96.2691`:
│       │       │   Split on `Past_Exam_Scores` at `67.5`
│       │       │   ├── If `Past_Exam_Scores` <= `67.5`:
│       │       │   │   Split on `Attendance_Rate` at `95.5289`
│       │       │   │   ├── If `Attendance_Rate` <= `95.5289`: Predict `Fail`
│       │       │   │   └── If `Attendance_Rate` > `95.5289`:
│       │       │   │       Split on `Study_Hours_per_Week` at `21.5`
│       │       │   │       ├── If `Study_Hours_per_Week` <= `21.5`: Predict `Pass`
│       │       │   │       └── If `Study_Hours_per_Week` > `21.5`: Predict `Fail`
│       │       │   └── If `Past_Exam_Scores` > `67.5`:
│       │       │       Split on `Past_Exam_Scores` at `78.5`
│       │       │       ├── If `Past_Exam_Scores` <= `78.5`: Predict `Pass`
│       │       │       └── If `Past_Exam_Scores` > `78.5`: Predict `Fail`
│       │       └── If `Attendance_Rate` > `96.2691`:
│       │           Split on `Attendance_Rate` at `99.1297`
│       │           ├── If `Attendance_Rate` <= `99.1297`: Predict `Fail`
│       │           └── If `Attendance_Rate` > `99.1297`:
│       │               Split on categorical feature `Gender`
│       │               ├── If `Gender` = `Female`: Predict `Pass`
│       │               └── If `Gender` = `Male`: Predict `Fail`
│       └── If `Study_Hours_per_Week` > `26.5`:
│           Split on `Past_Exam_Scores` at `58`
│           ├── If `Past_Exam_Scores` <= `58`:
│           │   Split on categorical feature `Parental_Education_Level`
│           │   ├── If `Parental_Education_Level` = `Bachelors`: Predict `Fail`
│           │   ├── If `Parental_Education_Level` = `High School`: Predict `Fail`
│           │   ├── If `Parental_Education_Level` = `Masters`: Predict `Fail`
│           │   └── If `Parental_Education_Level` = `PhD`:
│           │       Split on `Attendance_Rate` at `91.9382`
│           │       ├── If `Attendance_Rate` <= `91.9382`:
│           │       │   Split on `Study_Hours_per_Week` at `35.5`
│           │       │   ├── If `Study_Hours_per_Week` <= `35.5`: Predict `Fail`
│           │       │   └── If `Study_Hours_per_Week` > `35.5`:
│           │       │       Split on categorical feature `Gender`
│           │       │       ├── If `Gender` = `Female`: Predict `Pass`
│           │       │       └── If `Gender` = `Male`: Predict `Fail`
│           │       └── If `Attendance_Rate` > `91.9382`: Predict `Pass`
│           └── If `Past_Exam_Scores` > `58`:
│               Split on `Attendance_Rate` at `89.2645`
│               ├── If `Attendance_Rate` <= `89.2645`:
│               │   Split on `Study_Hours_per_Week` at `34.5`
│               │   ├── If `Study_Hours_per_Week` <= `34.5`:
│               │   │   Split on `Past_Exam_Scores` at `72.5`
│               │   │   ├── If `Past_Exam_Scores` <= `72.5`:
│               │   │   │   Split on categorical feature `Parental_Education_Level`
│               │   │   │   ├── If `Parental_Education_Level` = `Bachelors`:
│               │   │   │   │   Split on categorical feature `Extracurricular_Activities`
│               │   │   │   │   ├── If `Extracurricular_Activities` = `No`: Predict `Fail`
│               │   │   │   │   └── If `Extracurricular_Activities` = `Yes`:
│               │   │   │   │       Split on categorical feature `Gender`
│               │   │   │   │       ├── If `Gender` = `Female`: Predict `Fail`
│               │   │   │   │       └── If `Gender` = `Male`: Predict `Pass`
│               │   │   │   ├── If `Parental_Education_Level` = `Masters`: Predict `Fail`
│               │   │   │   └── If `Parental_Education_Level` = `PhD`:
│               │   │   │       Split on categorical feature `Gender`
│               │   │   │       ├── If `Gender` = `Female`: Predict `Fail`
│               │   │   │       └── If `Gender` = `Male`: Predict `Pass`
│               │   │   └── If `Past_Exam_Scores` > `72.5`:
│               │   │       Split on categorical feature `Parental_Education_Level`
│               │   │       ├── If `Parental_Education_Level` = `Bachelors`:
│               │   │       │   Split on categorical feature `Gender`
│               │   │       │   ├── If `Gender` = `Female`: Predict `Pass`
│               │   │       │   └── If `Gender` = `Male`: Predict `Fail`
│               │   │       ├── If `Parental_Education_Level` = `High School`: Predict `Fail`
│               │   │       ├── If `Parental_Education_Level` = `Masters`:
│               │   │       │   Split on `Study_Hours_per_Week` at `28`
│               │   │       │   ├── If `Study_Hours_per_Week` <= `28`: Predict `Fail`
│               │   │       │   └── If `Study_Hours_per_Week` > `28`:
│               │   │       │       Split on `Study_Hours_per_Week` at `33.5`
│               │   │       │       ├── If `Study_Hours_per_Week` <= `33.5`: Predict `Pass`
│               │   │       │       └── If `Study_Hours_per_Week` > `33.5`: Predict `Fail`
│               │   │       └── If `Parental_Education_Level` = `PhD`: Predict `Pass`
│               │   └── If `Study_Hours_per_Week` > `34.5`:
│               │       Split on `Past_Exam_Scores` at `68.5`
│               │       ├── If `Past_Exam_Scores` <= `68.5`:
│               │       │   Split on `Attendance_Rate` at `86.0586`
│               │       │   ├── If `Attendance_Rate` <= `86.0586`:
│               │       │   │   Split on `Attendance_Rate` at `76.986`
│               │       │   │   ├── If `Attendance_Rate` <= `76.986`: Predict `Pass`
│               │       │   │   └── If `Attendance_Rate` > `76.986`:
│               │       │   │       Split on categorical feature `Parental_Education_Level`
│               │       │   │       ├── If `Parental_Education_Level` = `Bachelors`: Predict `Fail`
│               │       │   │       ├── If `Parental_Education_Level` = `High School`:
│               │       │   │       │   Split on `Study_Hours_per_Week` at `37.5`
│               │       │   │       │   ├── If `Study_Hours_per_Week` <= `37.5`: Predict `Pass`
│               │       │   │       │   └── If `Study_Hours_per_Week` > `37.5`: Predict `Fail`
│               │       │   │       ├── If `Parental_Education_Level` = `Masters`: Predict `Fail`
│               │       │   │       └── If `Parental_Education_Level` = `PhD`:
│               │       │   │           Split on categorical feature `Gender`
│               │       │   │           ├── If `Gender` = `Female`: Predict `Fail`
│               │       │   │           └── If `Gender` = `Male`: Predict `Pass`
│               │       │   └── If `Attendance_Rate` > `86.0586`: Predict `Fail`
│               │       └── If `Past_Exam_Scores` > `68.5`:
│               │           Split on `Past_Exam_Scores` at `77.5`
│               │           ├── If `Past_Exam_Scores` <= `77.5`: Predict `Pass`
│               │           └── If `Past_Exam_Scores` > `77.5`:
│               │               Split on `Past_Exam_Scores` at `80`
│               │               ├── If `Past_Exam_Scores` <= `80`: Predict `Fail`
│               │               └── If `Past_Exam_Scores` > `80`: Predict `Pass`
│               └── If `Attendance_Rate` > `89.2645`:
│                   Split on `Past_Exam_Scores` at `62`
│                   ├── If `Past_Exam_Scores` <= `62`:
│                   │   Split on `Study_Hours_per_Week` at `33.5`
│                   │   ├── If `Study_Hours_per_Week` <= `33.5`: Predict `Fail`
│                   │   └── If `Study_Hours_per_Week` > `33.5`: Predict `Pass`
│                   └── If `Past_Exam_Scores` > `62`:
│                       Split on `Attendance_Rate` at `97.3003`
│                       ├── If `Attendance_Rate` <= `97.3003`: Predict `Pass`
│                       └── If `Attendance_Rate` > `97.3003`:
│                           Split on `Attendance_Rate` at `98.1762`
│                           ├── If `Attendance_Rate` <= `98.1762`: Predict `Fail`
│                           └── If `Attendance_Rate` > `98.1762`: Predict `Pass`
└── If `Past_Exam_Scores` > `82.5`:
    Split on `Attendance_Rate` at `77.5109`
    ├── If `Attendance_Rate` <= `77.5109`:
    │   Split on `Study_Hours_per_Week` at `19`
    │   ├── If `Study_Hours_per_Week` <= `19`:
    │   │   Split on `Past_Exam_Scores` at `95.5`
    │   │   ├── If `Past_Exam_Scores` <= `95.5`: Predict `Fail`
    │   │   └── If `Past_Exam_Scores` > `95.5`:
    │   │       Split on categorical feature `Parental_Education_Level`
    │   │       ├── If `Parental_Education_Level` = `Bachelors`: Predict `Fail`
    │   │       ├── If `Parental_Education_Level` = `High School`: Predict `Fail`
    │   │       ├── If `Parental_Education_Level` = `Masters`: Predict `Pass`
    │   │       └── If `Parental_Education_Level` = `PhD`: Predict `Fail`
    │   └── If `Study_Hours_per_Week` > `19`:
    │       Split on `Attendance_Rate` at `58.6596`
    │       ├── If `Attendance_Rate` <= `58.6596`:
    │       │   Split on categorical feature `Extracurricular_Activities`
    │       │   ├── If `Extracurricular_Activities` = `No`:
    │       │   │   Split on `Study_Hours_per_Week` at `29.5`
    │       │   │   ├── If `Study_Hours_per_Week` <= `29.5`: Predict `Fail`
    │       │   │   └── If `Study_Hours_per_Week` > `29.5`:
    │       │   │       Split on `Attendance_Rate` at `55.5391`
    │       │   │       ├── If `Attendance_Rate` <= `55.5391`:
    │       │   │       │   Split on `Past_Exam_Scores` at `98.5`
    │       │   │       │   ├── If `Past_Exam_Scores` <= `98.5`: Predict `Pass`
    │       │   │       │   └── If `Past_Exam_Scores` > `98.5`: Predict `Fail`
    │       │   │       └── If `Attendance_Rate` > `55.5391`: Predict `Fail`
    │       │   └── If `Extracurricular_Activities` = `Yes`: Predict `Fail`
    │       └── If `Attendance_Rate` > `58.6596`:
    │           Split on `Attendance_Rate` at `69.3722`
    │           ├── If `Attendance_Rate` <= `69.3722`:
    │           │   Split on `Past_Exam_Scores` at `91.5`
    │           │   ├── If `Past_Exam_Scores` <= `91.5`:
    │           │   │   Split on categorical feature `Gender`
    │           │   │   ├── If `Gender` = `Female`: Predict `Fail`
    │           │   │   └── If `Gender` = `Male`:
    │           │   │       Split on `Study_Hours_per_Week` at `29`
    │           │   │       ├── If `Study_Hours_per_Week` <= `29`:
    │           │   │       │   Split on `Study_Hours_per_Week` at `26.5`
    │           │   │       │   ├── If `Study_Hours_per_Week` <= `26.5`: Predict `Pass`
    │           │   │       │   └── If `Study_Hours_per_Week` > `26.5`: Predict `Fail`
    │           │   │       └── If `Study_Hours_per_Week` > `29`: Predict `Pass`
    │           │   └── If `Past_Exam_Scores` > `91.5`:
    │           │       Split on `Study_Hours_per_Week` at `38.5`
    │           │       ├── If `Study_Hours_per_Week` <= `38.5`:
    │           │       │   Split on categorical feature `Parental_Education_Level`
    │           │       │   ├── If `Parental_Education_Level` = `Bachelors`: Predict `Pass`
    │           │       │   ├── If `Parental_Education_Level` = `High School`: Predict `Pass`
    │           │       │   ├── If `Parental_Education_Level` = `Masters`:
    │           │       │   │   Split on categorical feature `Gender`
    │           │       │   │   ├── If `Gender` = `Female`: Predict `Pass`
    │           │       │   │   └── If `Gender` = `Male`: Predict `Fail`
    │           │       │   └── If `Parental_Education_Level` = `PhD`: Predict `Pass`
    │           │       └── If `Study_Hours_per_Week` > `38.5`:
    │           │           Split on categorical feature `Gender`
    │           │           ├── If `Gender` = `Female`: Predict `Pass`
    │           │           └── If `Gender` = `Male`: Predict `Fail`
    │           └── If `Attendance_Rate` > `69.3722`:
    │               Split on categorical feature `Parental_Education_Level`
    │               ├── If `Parental_Education_Level` = `Bachelors`: Predict `Fail`
    │               ├── If `Parental_Education_Level` = `High School`:
    │               │   Split on `Past_Exam_Scores` at `87`
    │               │   ├── If `Past_Exam_Scores` <= `87`: Predict `Fail`
    │               │   └── If `Past_Exam_Scores` > `87`:
    │               │       Split on categorical feature `Gender`
    │               │       ├── If `Gender` = `Female`: Predict `Fail`
    │               │       └── If `Gender` = `Male`:
    │               │           Split on `Attendance_Rate` at `71.5198`
    │               │           ├── If `Attendance_Rate` <= `71.5198`: Predict `Fail`
    │               │           └── If `Attendance_Rate` > `71.5198`: Predict `Pass`
    │               ├── If `Parental_Education_Level` = `Masters`:
    │               │   Split on `Attendance_Rate` at `72.5718`
    │               │   ├── If `Attendance_Rate` <= `72.5718`: Predict `Fail`
    │               │   └── If `Attendance_Rate` > `72.5718`: Predict `Pass`
    │               └── If `Parental_Education_Level` = `PhD`:
    │                   Split on `Attendance_Rate` at `74.0834`
    │                   ├── If `Attendance_Rate` <= `74.0834`:
    │                   │   Split on `Attendance_Rate` at `70.291`
    │                   │   ├── If `Attendance_Rate` <= `70.291`: Predict `Pass`
    │                   │   └── If `Attendance_Rate` > `70.291`: Predict `Fail`
    │                   └── If `Attendance_Rate` > `74.0834`: Predict `Pass`
    └── If `Attendance_Rate` > `77.5109`:
        Split on `Study_Hours_per_Week` at `14.5`
        ├── If `Study_Hours_per_Week` <= `14.5`:
        │   Split on categorical feature `Parental_Education_Level`
        │   ├── If `Parental_Education_Level` = `Bachelors`:
        │   │   Split on `Study_Hours_per_Week` at `12`
        │   │   ├── If `Study_Hours_per_Week` <= `12`:
        │   │   │   Split on `Attendance_Rate` at `81.2133`
        │   │   │   ├── If `Attendance_Rate` <= `81.2133`: Predict `Fail`
        │   │   │   └── If `Attendance_Rate` > `81.2133`: Predict `Pass`
        │   │   └── If `Study_Hours_per_Week` > `12`: Predict `Fail`
        │   ├── If `Parental_Education_Level` = `High School`:
        │   │   Split on categorical feature `Gender`
        │   │   ├── If `Gender` = `Female`:
        │   │   │   Split on `Attendance_Rate` at `88.3793`
        │   │   │   ├── If `Attendance_Rate` <= `88.3793`: Predict `Fail`
        │   │   │   └── If `Attendance_Rate` > `88.3793`: Predict `Pass`
        │   │   └── If `Gender` = `Male`: Predict `Fail`
        │   ├── If `Parental_Education_Level` = `Masters`:
        │   │   Split on `Attendance_Rate` at `81.3413`
        │   │   ├── If `Attendance_Rate` <= `81.3413`: Predict `Fail`
        │   │   └── If `Attendance_Rate` > `81.3413`: Predict `Pass`
        │   └── If `Parental_Education_Level` = `PhD`:
        │       Split on `Study_Hours_per_Week` at `13.5`
        │       ├── If `Study_Hours_per_Week` <= `13.5`: Predict `Fail`
        │       └── If `Study_Hours_per_Week` > `13.5`: Predict `Pass`
        └── If `Study_Hours_per_Week` > `14.5`:
            Split on categorical feature `Parental_Education_Level`
            ├── If `Parental_Education_Level` = `Bachelors`:
            │   Split on `Attendance_Rate` at `81.4143`
            │   ├── If `Attendance_Rate` <= `81.4143`: Predict `Fail`
            │   └── If `Attendance_Rate` > `81.4143`:
            │       Split on `Past_Exam_Scores` at `83.5`
            │       ├── If `Past_Exam_Scores` <= `83.5`: Predict `Fail`
            │       └── If `Past_Exam_Scores` > `83.5`:
            │           Split on `Past_Exam_Scores` at `88.5`
            │           ├── If `Past_Exam_Scores` <= `88.5`:
            │           │   Split on categorical feature `Gender`
            │           │   ├── If `Gender` = `Female`: Predict `Pass`
            │           │   └── If `Gender` = `Male`: Predict `Fail`
            │           └── If `Past_Exam_Scores` > `88.5`: Predict `Pass`
            ├── If `Parental_Education_Level` = `High School`: Predict `Pass`
            ├── If `Parental_Education_Level` = `Masters`:
            │   Split on `Attendance_Rate` at `82.3474`
            │   ├── If `Attendance_Rate` <= `82.3474`:
            │   │   Split on `Attendance_Rate` at `79.4812`
            │   │   ├── If `Attendance_Rate` <= `79.4812`: Predict `Pass`
            │   │   └── If `Attendance_Rate` > `79.4812`: Predict `Fail`
            │   └── If `Attendance_Rate` > `82.3474`: Predict `Pass`
            └── If `Parental_Education_Level` = `PhD`:
                Split on `Past_Exam_Scores` at `88.5`
                ├── If `Past_Exam_Scores` <= `88.5`:
                │   Split on `Study_Hours_per_Week` at `28.5`
                │   ├── If `Study_Hours_per_Week` <= `28.5`: Predict `Fail`
                │   └── If `Study_Hours_per_Week` > `28.5`:
                │       Split on categorical feature `Gender`
                │       ├── If `Gender` = `Female`: Predict `Fail`
                │       └── If `Gender` = `Male`: Predict `Pass`
                └── If `Past_Exam_Scores` > `88.5`:
                    Split on categorical feature `Gender`
                    ├── If `Gender` = `Female`: Predict `Pass`
                    └── If `Gender` = `Male`:
                        Split on `Study_Hours_per_Week` at `23.5`
                        ├── If `Study_Hours_per_Week` <= `23.5`: Predict `Pass`
                        └── If `Study_Hours_per_Week` > `23.5`: Predict `Fail`
```
