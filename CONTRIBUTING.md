# Contributing

欢迎提交问题、修正和可复现性改进。

提交前请：

1. 使用 `environment.yml` 或 `requirements.txt` 创建独立环境。
2. 不要提交 Notebook 的运行输出、执行编号或本机绝对路径。
3. 运行 `python scripts/clean_notebooks.py` 清理 Notebook。
4. 运行 `python scripts/validate_repository.py` 完成基础检查。
5. 若修改原始数据，请在 `data/README.md` 中记录来源、列含义和参数。

新 Notebook 应放入最合适的 `notebooks/` 子目录，并在 `docs/notebook-index.md` 中补充说明。探索性草稿请放入 `archive/`。
