"""In ChromNAV you can extract your peak info in an excel file by channels. For
further analysis, this script extract the important info (ex. peak area, peak name,
etc.) and merged them in a single excel file, where each sheet correspond to a 
single analyte, this facilitates the calibration curve analysis."""

import os
import pandas as pd


def merge_files(folder_path, extract_cols):
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
    appended_df["Sample Number"] = (
        appended_df["Chromatogram Name"].str.extract("(\d+)").astype(int)
    )

    # Change columns name.
    appended_df.rename(
        columns={
            "Chromatogram Name": "CHROMATOGRAM NAME",
            "CH": "CHANNEL",
            "Peak Name": "ANALITE",
            "Area": "AREA",
        },
        inplace=True,
    )

    return appended_df


# OBSOLETE
def merged2excel(merged_df, filepath, filename):
    """This function takes the merged dataframe and create and excel spreadsheet
    where each sheet correspond to a single analyte.

    input:
        merged_df: dataframe where all the peak information is stored.
        filepath: output folder.
        filename: name of the output file."""

    print("Writing output excel with merged files.")

    # Create an ExcelWriter object
    with pd.ExcelWriter(os.path.join(filepath, filename + ".xlsx")) as writer:

        # Group the DataFrame by the 'Peak Name' column
        for name, group_df in merged_df.groupby("Peak Name"):
            # Sort data
            group_df = group_df.sort_values(by="Sample Number")
            group_df = group_df.sort_values(by="CH")
            # write excel sheet
            group_df.to_excel(writer, sheet_name=name, index=False)
