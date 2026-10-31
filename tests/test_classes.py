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


class TestCreateFromPdaHeader:
    BODY = ["1\t2\t3", "4\t5\t6", "7\t8\t9"]
    BASE = [
        "DATA_TYPE\tPDAChromatogram", "TIME_INTERVAL\t200msec", "WL_INTERVAL\t2,00nm",
        "START_TIME\t0,0000min", "END_TIME\t0,4000min", "START_WL\t200,00nm",
        "END_WL\t204,00nm", "TIME_NPOINTS\t3", "WL_NPOINTS\t3",
        "NEW_PDA\tfalse", "INTENSITY_UNIT\tmicroAU",
    ]

    def _write(self, tmp_path, header, newline="\n"):
        p = tmp_path / "h.txt"
        text = newline.join(header + ["INTENSITY"] + self.BODY) + newline
        p.write_bytes(text.encode("utf-8"))
        return p

    def test_header_one_line_shorter(self, tmp_path):
        header = [h for h in self.BASE if not h.startswith("NEW_PDA")]
        c = Chromatogram.create_from_pda(self._write(tmp_path, header))
        assert c.PDA_DATA.shape == (3, 3)
        assert "NEW_PDA" not in c.INFO

    def test_header_one_line_longer(self, tmp_path):
        c = Chromatogram.create_from_pda(self._write(tmp_path, self.BASE + ["EXTRA\tvalor"]))
        assert c.PDA_DATA.shape == (3, 3)
        assert c.INFO["EXTRA"] == "valor"

    def test_real_file_modified_header(self, tmp_path, pda_file):
        lines = pda_file.read_bytes().decode("utf-8").splitlines()
        lines.insert(lines.index("INTENSITY"), "EXTRA_KEY\tx")
        p = tmp_path / "real_mod.txt"
        p.write_bytes(("\r\n".join(lines) + "\r\n").encode("utf-8"))
        c = Chromatogram.create_from_pda(p)
        assert c.PDA_DATA.shape == (2941, 101)
        assert c.INFO["EXTRA_KEY"] == "x"

    def test_crlf_and_lf_equivalent(self, tmp_path):
        a = Chromatogram.create_from_pda(self._write(tmp_path, self.BASE, "\r\n"))
        b = Chromatogram.create_from_pda(self._write(tmp_path, self.BASE, "\n"))
        assert a.INFO == b.INFO
        np.testing.assert_array_equal(a.PDA_DATA, b.PDA_DATA)
        assert all("\r" not in k and "\r" not in v for k, v in a.INFO.items())

    def test_missing_intensity_raises_valueerror(self, tmp_path):
        p = tmp_path / "noint.txt"
        p.write_text("\n".join(self.BASE + self.BODY) + "\n")
        with pytest.raises(ValueError, match="INTENSITY"):
            Chromatogram.create_from_pda(p)


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

    def test_create_from_fl_strips_channel_suffix(self, fl_csv):
        assert Chromatogram.create_from_fl(fl_csv).NAME == "sample1"

    def test_create_from_fl_name_is_trimmed(self, fl_csv):
        # "sample1 (01).csv" -> "sample1" (sin sufijo ni espacio final)
        assert Chromatogram.create_from_fl(fl_csv).NAME == "sample1"

    def test_add_fl_dataframe(self, fl_csv):
        c = Chromatogram("x", None)
        c.add_fl(fl_csv, "CH1")
        assert isinstance(c.FL_DATA, pd.DataFrame)
        assert list(c.FL_DATA.columns) == ["Time", "Intensity"]
        assert len(c.FL_DATA) == 11
        assert c.FL_DATA.attrs["channel"] == "CH1"
        np.testing.assert_allclose(c.FL_DATA["Intensity"].iloc[-1], 10.0)
        np.testing.assert_allclose(c.FL_DATA["Time"].iloc[-1], 1.0)

    def test_fl_data_types_consistent(self, fl_csv):
        a = Chromatogram.create_from_fl(fl_csv)
        b = Chromatogram("x", None)
        b.add_fl(fl_csv, "CH1")
        assert type(a.FL_DATA) is type(b.FL_DATA)
        assert list(a.FL_DATA.columns) == list(b.FL_DATA.columns)
        pd.testing.assert_frame_equal(a.FL_DATA, b.FL_DATA)


NON_STR_FACTORIES = [
    lambda: Chromatogram(123, None),
    lambda: Analyte(123),
    lambda: Sequence(123),
]


class TestNameValidation:
    def test_sequence_execute_is_classmethod(self):
        assert Sequence.execute() is None

    @pytest.mark.parametrize("factory", NON_STR_FACTORIES)
    def test_non_str_not_registered(self, factory):
        n = len(Sequence.all)
        with pytest.raises(TypeError):
            factory()
        assert len(Sequence.all) == n

    def test_defaults(self):
        c = Chromatogram("n", None)
        assert c.INFO == {} and c.PDA_DATA == {} and c.FL_DATA == {}

    def test_valid_str(self):
        assert Analyte("NAP", 3.2).name == "NAP"
        assert Sequence("seq").name == "seq"

    @pytest.mark.parametrize("factory", NON_STR_FACTORIES)
    def test_non_str_raises_typeerror(self, factory):
        with pytest.raises(TypeError):
            factory()

    @pytest.mark.parametrize("factory", NON_STR_FACTORIES)
    def test_non_str_not_assertion_error(self, factory):
        with pytest.raises(TypeError) as exc:
            factory()
        assert not isinstance(exc.value, AssertionError)
