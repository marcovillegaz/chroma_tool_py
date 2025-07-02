# src/io
This module contains functions for handling input/output operations related to ChromNAV data processing.

## merge_channels.py
ChromNAV exports peak information separately by channel. Each channel is stored in a file with the naming convention:

    ChromNAV_Channel_Data/
    ├── CH1.xlsx
    ├── CH2.xlsx
    ├── CH3.xlsx
    ├── CH4.xlsx
    ├── CH5.xlsx

This script reads all these channel files from a folder and merges their contents into a single DataFrame. It extracts only the relevant information, such as:

- Acquisition data
- Chromatogram name
- Channel number
- Peak (analyte) name
- Peak area
- Sample number (parsed from the file name)

The resulting DataFrame is ready for further analysis (e.g., calibration curve generation).

## update_excel_db.py
This script allows you to append the merged peak data into an existing Excel database stored as a table (within a specific worksheet of an Excel file). It helps organize and centralize peak area data from different batches for easier handling, analysis, and sharing.

The script:
- Adds metadata like batch name
- Matches and reorders columns to fit the database format
- Appends new entries directly below the existing Excel table
- Maintains formulas (e.g., concentration calculations) by copying them into the new rows


# src/display
The function in display folder are fucntion to plot in differente escenarios.
 
- chroma_plot.py contains various utility function to perofrm different kind of plot with chromaotgrafic signals. 
- peaks_plot.py contains various utility function to perform plot of peaks in a corresponding chromatogram signal. 
- 