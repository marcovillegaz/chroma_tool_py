# Design notes

Short overview of the classes and conventions in `src/chroma_tool_py`.

## Classes (`chroma_tool_py.classes`)

### Chromatogram

One HPLC injection. Attributes (upper case, as in the code):

| Attribute | Content |
|---|---|
| `NAME` | injection name (must be `str`, otherwise `TypeError`) |
| `INFO` | dict with the PDA header (`START_TIME`, `WL_NPOINTS`, ...); `{}` if none |
| `PDA_DATA` | `numpy` array `(time points, wavelengths)`; `{}` if none |
| `FL_DATA` | DataFrame with columns `Time` and `Intensity`; `{}` if none |

Alternative constructors (class methods): `create_from_pda(file_path)` and
`create_from_fl(file_path)`. Instance method `add_fl(file_path, channel)` attaches FL data
(same DataFrame schema as `create_from_fl`, channel label kept in `df.attrs["channel"]`).
Every instance is also appended to the class-level registry `Chromatogram.all`.

### Analyte

A compound of interest: `name` and `residence_time`, with `extract_spectrum(PDA_data)`
to plot its spectrum from a PDA surface. Instances are registered in `Analyte.all`.

### Sequence

Placeholder for a future executable processing pipeline: it stores a `name` and has an
empty class method `execute()`. Instances are registered in `Sequence.all`.

### ChromaVisualizer

Experimental tkinter widget (`classes/chroma_visualizer.py`) for interactive viewing.

## Functional modules

- `utils.info`: build time / wavelength axes from `Chromatogram.INFO`.
- `utils.extract`: `by_wavelength`, `by_time` (with interpolation) and `clip_pda`.
- `utils.peak_finder`: peak detection on top of `scipy.signal.find_peaks`.
- `display.chroma_plot`: `pda_2d`, `pda_spectrum`, `fl_plot`, `pda_contour`, `pda_surface`.
  They save a PNG when `save_path` is given, otherwise they call `plt.show()`.
- `io`: file-level operations (`merge_pda_channels`, `merge_peak_tables`,
  `update_xlsx_db`, `rename`).

## Conventions and known limitations

- Class-level registries (`all`) keep references to every created object; clear them in
  long batch jobs (`Chromatogram.all.clear()`).
- Library functions use `print` for progress; the CLIs are the intended user interface.
- Planned refactors (dataclasses, `Figure`-returning plot functions, logging) are tracked
  in [ROADMAP.md](../ROADMAP.md).
