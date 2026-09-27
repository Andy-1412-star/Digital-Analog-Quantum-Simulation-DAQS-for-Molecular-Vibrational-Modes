"""H2-reference electron-vibration model and reproducible experiments.

The module focuses on the numerical workflow rather than ab-initio chemistry:
four-spin-orbital reference coefficients are mapped with OpenFermion and then
coupled to a truncated harmonic mode in QuTiP.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from openfermion.ops import FermionOperator
from openfermion.transforms import bravyi_kitaev
from qutip import Qobj, basis, destroy, expect, mesolve, qeye, sesolve, sigmaz, tensor


@dataclass(frozen=True)
class ModelConfig:
    """Numerical parameters for the single-mode H2-reference model."""

    n_qubits: int = 4
    n_vibrational_levels: int = 3
    omega: float = 1.0
    coupling: float = 0.15

    def validate(self) -> None:
        if self.n_qubits != 4:
            raise ValueError("The supplied electronic Hamiltonian requires exactly four qubits")
        if self.n_vibrational_levels < 2:
            raise ValueError("At least two vibrational levels are required")
        if self.omega <= 0:
            raise ValueError("The vibrational frequency must be positive")
        if self.coupling < 0:
            raise ValueError("The coupling must be non-negative")


@dataclass(frozen=True)
class VibronicModel:
    """Hamiltonian blocks and observables in a shared tensor space."""

    config: ModelConfig
    h_total: Qobj
    h_free: Qobj
    h_interaction: Qobj
    annihilation: Qobj
    number: Qobj
    z0: Qobj
    qubit_hamiltonian: object


H2_TERMS = (
    ("", -0.81261),
    ("0^ 0", -1.25248),
    ("1^ 1", -0.47595),
    ("2^ 2", -0.47595),
    ("3^ 3", -1.25248),
    ("0^ 1^ 1 0", 0.67449),
    ("0^ 2^ 2 0", 0.66458),
    ("0^ 3^ 3 0", 0.18129),
    ("1^ 2^ 2 1", 0.18129),
    ("1^ 3^ 3 1", 0.66458),
    ("2^ 3^ 3 2", 0.67449),
    ("0^ 1^ 2 3", 0.66347),
    ("3^ 2^ 1 0", 0.66347),
)


def h2_fermion_hamiltonian() -> FermionOperator:
    """Return the manually supplied four-spin-orbital H2 Hamiltonian."""
    hamiltonian = FermionOperator()
    for term, coefficient in H2_TERMS:
        hamiltonian += FermionOperator(term, coefficient)
    return hamiltonian


def qubit_operator_to_qutip(qubit_operator, n_qubits: int) -> Qobj:
    """Convert an OpenFermion QubitOperator to a tensor-structured Qobj."""
    pauli = {
        "I": qeye(2),
        "X": Qobj([[0, 1], [1, 0]]),
        "Y": Qobj([[0, -1j], [1j, 0]]),
        "Z": sigmaz(),
    }
    identity = tensor([qeye(2) for _ in range(n_qubits)])
    hamiltonian = 0.0 * identity
    for term, coefficient in qubit_operator.terms.items():
        factors = [pauli["I"] for _ in range(n_qubits)]
        for index, operator in term:
            if index >= n_qubits:
                raise ValueError(f"Pauli term acts on qubit {index}; allocated qubits: {n_qubits}")
            factors[index] = pauli[operator]
        hamiltonian += coefficient * tensor(factors)
    return hamiltonian


def build_model(config: ModelConfig = ModelConfig()) -> VibronicModel:
    """Construct electronic, vibrational, and interaction Hamiltonian blocks."""
    config.validate()
    qubit_hamiltonian = bravyi_kitaev(
        h2_fermion_hamiltonian(), n_qubits=config.n_qubits
    )
    h_electronic = qubit_operator_to_qutip(qubit_hamiltonian, config.n_qubits)

    electronic_identity = tensor([qeye(2) for _ in range(config.n_qubits)])
    vibrational_identity = qeye(config.n_vibrational_levels)
    a_mode = destroy(config.n_vibrational_levels)
    a_full = tensor(electronic_identity, a_mode)
    number = a_full.dag() * a_full
    z0 = tensor(
        sigmaz(),
        *[qeye(2) for _ in range(config.n_qubits - 1)],
        vibrational_identity,
    )

    h_free = tensor(h_electronic, vibrational_identity) + config.omega * number
    h_interaction = config.coupling * z0 * (a_full + a_full.dag())
    h_total = h_free + h_interaction
    return VibronicModel(
        config=config,
        h_total=h_total,
        h_free=h_free,
        h_interaction=h_interaction,
        annihilation=a_full,
        number=number,
        z0=z0,
        qubit_hamiltonian=qubit_hamiltonian,
    )


def reference_initial_state(config: ModelConfig) -> Qobj:
    """Return a documented non-stationary reference state for dynamics tests."""
    electronic = tensor(
        (basis(2, 0) + basis(2, 1)).unit(),
        basis(2, 0),
        basis(2, 0),
        basis(2, 0),
    )
    return tensor(electronic, basis(config.n_vibrational_levels, 0))


def collapse_operators(model: VibronicModel, t1: float, t2: float) -> list[Qobj]:
    """Return zero-temperature damping and pure-dephasing operators."""
    if t1 <= 0 or t2 <= 0:
        raise ValueError("T1 and T2 must be positive")
    gamma_down = 1.0 / t1
    gamma_phi = max(0.0, 1.0 / t2 - 1.0 / (2.0 * t1))
    operators = [np.sqrt(gamma_down) * model.annihilation]
    if gamma_phi > 0:
        operators.append(np.sqrt(2.0 * gamma_phi) * model.number)
    return operators


def simulate_closed_open(
    config: ModelConfig,
    times: np.ndarray,
    *,
    t1: float,
    t2: float,
) -> dict[str, np.ndarray | int]:
    """Simulate unitary and Lindblad dynamics for two observables."""
    if times.ndim != 1 or len(times) < 2 or np.any(np.diff(times) <= 0):
        raise ValueError("times must be a strictly increasing one-dimensional array")
    model = build_model(config)
    initial_state = reference_initial_state(config)
    observables = [model.number, model.z0]
    closed = sesolve(model.h_total, initial_state, times, e_ops=observables)
    c_ops = collapse_operators(model, t1, t2)
    opened = mesolve(model.h_total, initial_state, times, c_ops=c_ops, e_ops=observables)
    return {
        "time": np.asarray(times),
        "closed_boson_number": np.real_if_close(closed.expect[0]),
        "open_boson_number": np.real_if_close(opened.expect[0]),
        "closed_z0": np.real_if_close(closed.expect[1]),
        "open_z0": np.real_if_close(opened.expect[1]),
        "pauli_terms": len(model.qubit_hamiltonian.terms),
        "hilbert_dimension": model.h_total.shape[0],
        "collapse_operators": len(c_ops),
    }


def _pure_state_fidelity(reference: Qobj, state: Qobj) -> float:
    return float(abs(reference.overlap(state)) ** 2)


def trotter_convergence(
    config: ModelConfig,
    total_time: float,
    step_counts: Iterable[int],
) -> list[dict[str, float | int]]:
    """Compare first-order Lie and second-order Strang product formulas."""
    if total_time <= 0:
        raise ValueError("total_time must be positive")
    model = build_model(config)
    initial_state = reference_initial_state(config)
    exact_state = (-1j * model.h_total * total_time).expm() * initial_state
    rows: list[dict[str, float | int]] = []

    for steps in step_counts:
        if steps < 1:
            raise ValueError("step counts must be positive")
        dt = total_time / steps
        u_free = (-1j * model.h_free * dt).expm()
        u_interaction = (-1j * model.h_interaction * dt).expm()
        u_free_half = (-1j * model.h_free * (dt / 2.0)).expm()

        lie_state = initial_state
        strang_state = initial_state
        for _ in range(steps):
            lie_state = u_interaction * (u_free * lie_state)
            strang_state = u_free_half * (u_interaction * (u_free_half * strang_state))

        lie_fidelity = _pure_state_fidelity(exact_state, lie_state)
        strang_fidelity = _pure_state_fidelity(exact_state, strang_state)
        rows.append(
            {
                "steps": steps,
                "dt": dt,
                "lie_fidelity": lie_fidelity,
                "lie_infidelity": max(0.0, 1.0 - lie_fidelity),
                "strang_fidelity": strang_fidelity,
                "strang_infidelity": max(0.0, 1.0 - strang_fidelity),
            }
        )
    return rows


def cutoff_observables(
    levels: Iterable[int],
    *,
    omega: float,
    coupling: float,
    final_time: float,
) -> list[dict[str, float | int]]:
    """Measure final observables as the bosonic cutoff is increased."""
    if final_time <= 0:
        raise ValueError("final_time must be positive")
    rows: list[dict[str, float | int]] = []
    for cutoff in levels:
        config = ModelConfig(
            n_vibrational_levels=cutoff,
            omega=omega,
            coupling=coupling,
        )
        model = build_model(config)
        state = (-1j * model.h_total * final_time).expm() * reference_initial_state(config)
        rows.append(
            {
                "vibrational_levels": cutoff,
                "hilbert_dimension": model.h_total.shape[0],
                "boson_number": float(np.real(expect(model.number, state))),
                "z0": float(np.real(expect(model.z0, state))),
            }
        )
    return rows
