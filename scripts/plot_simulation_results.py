#!/usr/bin/env python3
"""Plot all 16 simulation comparison cells without asserting real results."""

import csv
import itertools
import math
from plot_style import ROOT, configure_style, plt


SETTINGS = ("pusher", "grabber")
CASES = ("in_domain", "generalization")
REGIMES = ("bc", "cotrain")
METHODS = ("baseline", "arc")
LABELS = {
    "pusher": "Pusher", "grabber": "Grabber",
    "in_domain": "in-domain", "generalization": "generalization",
    "baseline": "Baseline", "arc": "ARC",
}
COLORS = {"baseline": "#84919A", "arc": "#426C93"}


def main():
    with (ROOT / "data/simulation_results.csv").open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    expected = set(itertools.product(SETTINGS, CASES, REGIMES, METHODS))
    keys = [(row["setting"], row["evaluation_case"], row["training_regime"],
             row["method"]) for row in rows]
    if len(keys) != len(expected) or set(keys) != expected:
        raise SystemExit(
            "Simulation data must contain exactly one row for each of the 16 "
            "setting/case/training/method combinations."
        )
    rates = {key: float(row["success_rate_percent"]) for key, row in zip(keys, rows)}
    if any(not math.isfinite(value) or not 0 <= value <= 100 for value in rates.values()):
        raise SystemExit("Simulation success rates must be finite percentages from 0 to 100.")
    flags = [row["is_placeholder"].strip().lower() for row in rows]
    if any(flag not in {"true", "false"} for flag in flags):
        raise SystemExit("Every simulation row must set is_placeholder to true or false.")

    configure_style()
    fig, axes = plt.subplots(2, 2, figsize=(5.5, 4.25), sharey=True)
    fig.subplots_adjust(left=0.105, right=0.99, bottom=0.095, top=0.79,
                        hspace=0.60, wspace=0.18)
    fig.text(0.105, 0.98, "Simulation comparisons", va="top", fontsize=11, weight="bold")
    if any(flag == "true" for flag in flags):
        fig.text(0.105, 0.915, "ILLUSTRATIVE PLACEHOLDER VALUES", va="top",
                 fontsize=8, color="#9B493C")
    for row_index, setting in enumerate(SETTINGS):
        for col_index, case in enumerate(CASES):
            ax = axes[row_index, col_index]
            panel = chr(ord("a") + row_index * 2 + col_index)
            ax.set_title(f"({panel}) {LABELS[setting]} - {LABELS[case]}",
                         fontsize=9, pad=6)
            for method_index, method in enumerate(METHODS):
                positions = [i + (-0.18 if method_index == 0 else 0.18) for i in range(2)]
                values = [rates[(setting, case, regime, method)] for regime in REGIMES]
                bars = ax.bar(positions, values, width=0.31, color=COLORS[method],
                              label=LABELS[method], zorder=3)
                for bar, value in zip(bars, values):
                    ax.text(bar.get_x() + bar.get_width() / 2, value + 2, f"{value:g}",
                            ha="center", va="bottom", fontsize=7.5)
            ax.set_xticks([0, 1], ["BC", "Co-training"])
            ax.set_xlim(-0.65, 1.65)
            ax.set_ylim(0, 100)
            ax.set_yticks([0, 25, 50, 75, 100])
            if col_index == 0:
                ax.set_ylabel("Success rate (%)", fontsize=8)
            ax.grid(axis="y", color="#E1E5E8", linewidth=0.6, zorder=0)
            ax.spines[["top", "right"]].set_visible(False)
            ax.spines[["bottom", "left"]].set_color("#687580")
            ax.spines[["bottom", "left"]].set_linewidth(0.6)
            ax.tick_params(axis="x", length=0, pad=5, labelsize=8)
            ax.tick_params(axis="y", length=3, color="#687580", labelsize=7.5)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right", bbox_to_anchor=(0.99, 0.99),
               ncol=2, frameon=False, fontsize=8, handlelength=1.2,
               columnspacing=1.2)
    destination = ROOT / "figures"
    destination.mkdir(exist_ok=True)
    fig.savefig(destination / "simulation_comparison.pdf", bbox_inches="tight", pad_inches=0.04)
    fig.savefig(destination / "simulation_comparison.png", dpi=220, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print("Generated simulation_comparison.pdf and .png; validated all 16 comparison cells.")


if __name__ == "__main__":
    main()
