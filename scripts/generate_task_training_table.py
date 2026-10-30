#!/usr/bin/env python3
"""Generate the single-task/multi-task table from explicitly labeled data."""

import csv
import itertools
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCOPES = {"single_task": "Single-task", "multi_task": "Multi-task"}
SCORES = ("bc_baseline", "bc_arc", "cotrain_baseline", "cotrain_arc")


def latex_escape(value):
    replacements = {
        "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
        "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}", "\\": r"\textbackslash{}",
    }
    return "".join(replacements.get(char, char) for char in value)


def main():
    with (ROOT / "data/task_results.csv").open(newline="") as stream:
        tasks = list(csv.DictReader(stream))
    task_ids = [row["task_id"] for row in tasks]
    if len(task_ids) != 4 or len(set(task_ids)) != 4:
        raise SystemExit("Expected four distinct tasks in task_results.csv.")
    with (ROOT / "data/task_training_results.csv").open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    keys = [(row["task_id"], row["training_scope"]) for row in rows]
    expected = set(itertools.product(task_ids, SCOPES))
    if len(keys) != len(expected) or set(keys) != expected:
        raise SystemExit("Expected exactly one single-task and one multi-task row per task.")
    table = {key: row for key, row in zip(keys, rows)}
    for row in rows:
        values = [float(row[column]) for column in SCORES]
        if any(not math.isfinite(value) or not 0 <= value <= 100 for value in values):
            raise SystemExit("All 32 table scores must be finite percentages from 0 to 100.")
        if row["is_placeholder"].strip().lower() not in {"true", "false"}:
            raise SystemExit("Every table row must explicitly set is_placeholder.")
    placeholders = any(row["is_placeholder"].strip().lower() == "true" for row in rows)
    caption = (
        r"Single-task and multi-task comparisons across the four tasks. "
        r"Columns report success rates (\%)."
    )
    if placeholders:
        caption += r" All numbers are \textbf{illustrative placeholders}."
    lines = [
        "% Generated from data/task_training_results.csv; edit the CSV, not this file.",
        r"\begin{table}[htbp]",
        r"  \centering",
        "  \\caption{" + caption + "}",
        r"  \label{tab:task-training-comparison}",
        r"  \small",
        r"  \setlength{\tabcolsep}{4pt}",
        r"  \renewcommand{\arraystretch}{1.1}",
        r"  \begin{tabular}{@{}llrrrr@{}}",
        r"    \toprule",
        r"    Task & Training scope & \multicolumn{2}{c}{BC} & \multicolumn{2}{c}{Co-training} \\",
        r"    \cmidrule(lr){3-4}\cmidrule(lr){5-6}",
        r"     & & Baseline & ARC & Baseline & ARC \\",
        r"    \midrule",
    ]
    for index, task in enumerate(tasks):
        for scope_index, (scope, label) in enumerate(SCOPES.items()):
            row = table[(task["task_id"], scope)]
            task_label = latex_escape(task["task_label"]) if scope_index == 0 else ""
            values = [f"{float(row[column]):g}" for column in SCORES]
            lines.append("    " + " & ".join([task_label, label] + values) + r" \\")
        if index < len(tasks) - 1:
            lines.append(r"    \addlinespace[3pt]")
    lines.extend([r"    \bottomrule", r"  \end{tabular}", r"\end{table}"])
    destination = ROOT / "sections/generated/task_training_results_table.tex"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(lines) + "\n")
    print("Generated single-task/multi-task table; validated all 32 scores.")


if __name__ == "__main__":
    main()
