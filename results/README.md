# Generated results

These files are produced by `python experiments/run_h2_study.py` and are committed so that the main numerical claims can be inspected without rerunning the simulation.

| File | Contents |
| --- | --- |
| `dynamics.csv` | Time, closed/open boson occupation, and closed/open `Z0` expectation |
| `trotter_convergence.csv` | Step size, fidelity, and infidelity for Lie–Trotter and Strang formulas |
| `cutoff_convergence.csv` | Final observables and joint Hilbert-space dimension for each bosonic cutoff |
| `summary.json` | Parameters and headline metrics used to generate `RESULTS.md` |

All times and Hamiltonian parameters are dimensionless in this reference study. The CSV files contain full-precision values; the Markdown report rounds numbers only for readability.

Regenerating the study overwrites these four files and the three `figures/h2_*.png` figures.
