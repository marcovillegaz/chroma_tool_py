# Installation

Requires Python 3.10 or newer. Runtime dependencies: numpy, pandas, matplotlib, scipy,
openpyxl and xlrd (the last one reads legacy `.xls` files).

## From GitHub

```bash
pip install git+https://github.com/marcovillegaz/chroma_tool_py.git
```

## From a clone (development)

```bash
git clone https://github.com/marcovillegaz/chroma_tool_py.git
cd chroma_tool_py
python -m venv .venv
# Windows: .venv\Scripts\activate    Linux/macOS: source .venv/bin/activate
pip install -e ".[dev]"
```

The `dev` extra installs pytest, ruff, build and twine.

## Optional extras

| Extra | Installs | Used by |
|---|---|---|
| `baseline` | `pybeads` | `chroma_tool_py.utils.chroma_corrector` (BEADS baseline correction) |
| `dev` | pytest, ruff, build, twine | tests, lint, packaging |

## Check the installation

```bash
plot-batch-pda --help
plot-batch-fl --help
process-chromnav-batch --help
python -m pytest
```
