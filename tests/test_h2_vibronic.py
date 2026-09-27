from __future__ import annotations

import numpy as np

from daqc import (
    ModelConfig,
    build_model,
    collapse_operators,
    noise_parameter_sweep,
    simulate_closed_open,
    trotter_convergence,
)


def test_model_is_hermitian_and_dimensionally_consistent() -> None:
    model = build_model(ModelConfig(n_vibrational_levels=2))
    assert model.h_total.isherm
    assert model.h_total.shape == (32, 32)
    assert len(model.qubit_hamiltonian.terms) == 19


def test_collapse_operators_share_model_dimensions() -> None:
    model = build_model(ModelConfig(n_vibrational_levels=2))
    operators = collapse_operators(model, t1=5.0, t2=4.0)
    assert len(operators) == 2
    assert all(operator.dims == model.h_total.dims for operator in operators)


def test_closed_open_dynamics_are_finite() -> None:
    results = simulate_closed_open(
        ModelConfig(n_vibrational_levels=2),
        np.linspace(0.0, 1.0, 5),
        t1=5.0,
        t2=4.0,
    )
    for key in ("closed_boson_number", "open_boson_number", "closed_z0", "open_z0"):
        assert np.isfinite(results[key]).all()


def test_product_formula_converges_and_strang_is_more_accurate() -> None:
    rows = trotter_convergence(
        ModelConfig(n_vibrational_levels=2),
        total_time=2.0,
        step_counts=[2, 4, 8],
    )
    assert rows[-1]["lie_infidelity"] < rows[0]["lie_infidelity"]
    assert rows[-1]["strang_infidelity"] < rows[0]["strang_infidelity"]
    assert rows[-1]["strang_infidelity"] < rows[-1]["lie_infidelity"]
    for key in ("lie_boson_number_error", "strang_boson_number_error"):
        assert np.isfinite(rows[-1][key])
        assert rows[-1][key] >= 0.0


def test_noise_sweep_has_exact_zero_noise_reference() -> None:
    rows = noise_parameter_sweep(
        couplings=[0.1, 0.2],
        noise_scales=[0.0, 1.0],
        times=np.linspace(0.0, 1.0, 5),
        n_vibrational_levels=2,
        omega=1.0,
        baseline_t1=5.0,
        baseline_t2=4.0,
    )
    assert len(rows) == 4
    zero_noise_rows = [row for row in rows if row["noise_scale"] == 0.0]
    assert all(row["max_boson_number_separation"] == 0.0 for row in zero_noise_rows)
    assert all(np.isfinite(value) for row in rows for value in row.values())
