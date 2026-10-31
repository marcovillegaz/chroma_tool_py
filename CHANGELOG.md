# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-10-31

First public release.

### Added
- `Chromatogram`, `Analyte` and `Sequence` classes, with `Chromatogram.create_from_pda`,
  `create_from_fl` and `add_fl` for JASCO ChromNAV exports.
- Plot functions for PDA (2D, contour, surface, spectrum) and FL chromatograms.
- Command-line tools `plot-batch-pda`, `plot-batch-fl` and `process-chromnav-batch`.
- Peak-table merging (`io.merge_peak_tables`), PDA channel merging
  (`io.merge_pda_channels`), bulk file renaming (`io.rename`) and Excel database update.
- pytest suite, sample PDA data in `data/DLLME_Chromatograms/`, documentation in `docs/`.
- Packaging metadata, declared dependencies and the optional extras `baseline` and `dev`.

### Changed
- Package moved to a `src` layout; `io/merge_channels.py` and `utils/merge_channels.py`
  renamed to `io/merge_peak_tables.py` and `io/merge_pda_channels.py` (the alias
  `io.merge_channels` is kept for compatibility).
- `pybeads` is imported lazily and is an optional dependency.
- Personal paths in examples replaced by placeholders; obsolete scripts removed.

### Fixed
- Missing `__init__.py` in `cli/` and `processing/`, and broken imports.
- `create_from_pda` reads the header by key (up to the `INTENSITY` line) instead of a fixed
  line count; `create_from_fl` strips the `(01)` channel suffix correctly.
- `FL_DATA` has the same schema for `create_from_fl` and `add_fl`.
- Name validation raises `TypeError` instead of using `assert`.
- `utils.extract.by_time` indexes the spectrum by row, giving exact values at exact times.
- Removed pandas `SettingWithCopyWarning` and made the calibration summary writer re-runnable.

[0.1.0]: https://github.com/marcovillegaz/chroma_tool_py/releases/tag/v0.1.0
