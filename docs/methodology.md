# Methodology and modelling scope

## Electronic Hamiltonian

The featured H₂ workflow starts from a manually supplied four-spin-orbital Hamiltonian in second quantization,

\[
H_{\mathrm{el}} = \sum_{pq} h_{pq} c_p^\dagger c_q
+ \frac{1}{2}\sum_{pqrs} h_{pqrs} c_p^\dagger c_q^\dagger c_r c_s.
\]

OpenFermion represents these terms as `FermionOperator` objects and applies the Bravyi–Kitaev transformation. The resulting `QubitOperator` is a weighted sum of Pauli strings and is converted into a tensor-structured QuTiP `Qobj`.

## Electron–vibration model

The compact example couples the encoded electronic Hamiltonian to one truncated harmonic mode,

\[
H = H_{\mathrm{el}} + \omega a^\dagger a
+ g Z_0(a + a^\dagger).
\]

The bosonic cutoff is a numerical approximation. Convergence should be checked by increasing `--vibrational-levels` until the observables of interest stop changing appreciably.

## Closed and open dynamics

Closed-system dynamics use QuTiP's Schrödinger solver. Open-system dynamics use the Lindblad master equation,

\[
\dot{\rho} = -i[H,\rho]
+ \sum_k \left(L_k\rho L_k^\dagger
- \frac{1}{2}\{L_k^\dagger L_k,\rho\}\right).
\]

The standalone example models zero-temperature vibrational damping with
`sqrt(1/T1) * a` and pure dephasing with `sqrt(2*gamma_phi) * a†a`, where
`gamma_phi = max(0, 1/T2 - 1/(2*T1))`.

## Digital–analog product formula

The Hubbard–Holstein notebooks split the Hamiltonian into an analog block and a hopping block. A first-order Lie–Trotter step is

\[
U(\Delta t) \approx
e^{-iH_{\mathrm{digital}}\Delta t}
e^{-iH_{\mathrm{analog}}\Delta t}.
\]

`03_hubbard_holstein_trotter_sweep.ipynb` compares this approximation with exact QuTiP propagation for several step counts. The gate notebooks demonstrate propagator composition, but the repository does not yet compile every mapped molecular Pauli term into a hardware-native circuit.

The reproducible H₂-reference study in `experiments/run_h2_study.py` also splits the Hamiltonian into free and interaction blocks. It compares first-order Lie–Trotter and symmetric second-order Strang propagation against the exact matrix exponential. Because the reported metric is infidelity (the squared state-error scale), the expected asymptotic slopes are approximately `steps^-2` and `steps^-4`, respectively.

The initial electronic state is `( |0> + |1> ) / sqrt(2) ⊗ |000>` and the oscillator starts in its vacuum. This deliberately non-stationary numerical reference state makes the dynamics and approximation errors visible; it is not presented as an H₂ ground-state preparation protocol.

## Important limitations

- The featured electronic coefficients are manually supplied reference values rather than integrals generated inside the repository.
- Molecular geometries, basis-set generation, active-space selection, and particle-number-sector preparation are not yet automated.
- Bosonic modes are truncated and the noise model is phenomenological.
- Archived multi-mode prototypes are retained for provenance and should not be cited as validated H₂O calculations.
- All results are classical simulations; no quantum-hardware execution is claimed.
