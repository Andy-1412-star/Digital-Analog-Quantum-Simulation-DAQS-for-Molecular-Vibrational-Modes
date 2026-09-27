# Generated results

These files are produced by `python experiments/run_h2_study.py` and are committed so that the main numerical claims can be inspected without rerunning the simulation.

| File | Contents |
| --- | --- |
| `dynamics.csv` | Time, closed/open boson occupation, and closed/open `Z0` expectation |
| `trotter_convergence.csv` | Step size, fidelity, infidelity, and final boson-number error for Lie–Trotter and Strang formulas |
| `cutoff_convergence.csv` | Final observables and joint Hilbert-space dimension for each bosonic cutoff |
| `noise_sweep.csv` | Coupling/noise grid, physical rates, final observables, and maximum trajectory separation |
| `error_budget.csv` | Baseline noise, product-formula, and truncation errors on a common final-observable scale |
| `summary.json` | Parameters and headline metrics used to generate `RESULTS.md` |

All times and Hamiltonian parameters are dimensionless in this reference study. The CSV files contain full-precision values; the Markdown report rounds numbers only for readability.

Regenerating the study overwrites these six files and the five `figures/h2_*.png` figures.
