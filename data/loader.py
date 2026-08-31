"""Load the student CSV into the decision-tree library's data objects."""

from __future__ import annotations

import csv
from pathlib import Path

from model.data.supervised import ValueSupervisedData


ID_COLUMN = "Student_ID"
TARGET_COLUMN = "Pass_Fail"
EXCLUDED_FEATURE_COLUMNS = {ID_COLUMN, "Final_Exam_Score"}
INTEGER_COLUMNS = {
    "Study_Hours_per_Week",
    "Past_Exam_Scores",
}
FLOAT_COLUMNS = {"Attendance_Rate"}

FeatureValue = str | int | float
ModelInput = list[tuple[str, FeatureValue]]
TrainingExample = ValueSupervisedData[ModelInput, str]


def _parse_feature(name: str, raw_value: str | None) -> FeatureValue:
    """Convert numeric fields while preserving categorical strings."""
    if raw_value is None:
        raise ValueError(f"Missing value in feature {name!r}")

    value = raw_value.strip()
    if value == "":
        raise ValueError(f"Missing value in feature {name!r}")
    if name in INTEGER_COLUMNS:
        return int(value)
    if name in FLOAT_COLUMNS:
        return float(value)
    return value


def load_data(path: str | Path) -> tuple[list[TrainingExample], list[str]]:
    """Load, validate, and convert the student data from ``path``."""
    data_path = Path(path)

    with data_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None:
            raise ValueError(f"{data_path} has no CSV header")

        required_columns = {ID_COLUMN, TARGET_COLUMN}
        missing_columns = required_columns.difference(reader.fieldnames)
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"CSV is missing required column(s): {missing}")

        feature_names = [
            name
            for name in reader.fieldnames
            if name not in EXCLUDED_FEATURE_COLUMNS | {TARGET_COLUMN}
        ]
        if not feature_names:
            raise ValueError(f"{data_path} has no usable feature columns")

        examples: list[TrainingExample] = []
        for line_number, row in enumerate(reader, start=2):
            try:
                inputs = [
                    (name, _parse_feature(name, row.get(name)))
                    for name in feature_names
                ]
                raw_output = row.get(TARGET_COLUMN)
                output = "" if raw_output is None else raw_output.strip()
                if output == "":
                    raise ValueError(f"Missing target {TARGET_COLUMN!r}")
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"Invalid data on CSV line {line_number}: {error}"
                ) from error

            examples.append(ValueSupervisedData(inputs, output))

    if not examples:
        raise ValueError(f"{data_path} contains no data rows")

    return examples, feature_names
