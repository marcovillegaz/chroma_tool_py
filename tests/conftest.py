"""Fixtures compartidas. Fuerza el backend Agg antes de importar pyplot."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import numpy as np
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
PDA_DIR = REPO_ROOT / "data" / "DLLME_Chromatograms"


@pytest.fixture(autouse=True)
def _isolate_state():
    """Limpia el registro de clase y las figuras entre tests."""
    import matplotlib.pyplot as plt
    from chroma_tool_py.classes.chromatogram import Chromatogram

    Chromatogram.all.clear()
    yield
    plt.close("all")
    Chromatogram.all.clear()


@pytest.fixture
def pda_file():
    path = PDA_DIR / "1w_ef_x.txt"
    if not path.exists():
        pytest.skip("datos PDA reales no disponibles")
    return path


@pytest.fixture
def pda_chromatogram(pda_file):
    from chroma_tool_py.classes.chromatogram import Chromatogram

    return Chromatogram.create_from_pda(pda_file)


@pytest.fixture
def fl_csv(tmp_path):
    """CSV FL sintetico: sep=';', decimal=',', columnas min/Intensity."""
    path = tmp_path / "sample1 (01).csv"
    t = np.linspace(0, 1, 11)
    df = pd.DataFrame({"min": t, "Intensity": t * 10})
    df.to_csv(path, sep=";", decimal=",", index=False)
    return path


@pytest.fixture
def peaks_folder(tmp_path):
    """Carpeta con xlsx de picos sinteticos (uno por canal) para merge_channels."""
    folder = tmp_path / "peaks"
    folder.mkdir()
    for ch, area in (("CH1", 100.0), ("CH2", 200.0)):
        df = pd.DataFrame(
            {
                "Acquisition Date": ["2024-01-01", "2024-01-02"],
                "Chromatogram Name": ["Std 12 (01)", "Std 13 (01)"],
                "CH": [ch, ch],
                "Peak Name": ["NAP", "PYR"],
                "Area": [area, area * 2],
                "Extra": [1, 2],
            }
        )
        df.to_excel(folder / f"{ch}.xlsx", index=False)
    return folder
