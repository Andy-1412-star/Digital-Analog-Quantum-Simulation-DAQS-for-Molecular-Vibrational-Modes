# Digital-Analog Quantum Computing of Fermion–Boson Models

[English README](README.md) · [Notebook 索引](docs/notebook-index.md) · [方法说明](docs/methodology.md)

本仓库整理了超导电路中费米子–玻色子模型的数字–模拟量子计算（DAQC）数值实验，涵盖 Hubbard–Holstein、Jaynes–Cummings、分子振动及相关 QuTiP 示例。

研究背景对应论文：

> S. Kumar *et al.*, “Digital-analog quantum computing of fermion-boson models in superconducting circuits,” *npj Quantum Information* **11**, 43 (2025). [DOI: 10.1038/s41534-025-01001-4](https://doi.org/10.1038/s41534-025-01001-4)

## 仓库内容

| 路径 | 内容 |
| --- | --- |
| [`examples`](examples) | 便于招聘者快速审阅的端到端示例 |
| [`experiments`](experiments) | 可复现实验入口，生成完整数值结果与图片 |
| [`src/daqc`](src/daqc) | 可复用的模型、噪声和乘积公式实现 |
| [`results`](results) | 实验生成的 CSV 与 JSON 数据 |
| [`tests`](tests) | 模型和收敛行为的自动化测试 |
| [`notebooks/applications`](notebooks/applications) | H₂ 参考模型与分子振动应用 |
| [`notebooks/models`](notebooks/models) | Hubbard–Holstein、Jaynes–Cummings、iSWAP、量子轨迹等模型 |
| [`notebooks/tutorials`](notebooks/tutorials) | QuTiP 入门与量子门教程 |
| [`data/raw`](data/raw) | 论文图所用的原始数值数据 |
| [`scripts`](scripts) | 绘图、Notebook 清理和仓库检查脚本 |
| [`figures`](figures) | 可直接预览的结果图 |
| [`archive`](archive) | 探索性实验和早期绘图草稿，不作为主入口 |

完整的 Notebook 说明及旧文件名映射见 [`docs/notebook-index.md`](docs/notebook-index.md)。

## 快速开始

推荐使用 Conda 创建隔离环境：

```bash
conda env create -f environment.yml
conda activate daqc-fermion-boson
jupyter lab
```

也可以使用 `pip`：

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab
```

建议先从以下 Notebook 开始：

1. [`H₂ 单振动模式`](notebooks/applications/01_h2_single_vibrational_mode.ipynb)
2. [`H₂ 双振动模式`](notebooks/applications/02_h2_two_vibrational_modes.ipynb)
3. [`Hubbard–Holstein 模型`](notebooks/models/02_hubbard_holstein.ipynb)
4. [`QuTiP 入门`](notebooks/tutorials/01_qutip_intro.ipynb)

如需快速验证 OpenFermion → QuTiP → closed/open-system 主线，可运行：

```bash
python -m pip install -e .
python examples/h2_vibronic_open_system.py
```

完整生成开放系统、Trotter 收敛和玻色截断结果：

```bash
python experiments/run_h2_study.py
```

## 主要结果

在仓库记录的测试参数下，完整实验得到：

- 振动阻尼与退相干使末态玻色占据数从 `0.107630` 降至 `0.075222`，降幅约 30.1%。
- 使用 64 个乘积公式步时，Lie–Trotter 末态不保真度为 `6.22e-5`，Strang 为 `2.77e-8`。
- 玻色截断从 4 增至 5 时，末态玻色占据数仅变化 `1.83e-5`，说明该可观测量已基本收敛。

完整精度数据、假设和局限见 [`RESULTS.md`](RESULTS.md)，CSV/JSON 原始结果及字段定义见 [`results/`](results/README.md)。

![Closed and open H2 dynamics](figures/h2_closed_open_dynamics.png)

![Lie-Trotter and Strang convergence](figures/h2_trotter_convergence.png)

![Bosonic cutoff convergence](figures/h2_cutoff_convergence.png)

部分分子模拟需要较大的 Hilbert 空间，运行前请先减小玻色截断维数或时间采样点进行试跑。

## 复现参考图

以下命令读取 `data/raw/` 中的数据并生成论文 Fig. 2 和 Fig. 5 对应的图：

```bash
python scripts/plot_reference_figures.py
```

默认结果写入 `figures/`。LaTeX 可用时可追加 `--use-tex`，交互显示可追加 `--show`。

![Fidelity comparison](figures/figure_2_fidelity.png)

![Double occupancy and boson number](figures/figure_5_dynamics.png)

## 数据与可复现性

- Notebook 已清除运行输出和执行编号，避免提交本机路径、报错堆栈和大体积嵌入图片。
- 原始数值数据保留在 `data/raw/`；列定义见 [`data/README.md`](data/README.md)。
- `outputs/` 用于本地产生的大文件，默认不会被 Git 跟踪。
- 可运行 `python scripts/validate_repository.py` 检查 Notebook JSON、输出清理状态和数据列一致性。
- GitHub Actions 会额外运行单元测试和缩小版完整实验，检查 Hamiltonian 厄米性、张量维数、开放系统数值以及乘积公式收敛。

## 引用

如果本仓库对你的工作有帮助，请引用上述论文。GitHub 的 “Cite this repository” 入口会读取 [`CITATION.cff`](CITATION.cff)。

## 许可证

本仓库暂未指定代码许可证。公开发布前，建议由仓库维护者选择并添加合适的 `LICENSE` 文件。
