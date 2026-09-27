"""Run the complete H2-reference noise, Trotter, and cutoff study."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import NullFormatter

from daqc import ModelConfig, cutoff_observables, simulate_closed_open, trotter_convergence

ROOT = Path(__file__).resolve().parents[1]

if "--show" not in sys.argv:
    plt.switch_backend("Agg")


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def empirical_slope(rows: list[dict], key: str) -> float:
    x = np.asarray([row["steps"] for row in rows], dtype=float)
    y = np.asarray([row[key] for row in rows], dtype=float)
    mask = y > 1e-14
    if mask.sum() < 2:
        return float("nan")
    return float(np.polyfit(np.log(x[mask]), np.log(y[mask]), 1)[0])


def dynamics_rows(results: dict) -> list[dict[str, float]]:
    keys = ("time", "closed_boson_number", "open_boson_number", "closed_z0", "open_z0")
    return [
        {key: float(np.real(results[key][index])) for key in keys}
        for index in range(len(results["time"]))
    ]


def plot_dynamics(rows: list[dict], destination: Path) -> None:
    time = np.asarray([row["time"] for row in rows])
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.1), constrained_layout=True)
    for ax, stem, ylabel in (
        (axes[0], "boson_number", r"$\langle a^\dagger a\rangle$"),
        (axes[1], "z0", r"$\langle Z_0\rangle$"),
    ):
        ax.plot(time, [row[f"closed_{stem}"] for row in rows], label="closed", color="#3569b7")
        ax.plot(
            time,
            [row[f"open_{stem}"] for row in rows],
            label="open",
            color="#d62728",
            linestyle="--",
        )
        ax.set(xlabel="time", ylabel=ylabel)
        ax.grid(alpha=0.2)
    axes[0].legend(frameon=False)
    fig.savefig(destination, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_trotter(rows: list[dict], destination: Path) -> None:
    steps = np.asarray([row["steps"] for row in rows])
    fig, ax = plt.subplots(figsize=(4.5, 3.3), constrained_layout=True)
    ax.loglog(steps, [row["lie_infidelity"] for row in rows], "o-", label="Lie–Trotter")
    ax.loglog(steps, [row["strang_infidelity"] for row in rows], "s--", label="Strang")
    ax.set(xlabel="product-formula steps", ylabel="final-state infidelity")
    ax.set_xticks(steps, [str(step) for step in steps])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.grid(True, which="both", alpha=0.2)
    ax.legend(frameon=False)
    fig.savefig(destination, dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_cutoff(rows: list[dict], destination: Path) -> None:
    levels = [row["vibrational_levels"] for row in rows]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), constrained_layout=True)
    axes[0].plot(levels, [row["boson_number"] for row in rows], "o-")
    axes[0].set(xlabel="vibrational cutoff", ylabel=r"final $\langle a^\dagger a\rangle$")
    axes[1].plot(levels, [row["z0"] for row in rows], "o-", color="#b07c00")
    axes[1].set(xlabel="vibrational cutoff", ylabel=r"final $\langle Z_0\rangle$")
    for ax in axes:
        ax.grid(alpha=0.2)
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    fig.savefig(destination, dpi=200, bbox_inches="tight")
    plt.close(fig)


def write_results_markdown(path: Path, summary: dict) -> None:
    path.write_text(
        f"""# Results: H₂-reference vibronic DAQS study

This study asks how Lindblad noise, product-formula order, and bosonic truncation affect a four-qubit H₂-reference electron–vibration simulation. The coefficients are manually supplied reference values; the study evaluates the numerical workflow, not ab-initio chemical accuracy.

## Configuration

- Bravyi–Kitaev Pauli terms: **{summary["pauli_terms"]}**
- Joint Hilbert-space dimension: **{summary["hilbert_dimension"]}**
- Vibrational cutoff: **{summary["vibrational_levels"]}**
- Coupling: **{summary["coupling"]}**; mode frequency: **{summary["omega"]}**
- Open-system parameters: **T1 = {summary["t1"]}**, **T2 = {summary["t2"]}**
- Evolution interval: **0–{summary["total_time"]}**

## Main findings

1. Vibrational damping and dephasing reduced the final boson occupation from **{summary["final_closed_boson_number"]:.6f}** to **{summary["final_open_boson_number"]:.6f}** (**{summary["final_boson_reduction_percent"]:.1f}%**). The maximum closed/open boson-number separation over the trajectory was **{summary["max_boson_number_separation"]:.6f}**.
2. At **{summary["largest_trotter_steps"]}** product-formula steps, Lie–Trotter infidelity was **{summary["lie_infidelity_at_largest_steps"]:.3e}**, while Strang infidelity was **{summary["strang_infidelity_at_largest_steps"]:.3e}**.
3. The empirical log–log infidelity slopes versus step count were **{summary["lie_empirical_slope"]:.3f}** (Lie) and **{summary["strang_empirical_slope"]:.3f}** (Strang), consistent with the expected `steps^-2` and `steps^-4` infidelity scaling for this test.
4. Increasing the bosonic cutoff from **{summary["minimum_cutoff"]}** to **{summary["maximum_cutoff"]}** changed the final boson occupation by **{summary["cutoff_boson_number_change"]:.3e}**. More importantly for convergence, the change between the final two cutoffs was only **{summary["last_cutoff_boson_number_change"]:.3e}** (and **{summary["last_cutoff_z0_change"]:.3e}** for `Z0`).

