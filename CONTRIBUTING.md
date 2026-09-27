# Contributing

欢迎提交问题、修正和可复现性改进。

提交前请：

1. 使用 `python -m pip install -e ".[dev]"` 创建开发环境；Notebook 用户也可使用 `environment.yml`。
2. 不要提交 Notebook 的运行输出、执行编号或本机绝对路径。
3. 运行 `python scripts/clean_notebooks.py --check` 检查 Notebook。
4. 运行 `python scripts/validate_repository.py` 完成结构与数据检查。
5. 运行 `ruff check src examples experiments scripts tests` 和 `ruff format --check src examples experiments scripts tests`。
6. 运行 `pytest`，并使用 `python -m build` 验证源码包和 wheel。
7. 若修改原始数据，请在 `data/README.md` 中记录来源、列含义和参数。
8. 面向用户的变化应记录在 `CHANGELOG.md` 的 `Unreleased` 小节。

新 Notebook 应放入最合适的 `notebooks/` 子目录，并在 `docs/notebook-index.md` 中补充说明。探索性草稿请放入 `archive/`。
