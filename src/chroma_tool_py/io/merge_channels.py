"""In ChromNAV you can extract your peak info in an excel file by channels. For
further analysis, this script extract the important info (ex. peak area, peak name,
etc.) and merged them in a single excel file, where each sheet correspond to a
single analyte, this facilitates the calibration curve analysis."""

import os
import pandas as pd


def merge_channels(folder_path, extract_cols):
    """
    Merge the single channel peak information into a single dataframe.

    params:
        folder_path: folder where the ChromNAV single channel info are stored.
        extract_cols: column with the information you want to extract.
    return:
        appended_df: dataframe with appended data.

    Description:

    The name of the files stored in folder_path must agree with the channel
    names. e.g. CH1.xlsx, CH2.xlsx, CH9.xlsx
    """
    print(f"Files stored in '{folder_path}' were being merged into a single DataFrame")
    appended_df = pd.DataFrame()

    # Loop by file
    for filename in os.listdir(folder_path):
        print(f"\tOpenning {filename}")
        # Read excel file
        raw_df = pd.read_excel(io=os.path.join(folder_path, filename))
        # Filter by important columns
        filter_df = raw_df[extract_cols]
        # Remove last three numbers in Chromatogram_name (For ChromNav software)
        filter_df.loc[:, "Chromatogram Name"] = filter_df["Chromatogram Name"].str[:-4]
        # Append dataframes
        appended_df = pd.concat([appended_df, filter_df], ignore_index=True)

    # Extract numeric part from "name" column and convert to integers
    appended_df["SAMPLE NUMBER"] = (
        appended_df["Chromatogram Name"].str.extract("(\d+)").astype(int)
    )

    # Change columns name.
    appended_df.rename(
        columns={
            "Acquisition Date": "ACQUISITION DATE",
            "Chromatogram Name": "CHROMATOGRAM NAME",
            "CH": "CHANNEL",
            "Peak Name": "ANALITE",
            "Area": "AREA",
        },
        inplace=True,
    )

    return appended_df
