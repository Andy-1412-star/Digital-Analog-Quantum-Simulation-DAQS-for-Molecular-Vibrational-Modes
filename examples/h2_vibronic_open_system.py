"""Run the compact closed/open-system H2-reference demonstration."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from daqc import ModelConfig, simulate_closed_open


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "figures"

if "--show" not in sys.argv:
    plt.switch_backend("Agg")


def plot_results(results) -> plt.Figure:
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.1), constrained_layout=True)
    series = (
        ("closed_boson_number", "open_boson_number", r"$\langle a^\dagger a\rangle$"),
        ("closed_z0", "open_z0", r"$\langle Z_0\rangle$"),
    )
    for ax, (closed_key, open_key, ylabel) in zip(axes, series, strict=True):
        ax.plot(results["time"], results[closed_key], label="closed", color="#3569b7")
        ax.plot(
            results["time"],
            results[open_key],
            label="open",
            color="#d62728",
            linestyle="--",
        )
        ax.set(xlabel="time", ylabel=ylabel)
        ax.grid(alpha=0.2)
    axes[0].legend(frameon=False)
    return fig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vibrational-levels", type=int, default=2)
    parser.add_argument("--omega", type=float, default=1.0)
    parser.add_argument("--coupling", type=float, default=0.15)
    parser.add_argument("--t1", type=float, default=5.0)
    parser.add_argument("--t2", type=float, default=4.0)
    parser.add_argument("--stop-time", type=float, default=6.0)
    parser.add_argument("--time-points", type=int, default=60)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--show", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = ModelConfig(
        n_vibrational_levels=args.vibrational_levels,
        omega=args.omega,
        coupling=args.coupling,
    )
    results = simulate_closed_open(
        config,
        np.linspace(0.0, args.stop_time, args.time_points),
        t1=args.t1,
        t2=args.t2,
    )
    figure = plot_results(results)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    destination = args.output_dir / "h2_closed_open_dynamics.png"
    figure.savefig(destination, dpi=200, bbox_inches="tight")
    print("Simulation diagnostics:")
    for key in ("pauli_terms", "hilbert_dimension", "collapse_operators"):
        print(f"  {key}: {results[key]}")
    print(f"Wrote {destination}")
    if args.show:
        plt.show()
    else:
        plt.close(figure)


if __name__ == "__main__":
    main()
