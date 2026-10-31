import numpy as np
import pytest

from chroma_tool_py.utils import info, extract


class TestInfo:
    def test_time(self, pda_chromatogram):
        t = info.time(pda_chromatogram.INFO)
        assert t.shape == (2941,)
        assert t[0] == 0.0 and t[-1] == pytest.approx(9.8)

    def test_wavelength(self, pda_chromatogram):
        wl = info.wavelenth(pda_chromatogram.INFO)  # (sic) nombre actual
        assert wl.shape == (101,)
        assert wl[0] == 200.0 and wl[-1] == 400.0
        assert np.allclose(np.diff(wl), 2.0)

    def test_time_synthetic(self):
        t = info.time({"START_TIME": "1.0min", "END_TIME": "2.0min", "TIME_NPOINTS": "3"})
        np.testing.assert_allclose(t, [1.0, 1.5, 2.0])


class TestExtract:
    def test_by_wavelength_exact(self, pda_chromatogram):
        c = pda_chromatogram
        out = extract.by_wavelength(c, 250)  # 250 = 200 + 25*2 -> indice 25
        assert out.shape == (2941,)
        np.testing.assert_array_equal(out, c.PDA_DATA[:, 25])

    def test_by_wavelength_interpolated(self, pda_chromatogram):
        c = pda_chromatogram
        out = extract.by_wavelength(c, 251)  # entre indices 25 y 26
        np.testing.assert_allclose(out, 0.5 * c.PDA_DATA[:, 25] + 0.5 * c.PDA_DATA[:, 26])

    def test_by_time_exact_is_row(self, pda_chromatogram):
        c = pda_chromatogram
        t = info.time(c.INFO)
        k = int(np.argmin(np.abs(t - 3.0)))
        out = extract.by_time(c, float(t[k]))
        assert out.shape == (101,)
        np.testing.assert_array_equal(out, c.PDA_DATA[k, :])

    def test_by_time_exact_vs_interpolated_consistent(self, pda_chromatogram):
        c = pda_chromatogram
        t = info.time(c.INFO)
        k = 1000
        exact = extract.by_time(c, float(t[k]))
        # un tiempo apenas desplazado (interpolado) da casi el mismo espectro
        near = extract.by_time(c, float(t[k]) + 1e-6)
        assert near.shape == exact.shape
        np.testing.assert_allclose(near, exact, atol=1.0)
        # punto medio = media de las filas vecinas
        mid = extract.by_time(c, float((t[k] + t[k + 1]) / 2))
        np.testing.assert_allclose(
            mid, 0.5 * c.PDA_DATA[k, :] + 0.5 * c.PDA_DATA[k + 1, :], atol=1e-6
        )

    def test_find_neighbors_and_interpolate(self):
        assert extract.find_neighbors([2, 4, 6, 8], 5) == [1, 2]
        out = extract.interpolate_v(np.array([0.0, 10.0]), np.array([10.0, 20.0]), 0, 2, 1)
        np.testing.assert_allclose(out, [5.0, 15.0])

    def test_clip_pda(self):
        x = np.linspace(0, 10, 11)
        y = np.linspace(200, 400, 5)
        z = np.arange(55).reshape(11, 5)
        xc, yc, zc = extract.clip_pda(x, y, z, (2, 4), (250, 350))
        np.testing.assert_array_equal(xc, [2, 3, 4])
        np.testing.assert_array_equal(yc, [250, 300, 350])
        assert zc.shape == (3, 3)
        np.testing.assert_array_equal(zc, z[2:5, 1:4])

    def test_clip_pda_real_data(self, pda_chromatogram):
        c = pda_chromatogram
        t, wl = info.time(c.INFO), info.wavelenth(c.INFO)
        xc, yc, zc = extract.clip_pda(t, wl, c.PDA_DATA, (1, 2), (220, 300))
        assert zc.shape == (len(xc), len(yc))
        assert xc.min() >= 1 and xc.max() <= 2
