"""Reproduce the fidelity and dynamics figures from the bundled data."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Use a headless backend for normal runs and CI. ``--show`` keeps the user's
# configured interactive backend when the script is launched from a desktop.
if "--show" not in sys.argv:
    plt.switch_backend("Agg")


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = ROOT / "data" / "raw"
DEFAULT_OUTPUT_DIR = ROOT / "figures"


def configure_style(use_tex: bool = False) -> None:
    """Apply a compact publication-style Matplotlib theme."""
    plt.rcParams.update(
        {
            "axes.linewidth": 0.8,
            "font.family": "serif",
            "font.size": 9,
            "mathtext.fontset": "cm",
            "savefig.dpi": 200,
            "text.usetex": use_tex,
            "xtick.major.size": 2.5,
            "xtick.major.width": 0.8,
            "ytick.major.size": 2.5,
            "ytick.major.width": 0.8,
        }
    )
    if use_tex:
        plt.rcParams["text.latex.preamble"] = r"\usepackage{amsmath}\usepackage{amssymb}"


def load_table(data_dir: Path, filename: str, columns: int) -> np.ndarray:
    """Load one data table and fail early if its shape is unexpected."""
    path = data_dir / filename
    data = np.loadtxt(path, comments="#", ndmin=2)
    if data.shape[1] != columns:
        raise ValueError(f"{path} has {data.shape[1]} columns; expected {columns}")
    return data


def plot_fidelity(data_dir: Path) -> plt.Figure:
    """Create the three-panel fidelity comparison (reference Fig. 2)."""
    datasets = [
        ("fidelity_g0.1.txt", r"$g=0.1k$"),
        ("fidelity_g1.txt", r"$g=k$"),
        ("fidelity_g5.txt", r"$g=5k$"),
    ]
    styles = [
        ("DAQC (ideal)", "o", "#d62728"),
        ("DAQC (noisy)", "*", "#111111"),
        ("Digital (ideal)", "^", "#e69f00"),
        ("Digital (noisy)", "H", "#4c78a8"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.2), sharey=True, constrained_layout=True)
    for panel, (ax, (filename, coupling)) in enumerate(zip(axes, datasets, strict=True)):
        data = load_table(data_dir, filename, 5)
        for column, (label, marker, color) in enumerate(styles, start=1):
            ax.plot(
                data[:, 0],
                data[:, column],
                label=label,
                color=color,
                linewidth=0.8,
                marker=marker,
                markersize=3,
            )
        ax.set(xlabel=r"$t\,k$", xlim=(data[:, 0].min(), data[:, 0].max()), ylim=(-0.05, 1.15))
        ax.text(0.04, 0.92, f"{chr(97 + panel)}.", transform=ax.transAxes)
        ax.text(0.62, 0.92, coupling, transform=ax.transAxes)
        ax.grid(alpha=0.18, linewidth=0.5)

    axes[0].set_ylabel("Fidelity")
    axes[0].legend(frameon=False, fontsize=7, handlelength=1.4)
    return fig


def plot_dynamics(data_dir: Path) -> plt.Figure:
    """Create double-occupancy and boson-number panels (reference Fig. 5)."""
    weak_occupancy = load_table(data_dir, "double_occupancy_g0.1.txt", 3)
    strong_occupancy = load_table(data_dir, "double_occupancy_g5.txt", 3)
    weak_bosons = load_table(data_dir, "total_boson_number_g0.1.txt", 4)
    strong_bosons = load_table(data_dir, "total_boson_number_g5.txt", 4)

    fig, axes = plt.subplots(3, 1, figsize=(4.0, 5.4), sharex=True, constrained_layout=True)
    occupancy_styles = [
        (r"$j=1$", "-", "#111111"),
        (r"$j=2$", "--", "#b07c00"),
        ("total", ":", "#3569b7"),
    ]
    for panel, (ax, data, coupling) in enumerate(
        zip(axes[:2], (weak_occupancy, strong_occupancy), (r"$g/k=0.1$", r"$g/k=5$"), strict=True)
    ):
        series = (data[:, 1], data[:, 2], data[:, 1] + data[:, 2])
        for values, (label, linestyle, color) in zip(series, occupancy_styles, strict=True):
            ax.plot(
                data[:, 0], values, label=label, linestyle=linestyle, color=color, linewidth=1.1
            )
        ax.set(ylabel=r"$\langle n_{j\uparrow}n_{j\downarrow}\rangle$", ylim=(-0.05, 1.4))
        ax.text(0.03, 0.84, f"{chr(97 + panel)}.", transform=ax.transAxes)
        ax.text(0.66, 0.84, coupling, transform=ax.transAxes)
        ax.grid(alpha=0.18, linewidth=0.5)

    axes[1].legend(frameon=False, ncol=3, fontsize=7, loc="upper center")
    axes[2].plot(
        weak_bosons[:, 0],
        weak_bosons[:, 1] + weak_bosons[:, 2],
        "--",
        color="#d62728",
        label=r"$g/k=0.1$",
    )
    axes[2].plot(
        strong_bosons[:, 0],
        strong_bosons[:, 1] + strong_bosons[:, 2],
        "-",
        color="#25a9d6",
        label=r"$g/k=5$",
    )
    axes[2].set(
        xlabel=r"$t\,k$",
        ylabel=r"$\langle n_{\mathrm{ph}}\rangle$",
        xlim=(0, 20),
        ylim=(-0.2, 6.75),
    )
    axes[2].text(0.03, 0.84, "c.", transform=axes[2].transAxes)
    axes[2].legend(frameon=False, fontsize=7)
    axes[2].grid(alpha=0.18, linewidth=0.5)
    return fig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--use-tex", action="store_true", help="Render labels with a local LaTeX installation."
    )
    parser.add_argument("--show", action="store_true", help="Display figures after saving them.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configure_style(args.use_tex)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    figures = {
        "figure_2_fidelity.png": plot_fidelity(args.data_dir),
        "figure_5_dynamics.png": plot_dynamics(args.data_dir),
    }
    for filename, figure in figures.items():
        destination = args.output_dir / filename
        figure.savefig(destination, bbox_inches="tight")
        print(f"Wrote {destination}")

    if args.show:
        plt.show()
    else:
        for figure in figures.values():
            plt.close(figure)


if __name__ == "__main__":
    main()
