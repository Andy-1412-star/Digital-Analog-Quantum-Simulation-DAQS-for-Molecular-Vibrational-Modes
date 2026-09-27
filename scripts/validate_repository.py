"""Run dependency-free structural checks for this repository."""

from __future__ import annotations

import csv
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCAL_PATH = re.compile(r"(?:[A-Za-z]:\\(?:Users|home)\\|/(?:Users|home)/)")
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\((?!https?://|mailto:|#)([^)]+)\)")

EXPECTED_COLUMNS = {
    "double_occupancy_g0.1.txt": 3,
    "double_occupancy_g5.txt": 3,
    "fidelity_g0.1.txt": 5,
    "fidelity_g1.txt": 5,
    "fidelity_g5.txt": 5,
    "total_boson_number_g0.1.txt": 4,
    "total_boson_number_g5.txt": 4,
}

EXPECTED_RESULT_COLUMNS = {
    "dynamics.csv": {
        "time",
        "closed_boson_number",
        "open_boson_number",
        "closed_z0",
        "open_z0",
    },
    "trotter_convergence.csv": {
        "steps",
        "dt",
        "lie_fidelity",
        "lie_infidelity",
        "strang_fidelity",
        "strang_infidelity",
    },
    "cutoff_convergence.csv": {
        "vibrational_levels",
        "hilbert_dimension",
        "boson_number",
        "z0",
    },
}


def check_notebooks(errors: list[str]) -> int:
    paths = sorted((ROOT / "notebooks").rglob("*.ipynb")) + sorted(
        (ROOT / "archive").rglob("*.ipynb")
    )
    for path in paths:
        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"Invalid notebook {path.relative_to(ROOT)}: {exc}")
            continue
        if notebook.get("nbformat") != 4:
            errors.append(f"Unsupported nbformat in {path.relative_to(ROOT)}")
        if not notebook.get("cells"):
            errors.append(f"Notebook has no cells: {path.relative_to(ROOT)}")
        for index, cell in enumerate(notebook.get("cells", [])):
            if not cell.get("id"):
                errors.append(f"Missing cell id in {path.relative_to(ROOT)} cell {index}")
            if cell.get("cell_type") == "code" and (
                cell.get("outputs") or cell.get("execution_count") is not None
            ):
                errors.append(f"Transient output in {path.relative_to(ROOT)} cell {index}")
            source = "".join(cell.get("source", []))
            if LOCAL_PATH.search(source):
                errors.append(f"Local absolute path in {path.relative_to(ROOT)} cell {index}")
    return len(paths)


def check_text_data(errors: list[str]) -> int:
    data_dir = ROOT / "data" / "raw"
    for filename, expected_columns in EXPECTED_COLUMNS.items():
        path = data_dir / filename
        if not path.is_file():
            errors.append(f"Missing data file: {path.relative_to(ROOT)}")
            continue
        rows = 0
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                values = line.split()
                rows += 1
                if len(values) != expected_columns:
                    errors.append(
                        f"{path.relative_to(ROOT)}:{line_number} has {len(values)} columns; expected {expected_columns}"
                    )
                try:
                    [float(value) for value in values]
                except ValueError:
                    errors.append(f"Non-numeric value in {path.relative_to(ROOT)}:{line_number}")
        if rows == 0:
            errors.append(f"No data rows in {path.relative_to(ROOT)}")
    return len(EXPECTED_COLUMNS)


def check_thermal_csv(errors: list[str]) -> None:
    path = ROOT / "data" / "raw" / "thermal_summary.csv"
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    if len(rows) < 2 or not rows[0]:
        errors.append(f"CSV is empty or lacks a header: {path.relative_to(ROOT)}")
    elif any(len(row) != len(rows[0]) for row in rows[1:]):
        errors.append(f"Inconsistent CSV columns: {path.relative_to(ROOT)}")


def check_generated_results(errors: list[str]) -> int:
    result_dir = ROOT / "results"
    for filename, expected_columns in EXPECTED_RESULT_COLUMNS.items():
        path = result_dir / filename
        if not path.is_file():
            errors.append(f"Missing generated result: {path.relative_to(ROOT)}")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if set(reader.fieldnames or []) != expected_columns:
                errors.append(f"Unexpected columns in {path.relative_to(ROOT)}")
                continue
            rows = list(reader)
        if not rows:
            errors.append(f"No result rows in {path.relative_to(ROOT)}")
        for line_number, row in enumerate(rows, start=2):
            try:
                values = [float(value) for value in row.values()]
            except (TypeError, ValueError):
                errors.append(f"Non-numeric result in {path.relative_to(ROOT)}:{line_number}")
                continue
            if not all(math.isfinite(value) for value in values):
                errors.append(f"Non-finite result in {path.relative_to(ROOT)}:{line_number}")

    summary_path = result_dir / "summary.json"
    try:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Invalid generated summary {summary_path.relative_to(ROOT)}: {exc}")
    else:
        if not summary or not all(
            isinstance(value, (int, float)) and math.isfinite(value) for value in summary.values()
        ):
            errors.append(
                f"Generated summary contains invalid values: {summary_path.relative_to(ROOT)}"
            )
    return len(EXPECTED_RESULT_COLUMNS) + 1


def check_markdown_links(errors: list[str]) -> int:
    paths = sorted(ROOT.rglob("*.md"))
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(text):
            target_path = target.split("#", maxsplit=1)[0]
            if target_path and not (path.parent / target_path).resolve().exists():
                errors.append(f"Broken local link in {path.relative_to(ROOT)}: {target}")
    return len(paths)


def main() -> None:
    errors: list[str] = []
    notebook_count = check_notebooks(errors)
    data_count = check_text_data(errors)
    check_thermal_csv(errors)
    result_count = check_generated_results(errors)
    markdown_count = check_markdown_links(errors)

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(
        "Repository validation passed: "
        f"{notebook_count} notebooks, {data_count + 1} source data files, "
        f"{result_count} generated result files, and {markdown_count} Markdown files checked."
    )


if __name__ == "__main__":
    main()
