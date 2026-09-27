# Simulation data

本目录包含论文参考图所使用的纯文本数据。以 `#` 开头的首行记录列名、初态与模型参数；后续各行为空格分隔的浮点数。

| 文件 | 列定义 |
| --- | --- |
| `fidelity_g0.1.txt` | `time`, DAQC ideal/noisy fidelity, digital ideal/noisy fidelity；`g/k = 0.1` |
| `fidelity_g1.txt` | 同上；`g/k = 1` |
| `fidelity_g5.txt` | 同上；`g/k = 5` |
| `double_occupancy_g0.1.txt` | `time`, site-1 double occupancy, site-2 double occupancy；`g/k = 0.1` |
| `double_occupancy_g5.txt` | 同上；`g/k = 5` |
| `total_boson_number_g0.1.txt` | `time`, site-1 boson number, site-2 boson number, total；`g/k = 0.1` |
| `total_boson_number_g5.txt` | 同上；`g/k = 5` |
| `thermal_summary.csv` | 热态计算的汇总结果 |

`scripts/plot_reference_figures.py` 直接从本目录读取数据，不依赖当前工作目录。

原始文件名中 `double_ocupany` 的拼写已更正为 `double_occupancy`；数值内容未改动。
