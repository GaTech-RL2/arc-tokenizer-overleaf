#!/usr/bin/env python3
"""Render the four-task figure from editable, explicitly labeled input data."""

import csv
import math
import textwrap
from plot_style import ROOT, configure_style, plt
EXPECTED_TASKS = [
    "sort_stationery", "fold_towels", "earbuds", "vegetables_from_bag"
]


def main():
    with (ROOT / "data/task_results.csv").open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    if [row["task_id"] for row in rows] != EXPECTED_TASKS:
        raise SystemExit("Expected exactly the four paper tasks in their stated order.")
    values = [float(row["success_rate_percent"]) for row in rows]
    if any(not math.isfinite(value) or not 0 <= value <= 100 for value in values):
        raise SystemExit("Success rates must be finite percentages from 0 to 100.")
    flags = [row["is_placeholder"].strip().lower() for row in rows]
    if any(flag not in {"true", "false"} for flag in flags):
        raise SystemExit("Every row must explicitly set is_placeholder to true or false.")
    placeholders = any(flag == "true" for flag in flags)

    configure_style()
    fig, ax = plt.subplots(figsize=(5.5, 2.85))
    fig.subplots_adjust(left=0.13, right=0.985, bottom=0.23, top=0.79)
    fig.text(0.13, 0.965, "Four-task evaluation", va="top", fontsize=11, weight="bold")
    if placeholders:
        fig.text(0.13, 0.89, "ILLUSTRATIVE PLACEHOLDER VALUES", va="top",
                 fontsize=8, color="#9B493C")
    labels = ["\n".join(textwrap.wrap(row["task_label"], width=12)) for row in rows]
    bars = ax.bar(range(4), values, width=0.52, color="#426C93", zorder=3)
    ax.set_xticks(range(4), labels)
    ax.set_ylabel("Task success rate (%)")
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_xlim(-0.55, 3.55)
    ax.grid(axis="y", color="#E1E5E8", linewidth=0.6, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["bottom", "left"]].set_color("#687580")
    ax.spines[["bottom", "left"]].set_linewidth(0.6)
    ax.tick_params(axis="x", length=0, pad=7)
    ax.tick_params(axis="y", length=3, color="#687580")
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 2, f"{value:g}%",
                ha="center", va="bottom", fontsize=9)

    destination = ROOT / "figures"
    destination.mkdir(exist_ok=True)
    fig.savefig(destination / "task_success_rates.pdf", bbox_inches="tight", pad_inches=0.04)
    fig.savefig(destination / "task_success_rates.png", dpi=220, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print("Generated figures/task_success_rates.pdf and .png")


if __name__ == "__main__":
    main()
