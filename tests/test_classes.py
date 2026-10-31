import numpy as np
import pandas as pd
import pytest

from chroma_tool_py.classes.chromatogram import Chromatogram
from chroma_tool_py.classes.analyte import Analyte
from chroma_tool_py.classes.sequence import Sequence


class TestCreateFromPda:
    def test_shape_matches_info(self, pda_chromatogram):
        c = pda_chromatogram
        assert c.PDA_DATA.shape == (
            int(c.INFO["TIME_NPOINTS"]),
            int(c.INFO["WL_NPOINTS"]),
        )
        assert c.PDA_DATA.shape == (2941, 101)

    def test_info_keys(self, pda_chromatogram):
        keys = set(pda_chromatogram.INFO)
        assert {
            "DATA_TYPE", "TIME_INTERVAL", "START_TIME", "END_TIME", "START_WL",
            "END_WL", "TIME_NPOINTS", "WL_NPOINTS", "NEW_PDA", "INTENSITY_UNIT",
        } <= keys
        # comas decimales convertidas a punto
        assert pda_chromatogram.INFO["END_TIME"] == "9.8000min"

    def test_name_without_pda_suffix(self, tmp_path, pda_file):
        dst = tmp_path / "muestra (PDA).txt"
        dst.write_text(pda_file.read_text())
        assert Chromatogram.create_from_pda(dst).NAME == "muestra"

    def test_name_plain_stem(self, pda_chromatogram):
        assert pda_chromatogram.NAME == "1w_ef_x"

    def test_registered_in_all(self, pda_chromatogram):
        assert pda_chromatogram in Chromatogram.all

    @pytest.mark.xfail(strict=False, reason="Cabecera fija de 11 lineas: una cabecera de otro tamano rompe el parseo (Fase C)")
    def test_header_of_different_length(self, tmp_path):
        lines = [
            "DATA_TYPE\tPDAChromatogram", "TIME_INTERVAL\t200msec", "WL_INTERVAL\t2,00nm",
            "START_TIME\t0,0000min", "END_TIME\t0,4000min", "START_WL\t200,00nm",
            "END_WL\t204,00nm", "TIME_NPOINTS\t3", "WL_NPOINTS\t3",
            "INTENSITY_UNIT\tmicroAU", "INTENSITY",  # una linea menos (sin NEW_PDA)
            "1\t2\t3", "4\t5\t6", "7\t8\t9",
        ]
        p = tmp_path / "short.txt"
        p.write_text("\n".join(lines) + "\n")
        c = Chromatogram.create_from_pda(p)
        assert c.PDA_DATA.shape == (3, 3)


class TestFl:
    def test_create_from_fl_dataframe(self, fl_csv):
        c = Chromatogram.create_from_fl(fl_csv)
        assert isinstance(c.FL_DATA, pd.DataFrame)
        assert list(c.FL_DATA.columns) == ["Time", "Intensity"]
        assert len(c.FL_DATA) == 11
        assert c.INFO == {}
        assert c.PDA_DATA == {}

    def test_create_from_fl_decimal_comma(self, fl_csv):
        c = Chromatogram.create_from_fl(fl_csv)
        assert c.FL_DATA["Intensity"].iloc[-1] == pytest.approx(10.0)

    @pytest.mark.xfail(strict=False, reason="create_from_fl no recorta el sufijo '(01)' del stem: removesuffix('(01).csv') nunca coincide con un stem (Fase C)")
    def test_create_from_fl_strips_channel_suffix(self, fl_csv):
        assert Chromatogram.create_from_fl(fl_csv).NAME == "sample1"

    def test_create_from_fl_current_name_keeps_suffix(self, fl_csv):
        # Caracterizacion del comportamiento actual (bug conocido)
        assert Chromatogram.create_from_fl(fl_csv).NAME == "sample1 (01)"

    def test_add_fl_dict(self, fl_csv):
        c = Chromatogram("x", None)
        c.add_fl(fl_csv, "CH1")
        assert isinstance(c.FL_DATA, dict)
        assert set(c.FL_DATA) == {"time", "CH1"}
        assert len(c.FL_DATA["time"]) == 11
        np.testing.assert_allclose(c.FL_DATA["CH1"][-1], 10.0)

    @pytest.mark.xfail(strict=False, reason="add_fl (dict) y create_from_fl (DataFrame) dejan FL_DATA con tipos distintos (Fase C)")
    def test_fl_data_types_consistent(self, fl_csv):
        a = Chromatogram.create_from_fl(fl_csv)
        b = Chromatogram("x", None)
        b.add_fl(fl_csv, "CH1")
        assert type(a.FL_DATA) is type(b.FL_DATA)


NON_STR_FACTORIES = [
    lambda: Chromatogram(123, None),
    lambda: Analyte(123),
    lambda: Sequence(123),
]


class TestNameValidation:
    def test_defaults(self):
        c = Chromatogram("n", None)
        assert c.INFO == {} and c.PDA_DATA == {} and c.FL_DATA == {}

    def test_valid_str(self):
        assert Analyte("NAP", 3.2).name == "NAP"
        assert Sequence("seq").name == "seq"

    @pytest.mark.xfail(strict=False, reason="Se valida con assert (AssertionError) en vez de TypeError (Fase C)")
    @pytest.mark.parametrize("factory", NON_STR_FACTORIES)
    def test_non_str_raises_typeerror(self, factory):
        with pytest.raises(TypeError):
            factory()

    @pytest.mark.parametrize("factory", NON_STR_FACTORIES)
    def test_non_str_rejected_currently(self, factory):
        # Comportamiento actual: AssertionError (TypeError tras Fase C)
        with pytest.raises((AssertionError, TypeError)):
            factory()
