"""Shared typography and runtime setup for the paper's plotting scripts."""

from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Plot dependencies are missing. Install requirements-plots.txt into "
        ".venv and run bash scripts/build_paper.sh."
    ) from exc


ROOT = Path(__file__).resolve().parents[1]


def configure_style():
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "font.size": 9,
        "axes.labelsize": 9,
        "xtick.labelsize": 9,
        "ytick.labelsize": 8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })
