# Notebook index

Notebook 按“应用 → 基础模型 → 教程 → 归档”的顺序组织。所有文件均已清除历史输出，首次运行时请从上到下执行单元格。

## Applications

| Notebook | 说明 | 原文件名 |
| --- | --- | --- |
| `01_h2_single_vibrational_mode.ipynb` | 使用手动参考电子系数的 H₂ 单振动模式 DAQS 构建 | `H_2 真实模拟（单振动模式）.ipynb` |
| `02_h2_two_vibrational_modes.ipynb` | 使用手动参考电子系数的 H₂ 双振动模式探索 | `真实H2分子模拟（双振动模式）.ipynb` |
| `03_h2_model_simulation.ipynb` | H₂ 模型、振动激发与三维可视化 | `H2 Model Simulation.ipynb` |
| `05_h2_animation.ipynb` | H₂ 动力学动画 | `animation for H2.ipynb` |
| `06_h2_test_bench.ipynb` | H₂ 参数和可视化试验台 | `test for H2.ipynb` |

## Models

| Notebook | 说明 | 原文件名 |
| --- | --- | --- |
| `01_multimode_jc_open_system.ipynb` | 使用 H₂ 参考电子系数的探索性多模 JC 开放系统模型（非 H₂O 从头算） | `JC.ipynb` |
| `02_hubbard_holstein.ipynb` | Hubbard–Holstein 模型 | `HH model.ipynb` |
| `03_hubbard_holstein_trotter_sweep.ipynb` | 不同 Trotter 步数比较 | `HH model with diff Trotter.ipynb` |
| `04_hubbard_holstein_optimized.ipynb` | 加速的 Hubbard–Holstein 实现 | `HH model加速.ipynb` |
| `05_holstein_jc_spectrum.ipynb` | Holstein–JC 耦合本征能谱 | `Holstein&JC耦合得到本征能量.ipynb` |
| `06_holstein_jc_dynamics.ipynb` | Holstein-like 与 JC 时域演化 | `constructing Holstein...示例.ipynb` |
| `07_jaynes_cummings_dynamics.ipynb` | 腔场 Wigner 函数与 JC 动力学 | `Jaynes-Cumming-model.ipynb` |
| `08_ultrastrong_coupling.ipynb` | 超强耦合区的 JC-like 模型 | `Jaynes-Cummings-like model in the ultrastrong coupling regime.ipynb` |
| `09_jc_model_analysis.ipynb` | JC 模型分析与可视化 | `JC model.ipynb` |
| `10_jc_model_modified.ipynb` | 修改版 JC 模型草案 | `JCmodel改.ipynb` |
| `11_oh_vibrational_model.ipynb` | O–H 振动与二能级系统耦合 | `O-H框架.ipynb` |
| `12_electronic_coupling.ipynb` | 电子耦合及三维可视化 | `电子耦合.ipynb` |
| `13_iswap_gate.ipynb` | iSWAP 门动力学 | `iSWAP-gate.ipynb` |
| `14_quantum_trajectories.ipynb` | Monte Carlo 量子轨迹 | `Quantum-Monte-Carlo-Trajectories.ipynb` |

## Tutorials

| Notebook | 说明 | 原文件名 |
| --- | --- | --- |
| `01_qutip_intro.ipynb` | QuTiP 对象、演化、测量和可视化综合教程 | `intro.ipynb` |
| `02_qutip_quantum_gates.ipynb` | QuTiP-QIP 量子门教程 | `Quantum gates.ipynb` |

## Archive

`archive/experiments/` 保存尚未归并到主案例的 H₂/JC 实验，以及早期多振动模式原型。后者使用 H₂ 参考电子系数探索三模结构，不能视为经过验证的 H₂O 从头算模型。`archive/figure-development/` 保存论文绘图过程中的早期 Notebook；`archive/legacy/` 保存原始绘图脚本供历史对照。归档内容不保证能作为独立入口运行。

| 归档 Notebook | 归档原因 | 原文件名 |
| --- | --- | --- |
| `multimode_jc_open_system_prototype.ipynb` | 四轨道电子模型曾被截断为三个 qubit，且噪声速率未正确应用；仅保留研究过程 | `H2 Model Simulation with JC model 可跑通.ipynb` |
| `water_vibrational_prototype.ipynb` | 使用 H₂ 参考电子系数探索三模结构，不足以支持定量 H₂O 表述 | `水分子振动模模拟demo.ipynb` |
