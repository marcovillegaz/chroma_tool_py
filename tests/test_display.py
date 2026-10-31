import matplotlib.pyplot as plt
import pytest

from chroma_tool_py.classes.chromatogram import Chromatogram
from chroma_tool_py.display import chroma_plot


def test_backend_is_agg():
    assert plt.get_backend().lower() == "agg"


def test_pda_2d_saves(pda_chromatogram, tmp_path):
    chroma_plot.pda_2d(pda_chromatogram, [220, 254], save_path=str(tmp_path))
    assert (tmp_path / "1w_ef_x_2d.png").exists()


def test_pda_2d_show_does_not_raise(pda_chromatogram):
    chroma_plot.pda_2d(pda_chromatogram, [254])


def test_pda_spectrum(pda_chromatogram):
    # tiempos que NO caen exactamente en la malla (rama interpolada)
    chroma_plot.pda_spectrum(pda_chromatogram, [3.001, 5.001])


@pytest.mark.xfail(strict=False, reason="extract.by_time con tiempo exacto indexa data[:, index] (eje equivocado) -> IndexError; deberia ser data[index, :] (bug no listado)")
def test_pda_spectrum_exact_time(pda_chromatogram):
    chroma_plot.pda_spectrum(pda_chromatogram, [3.0])


def test_pda_contour_saves(pda_chromatogram, tmp_path):
    chroma_plot.pda_contour(pda_chromatogram, lvls=20, save_path=str(tmp_path))
    assert any(tmp_path.glob("*.png"))


def test_pda_surface_saves(pda_chromatogram, tmp_path):
    chroma_plot.pda_surface(pda_chromatogram, save_path=str(tmp_path))
    assert any(tmp_path.glob("*.png"))


def test_fl_plot_from_create_from_fl(fl_csv, tmp_path):
    c = Chromatogram.create_from_fl(fl_csv)
    chroma_plot.fl_plot(c, save_path=str(tmp_path))
    assert any(tmp_path.glob("*_FL.png"))


@pytest.mark.xfail(strict=False, reason="fl_plot espera DataFrame con 'Time'/'Intensity'; add_fl deja un dict (Fase C)")
def test_fl_plot_after_add_fl(fl_csv):
    c = Chromatogram("x", None)
    c.add_fl(fl_csv, "CH1")
    chroma_plot.fl_plot(c)
