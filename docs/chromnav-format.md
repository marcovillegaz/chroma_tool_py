# ChromNAV / JASCO export format

`chroma_tool_py` parses the files that JASCO ChromNAV exports as text or Excel. Other
vendor formats are not supported. ChromNAV exports **one channel per file**, so a single
injection can produce several files.

## PDA surface (`.txt`)

Export the full PDA (3D) chromatogram as text from ChromNAV. The parser
(`Chromatogram.create_from_pda`) expects:

1. A header of `KEY<TAB>value` lines (any number of lines), for example:

   ```
   DATA_TYPE	PDAChromatogram
   TIME_INTERVAL	200msec
   WL_INTERVAL	2,00nm
   START_TIME	0,0000min
   END_TIME	9,8000min
   START_WL	200,00nm
   END_WL	400,00nm
   TIME_NPOINTS	2941
   WL_NPOINTS	101
   NEW_PDA	false
   INTENSITY_UNIT	microAU
   ```

   Decimal commas are converted to dots and the header is stored as a dict in
   `Chromatogram.INFO`. The keys `START_TIME`, `END_TIME`, `TIME_NPOINTS`, `START_WL`,
   `END_WL` and `WL_NPOINTS` are needed to build the time and wavelength axes
   (`utils.info`).
2. A line containing only `INTENSITY` (header terminator).
3. The matrix of integer intensities (micro-AU), one row per time point and one column per
   wavelength, whitespace separated. Result: `PDA_DATA` with shape
   `(TIME_NPOINTS, WL_NPOINTS)`.

The file is read as UTF-8. The chromatogram name is the file name without extension and
without a trailing ` (PDA)`. Sample files: `data/DLLME_Chromatograms/*.txt`.

## Fluorescence (`.csv`)

One CSV per FL channel (`Chromatogram.create_from_fl` / `add_fl`):

- separator `;`, decimal comma;
- a time column named `min` (renamed to `Time`) and a column `Intensity`.

```
min;Intensity
0,0000;12,5
0,0167;12,7
```

The chromatogram name is the file name without extension and without a trailing `(01)`
(ChromNAV channel suffix). The data is stored as a DataFrame in `FL_DATA`.
`add_fl(file_path, channel)` attaches a channel file to an existing chromatogram.

## Peak tables (`.xls` / `.xlsx`)

Peak integration results exported per channel, one file per channel, named after the
channel (`CH1.xlsx`, `CH2.xlsx`, ...). `io.merge_peak_tables` (used by
`process-chromnav-batch`) reads every file in the folder with `pandas.read_excel` and
requires these columns:

| Column | Meaning |
|---|---|
| `Acquisition Date` | injection date/time |
| `Chromatogram Name` | injection name; the last 4 characters (a ` (01)`-style suffix) are dropped and the first number found becomes `SAMPLE NUMBER` |
| `CH` | channel |
| `Peak Name` | analyte name |
| `Area` | peak area |

Extra columns are ignored. Output columns are renamed to upper case (`ACQUISITION DATE`,
`CHROMATOGRAM NAME`, `CHANNEL`, `ANALITE`, `AREA`, `SAMPLE NUMBER`). Legacy `.xls` files need
`xlrd` (installed as a dependency).

## Per-channel signal files used by `merge_pda_channels`

`io.merge_pda_channels` expects `<main>/original_data/<channel>/<chromatogram>.csv`
(`;` separator, decimal comma, column `Intensity`) and writes a merged table to
`<main>/merged_data/`.
