# Command-line tools

Installed as console scripts (see `[project.scripts]` in `pyproject.toml`). Each file in
the input folder is processed independently; an error in one file is printed and the
batch continues.

## plot-batch-pda

Plot PDA chromatograms from every `*.txt` file in a folder.

```
plot-batch-pda --input INPUT --output OUTPUT [--mode {contour,2d,both}] [--wavelengths WAVELENGTHS]
```

| Option | Description |
|---|---|
| `-i`, `--input` | Folder containing PDA `.txt` files (required) |
| `-o`, `--output` | Folder to save the plots; created if missing (required) |
| `-m`, `--mode` | `contour`, `2d` or `both` (default `both`) |
| `-w`, `--wavelengths` | Comma-separated wavelengths in nm for the 2D plots (default `250,300`) |

Outputs per file: `<name>_PDA.png` (contour) and/or `<name>_2d.png`. The contour plot uses
fixed axis limits (`y_max=400`, `z_min=-10000`, `z_max=530000`); 2D wavelengths outside the
acquired range are skipped with a message.

```bash
plot-batch-pda -i data/DLLME_Chromatograms -o plots -m 2d -w 254,280
```

## plot-batch-fl

Plot FL chromatograms from every `*.csv` file in a folder.

```
plot-batch-fl --input INPUT --output OUTPUT
```

| Option | Description |
|---|---|
| `-i`, `--input` | Folder containing FL `.csv` files (required) |
| `-o`, `--output` | Folder to save the plots; created if missing (required) |

Output per file: `<name>_FL.png`. A trailing `(01)` in the file name is removed from the
chromatogram name.

## process-chromnav-batch

Merge the per-channel peak tables of a batch folder and append them to an Excel database.

```
process-chromnav-batch --batch BATCH --database DATABASE
```

| Option | Description |
|---|---|
| `-b`, `--batch` | Batch folder with one peak-table file per channel, named after the channel (`CH1.xlsx`, `CH2.xlsx`, ...) (required) |
| `-db`, `--database` | Path of the existing Excel database workbook (required) |

Every file in the batch folder must be an Excel file (read with `pandas.read_excel`) with
the columns `Acquisition Date`, `Chromatogram Name`, `CH`, `Peak Name` and `Area`. The
batch name stored in the database is the batch folder name.

The workbook must already contain a sheet named `TABLE` with an Excel Table named
`DataTable`. New rows are appended to that table with the columns, in order:
`ACQUISITION DATE`, `BATCH NAME`, `CHROMATOGRAM NAME`, `CHANNEL`, `ANALITE`, `AREA`,
`CONCENTRATION [ug/mL]` (empty; if the last cell of the last column holds a formula, it is
copied to the new rows). The workbook is modified in place, so keep a backup.

## Other helpers (library only)

Not exposed as commands: `chroma_tool_py.io.rename` (bulk file renaming, `dry_run=True`
by default), `chroma_tool_py.io.merge_pda_channels` and
`chroma_tool_py.processing.calibration_curve_params`.
