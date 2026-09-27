"""Remove transient outputs from notebooks and add consistent title cells."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEARCH_DIRS = (ROOT / "notebooks", ROOT / "archive")

NOTEBOOK_TITLES = {
    "01_h2_single_vibrational_mode.ipynb": "H₂ simulation: single vibrational mode",
    "02_h2_two_vibrational_modes.ipynb": "H₂ simulation: two vibrational modes",
    "03_h2_model_simulation.ipynb": "H₂ model simulation",
    "05_h2_animation.ipynb": "H₂ dynamics animation",
    "06_h2_test_bench.ipynb": "H₂ simulation test bench",
    "01_multimode_jc_open_system.ipynb": "Multi-mode Jaynes–Cummings open-system model",
    "02_hubbard_holstein.ipynb": "Hubbard–Holstein model",
    "03_hubbard_holstein_trotter_sweep.ipynb": "Hubbard–Holstein Trotter-step sweep",
    "04_hubbard_holstein_optimized.ipynb": "Optimized Hubbard–Holstein simulation",
    "05_holstein_jc_spectrum.ipynb": "Holstein–Jaynes–Cummings spectrum",
    "06_holstein_jc_dynamics.ipynb": "Holstein-like and Jaynes–Cummings dynamics",
    "07_jaynes_cummings_dynamics.ipynb": "Jaynes–Cummings cavity dynamics",
    "08_ultrastrong_coupling.ipynb": "Jaynes–Cummings-like ultrastrong-coupling regime",
    "09_jc_model_analysis.ipynb": "Jaynes–Cummings model analysis",
    "10_jc_model_modified.ipynb": "Modified Jaynes–Cummings model",
    "11_oh_vibrational_model.ipynb": "O–H vibrational model",
    "12_electronic_coupling.ipynb": "Electronic coupling",
    "13_iswap_gate.ipynb": "iSWAP gate dynamics",
    "14_quantum_trajectories.ipynb": "Quantum Monte Carlo trajectories",
    "01_qutip_intro.ipynb": "QuTiP introduction",
    "02_qutip_quantum_gates.ipynb": "Quantum gates in QuTiP",
    "multimode_jc_open_system_prototype.ipynb": "Archived multi-mode JC open-system prototype",
    "water_vibrational_prototype.ipynb": "Archived multi-mode molecular-vibration prototype",
}


def notebook_paths() -> list[Path]:
    return sorted(path for directory in SEARCH_DIRS for path in directory.rglob("*.ipynb"))


def clean_notebook(path: Path) -> bool:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    changed = False

    title = NOTEBOOK_TITLES.get(path.name)
    metadata = notebook.setdefault("metadata", {})
    if title and not metadata.get("repository_title_added"):
        notebook["cells"].insert(
            0,
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [f"# {title}\n", "\n", "Cleaned and organized for reproducible execution from the repository root.\n"],
            },
        )
        metadata["repository_title_added"] = True
        changed = True

    metadata.pop("widgets", None)
    relative_path = path.relative_to(ROOT).as_posix()
    for index, cell in enumerate(notebook.get("cells", [])):
        if not cell.get("id"):
            source = "".join(cell.get("source", []))
            seed = f"{relative_path}:{index}:{source}".encode()
            cell["id"] = hashlib.sha1(seed).hexdigest()[:12]
            changed = True
        if cell.get("cell_type") != "code":
            continue
        if cell.get("outputs"):
            cell["outputs"] = []
            changed = True
        if cell.get("execution_count") is not None:
            cell["execution_count"] = None
            changed = True

    if changed:
        path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return changed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report dirty notebooks without modifying them.")
    args = parser.parse_args()

    dirty: list[Path] = []
    for path in notebook_paths():
        if args.check:
            notebook = json.loads(path.read_text(encoding="utf-8"))
            has_output = any(
                cell.get("outputs") or cell.get("execution_count") is not None
                for cell in notebook.get("cells", [])
                if cell.get("cell_type") == "code"
            )
            has_missing_ids = any(not cell.get("id") for cell in notebook.get("cells", []))
            if has_output or has_missing_ids:
                dirty.append(path)
        elif clean_notebook(path):
            print(f"Cleaned {path.relative_to(ROOT)}")

    if args.check and dirty:
        for path in dirty:
            print(f"Notebook contains transient output: {path.relative_to(ROOT)}")
        raise SystemExit(1)
    if args.check:
        print(f"Checked {len(notebook_paths())} notebooks: clean")


if __name__ == "__main__":
    main()
