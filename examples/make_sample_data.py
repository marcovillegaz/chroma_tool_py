"""Generate a small synthetic ChromNAV-like dataset (PDA .txt and FL .csv).

The files are written to data/sample/ and are safe to publish: no real sample
is involved. Three Gaussian peaks (with Gaussian absorption bands) are added
over a noisy baseline.

Usage:
    python examples/make_sample_data.py [output_folder]
"""

import sys
from pathlib import Path

import numpy as np

NAME = "synthetic_mix"
START_TIME, END_TIME, N_TIME = 0.0, 3.0, 901  # min (200 msec interval)
START_WL, END_WL, N_WL = 200.0, 400.0, 21  # nm (10 nm interval)

# (retention time [min], peak width [min], lambda max [nm], band width [nm], height)
PEAKS = [
    (0.8, 0.03, 220.0, 20.0, 60000),
    (1.6, 0.04, 254.0, 25.0, 120000),
    (2.3, 0.03, 280.0, 25.0, 90000),
]


def build_pda(rng):
    time = np.linspace(START_TIME, END_TIME, N_TIME)
    wavelengths = np.linspace(START_WL, END_WL, N_WL)
    data = rng.normal(0, 3, size=(N_TIME, N_WL))
    for t_r, t_w, wl_max, wl_w, height in PEAKS:
        elution = np.exp(-0.5 * ((time - t_r) / t_w) ** 2)
        band = np.exp(-0.5 * ((wavelengths - wl_max) / wl_w) ** 2)
        data += height * np.outer(elution, band)
    return time, np.rint(data).astype(int)


def write_pda(path, data):
    def comma(value):
        return f"{value:.4f}".replace(".", ",")

    header = [
        ("DATA_TYPE", "PDAChromatogram"),
        ("TIME_INTERVAL", "200msec"),
        ("WL_INTERVAL", f"{comma((END_WL - START_WL) / (N_WL - 1))[:-2]}nm"),
        ("START_TIME", f"{comma(START_TIME)}min"),
        ("END_TIME", f"{comma(END_TIME)}min"),
        ("START_WL", f"{comma(START_WL)[:-2]}nm"),
        ("END_WL", f"{comma(END_WL)[:-2]}nm"),
        ("TIME_NPOINTS", str(N_TIME)),
        ("WL_NPOINTS", str(N_WL)),
        ("NEW_PDA", "false"),
        ("INTENSITY_UNIT", "microAU"),
    ]
    lines = [f"{key}\t{value}" for key, value in header] + ["INTENSITY"]
    lines += ["\t".join(map(str, row)) for row in data]
    path.write_text("\r\n".join(lines) + "\r\n", encoding="utf-8", newline="")


def write_fl(path, time, rng):
    intensity = rng.normal(0, 0.5, size=time.size)
    for t_r, t_w, _, _, height in PEAKS:
        intensity += height / 3000 * np.exp(-0.5 * ((time - t_r) / t_w) ** 2)
    lines = ["min;Intensity"]
    lines += [f"{t:.4f};{i:.4f}".replace(".", ",") for t, i in zip(time, intensity)]
    path.write_text("\r\n".join(lines) + "\r\n", encoding="utf-8", newline="")


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/sample")
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(0)
    time, data = build_pda(rng)
    write_pda(out / f"{NAME} (PDA).txt", data)
    write_fl(out / f"{NAME} (01).csv", time, rng)
    print(f"Synthetic sample written to {out}")


if __name__ == "__main__":
    main()
