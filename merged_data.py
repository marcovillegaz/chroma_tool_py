"""In ChromNAV you can extract your peak info in an excel file by channels. For
further analysis, this script extract the important info (ex. peak area, peak name,
etc.) and merged them in a single excel file, where each sheet correspond to a 
single analyte, this facilitates the calibration curve analysis."""

import os
import pandas as pd


def merge_files(filepath, filenames, extract_cols):
    """This function open the single channels files and return the data in
    a single dataframe
    input:
        filepath: folder where the ChromNAV outpur are stored.
        filenames: names of the xls file (without extension).
        extract_cols: columns where important data are.
    output:
        appended_df: dataframe with appended data.
    """

    appended_df = pd.DataFrame()

    # Loop by file
    for i, filename in enumerate(filenames):
        print(filename.center(80, "-"))

        # Read excel file
        raw_df = pd.read_excel(io=os.path.join(filepath, filename + ".xls"))
        # Filter by important columns
        filter_df = raw_df[extract_cols]

        # Remove last three numbers in Chromatogram_name
        filter_df.loc[:, "Chromatogram Name"] = filter_df["Chromatogram Name"].str[:-4]
        print(filter_df)

        # Append dataframes
        appended_df = pd.concat([appended_df, filter_df], ignore_index=True)

    # Extract numeric part from "name" column and convert to integers
    appended_df["Sample Number"] = (
        appended_df["Chromatogram Name"].str.extract("(\d+)").astype(int)
    )
    print(appended_df)
    # Sort data
    """ group_df = appended_df.sort_values(by="Peak Name")
    # group_df = df.sort_values(by="CH")
    print(group_df) """

    print("Final dataframe".center(80, "-"))
    print(appended_df)

    return appended_df


def merged_excel(merged_df, filepath, filename):
    """This function takes the merged dataframe and create and excel spreadsheet
    where each sheet correspond to a single analyte.

    input:
        merged_df: dataframe where all the peak information is stored.
        filepath: output folder.
        filename: name of the output file."""

    print("Writing output esxcel file...")
    # Create an ExcelWriter object
    with pd.ExcelWriter(os.path.join(filepath, filename + ".xlsx")) as writer:

        # Group the DataFrame by the 'Peak Name' column
        for name, group_df in merged_df.groupby("Peak Name"):
            # Sort data
            group_df = group_df.sort_values(by="Sample Number")
            group_df = group_df.sort_values(by="CH")
            # Create the "Concentration" column using the initial concentration
            group_df["Concentration"] = group_df["Sample Number"].apply(
                lambda x: initial_cons[name] / (dilution_rate**x)
            )
            group_df.to_excel(writer, sheet_name=name, index=False)


#################################################################################
channels = ["CH1", "CH9", "CH10", "CH11", "CH12", "CH13", "CH14", "CH15"]
filepath = r"path/to/data"

extract_cols = ["Chromatogram Name", "CH", "Peak Name", "Area"]
initial_cons = {
    "CAF": 121.5,
    "ACTN": 123.2,
    "TMP": 141.7,
    "MeP": 173.5,
    "BPA": 97.0,
    "TPhP": 225.8,
    "TCS": 207.3,
    "4NP": 79.0,
    "OC": 314.2,
    "DEHP": 354.9,
}

dilution_rate = 1.5

# Merge single channel data
appended_df = merge_files(filepath, channels, extract_cols)
# Write information in output spreadsheet
merged_excel(appended_df, filepath, "output")
