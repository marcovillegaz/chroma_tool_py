# Contributing

Thanks for your interest in chroma_tool_py. Issues and pull requests are welcome at
<https://github.com/marcovillegaz/chroma_tool_py>.

## Setup

```bash
git clone https://github.com/marcovillegaz/chroma_tool_py.git
cd chroma_tool_py
pip install -e ".[dev]"
```

## Checks before opening a pull request

```bash
python -m pytest
ruff check src
```

Add or update tests in `tests/` for any behaviour change. Do not commit personal paths,
credentials or client data.

## Commit style

Use [Conventional Commits](https://www.conventionalcommits.org/): `feat(io): ...`,
`fix(classes): ...`, `docs: ...`, `test: ...`, `refactor: ...`, `build: ...`, `chore: ...`.
Keep each commit focused on one logical change.

See [ROADMAP.md](ROADMAP.md) for planned work.
