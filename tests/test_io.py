import warnings

import pandas as pd
import pytest

from chroma_tool_py.io.rename import (
    remove_pattern_from_filenames,
    remove_pattern_regex,
    replace_pattern_in_filenames,
)
# NOTA: la Fase B puede mover este modulo; este import (la funcion tal como
# esta hoy, re-exportada en chroma_tool_py.io) es el que habra que ajustar.
from chroma_tool_py.io import merge_channels


def _make(folder, names):
    for n in names:
        (folder / n).write_text("x")


@pytest.mark.parametrize("func,arg", [
    (remove_pattern_from_filenames, "TV_1226 "),
    (remove_pattern_regex, r"TV_\d+ "),
])
class TestRemovePattern:
    def test_dry_run_does_not_rename(self, tmp_path, func, arg):
        _make(tmp_path, ["TV_1226 a.csv", "b.csv"])
        changes = func(str(tmp_path), arg)  # dry_run=True por defecto
        assert changes == [("TV_1226 a.csv", "a.csv")]
        assert sorted(p.name for p in tmp_path.iterdir()) == ["TV_1226 a.csv", "b.csv"]

    def test_apply_renames(self, tmp_path, func, arg):
        _make(tmp_path, ["TV_1226 a.csv", "b.csv"])
        func(str(tmp_path), arg, dry_run=False)
        assert sorted(p.name for p in tmp_path.iterdir()) == ["a.csv", "b.csv"]

    def test_does_not_overwrite_existing(self, tmp_path, func, arg):
        (tmp_path / "TV_1226 a.csv").write_text("old")
        (tmp_path / "a.csv").write_text("keep")
        changes = func(str(tmp_path), arg, dry_run=False)
        assert changes == [("TV_1226 a.csv", "a.csv")]  # se reporta aunque se omita
        assert (tmp_path / "a.csv").read_text() == "keep"
        assert (tmp_path / "TV_1226 a.csv").read_text() == "old"

    def test_missing_folder(self, tmp_path, func, arg):
        with pytest.raises(FileNotFoundError):
            func(str(tmp_path / "nope"), arg)

    def test_skips_directories(self, tmp_path, func, arg):
        (tmp_path / "TV_1226 dir").mkdir()
        assert func(str(tmp_path), arg, dry_run=False) == []
        assert (tmp_path / "TV_1226 dir").is_dir()


def test_replace_pattern(tmp_path):
    _make(tmp_path, ["a_b.csv"])
    assert replace_pattern_in_filenames(str(tmp_path), "_", "-", dry_run=False) == [("a_b.csv", "a-b.csv")]
    assert (tmp_path / "a-b.csv").exists()


class TestMergeChannels:
    def test_no_settingwithcopywarning(self, peaks_folder):
        with warnings.catch_warnings():
            # En pandas >= 3 (Copy-on-Write) la clase ya no existe; ahi el test
            # solo garantiza que no aparezcan avisos de "copy" (no otros, p.ej.
            # el de inplace=True en rename, ajeno a este cambio).
            warn_cls = getattr(pd.errors, "SettingWithCopyWarning", None)
            if warn_cls is not None:
                warnings.simplefilter("error", warn_cls)
            else:
                warnings.filterwarnings("error", message=".*(SettingWithCopy|on a copy).*")
            df = merge_channels(str(peaks_folder), self.COLS)
        assert len(df) == 4

    COLS = ["Acquisition Date", "Chromatogram Name", "CH", "Peak Name", "Area"]

    def test_merge(self, peaks_folder):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df = merge_channels(str(peaks_folder), self.COLS)
        assert len(df) == 4
        assert set(df.columns) == {
            "ACQUISITION DATE", "CHROMATOGRAM NAME", "CHANNEL", "ANALITE", "AREA", "SAMPLE NUMBER",
        }
        assert set(df["CHANNEL"]) == {"CH1", "CH2"}
        # se recortan los ultimos 4 caracteres: "Std 12 (01)" -> "Std 12 "
        # (queda un espacio final; comportamiento actual, sorprendente)
        assert set(df["CHROMATOGRAM NAME"]) == {"Std 12 ", "Std 13 "}
        assert sorted(df["SAMPLE NUMBER"].unique()) == [12, 13]
        assert str(df["SAMPLE NUMBER"].dtype) == "Int64"
        assert df["AREA"].sum() == pytest.approx(100 + 200 + 200 + 400)


class TestCalibrationCurveParams:
    @staticmethod
    def _make_xlsx(path):
        from openpyxl import Workbook

        wb = Workbook()
        wb.active.title = "NAP"
        for name, vals in (("NAP", (2.0, 0.5, 0.99)), ("PYR", (3.0, 0.1, 0.98))):
            ws = wb[name] if name in wb.sheetnames else wb.create_sheet(name)
            for i, v in enumerate(vals):  # H2:I4
                ws.cell(row=2 + i, column=8, value=["Slope", "Intercept", "R2"][i])
                ws.cell(row=2 + i, column=9, value=v)
        wb.save(path)

    def test_run_twice(self, tmp_path):
        from openpyxl import load_workbook
        from chroma_tool_py.processing.calibration_curve_params import extract_calibration_data

        xlsx = tmp_path / "cal.xlsx"
        self._make_xlsx(xlsx)
        df1 = extract_calibration_data(str(xlsx))
        assert list(df1["Sheet Name"]) == ["NAP", "PYR"]
        assert list(df1["Slope"]) == [2.0, 3.0]
        # segunda ejecucion: antes fallaba (hoja ya existente)
        extract_calibration_data(str(xlsx))
        wb = load_workbook(xlsx)
        assert wb.sheetnames.count("Calibration_Summary") == 1
        assert wb["Calibration_Summary"].max_row == 3