## Figures

![Closed and open dynamics](figures/h2_closed_open_dynamics.png)

![Product-formula convergence](figures/h2_trotter_convergence.png)

![Bosonic cutoff convergence](figures/h2_cutoff_convergence.png)

## Reproduce

```bash
python -m pip install -e .
python experiments/run_h2_study.py
```

Machine-readable outputs and their column definitions are stored in [`results/`](results/README.md). Re-run after changing model parameters; do not compare cutoffs or product-formula orders without regenerating the corresponding CSV files.
""",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", type=Path, default=ROOT / "results")
    parser.add_argument("--figure-dir", type=Path, default=ROOT / "figures")
    parser.add_argument("--quick", action="store_true", help="Use a reduced CI smoke-test grid.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.results_dir.mkdir(parents=True, exist_ok=True)
    args.figure_dir.mkdir(parents=True, exist_ok=True)

    if args.quick:
        cutoff, time_points = 2, 21
        step_counts, cutoff_levels = [4, 8], [2, 3]
    else:
        cutoff, time_points = 3, 81
        step_counts, cutoff_levels = [4, 8, 16, 32, 64], [2, 3, 4, 5]

    total_time, omega, coupling, t1, t2 = 6.0, 1.0, 0.15, 5.0, 4.0
    config = ModelConfig(
        n_vibrational_levels=cutoff,
        omega=omega,
        coupling=coupling,
    )
    dynamics = simulate_closed_open(
        config,
        np.linspace(0.0, total_time, time_points),
        t1=t1,
        t2=t2,
    )
    dynamic_rows = dynamics_rows(dynamics)
    trotter_rows = trotter_convergence(config, total_time, step_counts)
    cutoff_rows = cutoff_observables(
        cutoff_levels,
        omega=omega,
        coupling=coupling,
        final_time=total_time,
    )

    write_csv(args.results_dir / "dynamics.csv", dynamic_rows)
    write_csv(args.results_dir / "trotter_convergence.csv", trotter_rows)
    write_csv(args.results_dir / "cutoff_convergence.csv", cutoff_rows)
    plot_dynamics(dynamic_rows, args.figure_dir / "h2_closed_open_dynamics.png")
    plot_trotter(trotter_rows, args.figure_dir / "h2_trotter_convergence.png")
    plot_cutoff(cutoff_rows, args.figure_dir / "h2_cutoff_convergence.png")

    summary = {
        "pauli_terms": dynamics["pauli_terms"],
        "hilbert_dimension": dynamics["hilbert_dimension"],
        "vibrational_levels": cutoff,
        "omega": omega,
        "coupling": coupling,
        "t1": t1,
        "t2": t2,
        "total_time": total_time,
        "final_closed_boson_number": dynamic_rows[-1]["closed_boson_number"],
        "final_open_boson_number": dynamic_rows[-1]["open_boson_number"],
        "final_boson_reduction_percent": 100.0
        * (dynamic_rows[-1]["closed_boson_number"] - dynamic_rows[-1]["open_boson_number"])
        / dynamic_rows[-1]["closed_boson_number"],
        "max_boson_number_separation": max(
            abs(row["closed_boson_number"] - row["open_boson_number"]) for row in dynamic_rows
        ),
        "largest_trotter_steps": trotter_rows[-1]["steps"],
        "lie_infidelity_at_largest_steps": trotter_rows[-1]["lie_infidelity"],
        "strang_infidelity_at_largest_steps": trotter_rows[-1]["strang_infidelity"],
        "lie_empirical_slope": empirical_slope(trotter_rows, "lie_infidelity"),
        "strang_empirical_slope": empirical_slope(trotter_rows, "strang_infidelity"),
        "minimum_cutoff": cutoff_rows[0]["vibrational_levels"],
        "maximum_cutoff": cutoff_rows[-1]["vibrational_levels"],
        "cutoff_boson_number_change": abs(
            cutoff_rows[-1]["boson_number"] - cutoff_rows[0]["boson_number"]
        ),
        "last_cutoff_boson_number_change": abs(
            cutoff_rows[-1]["boson_number"] - cutoff_rows[-2]["boson_number"]
        ),
        "last_cutoff_z0_change": abs(cutoff_rows[-1]["z0"] - cutoff_rows[-2]["z0"]),
    }
    (args.results_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    if not args.quick:
        write_results_markdown(ROOT / "RESULTS.md", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
