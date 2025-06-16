"""In ChromNAV you can extract your peak info in an excel file by channels. For
further analysis. In this script there are utility function to process
data extracted from ChromNav"""

import os
import pandas as pd


def merge(file_path, file_names, extract_cols):
    """
    Open the single channels files and return the data in a single dataframe

    Args:
        filepath (string)   : folder where the ChromNAV output is stored.
        filenames (list)    : names of the xls files (without extension).
        extract_cols (list) : columns where important data are.

    Return:
        appended_df (DataFrame) : dataframe with appended data.
    """

    appended_df = pd.DataFrame()

    # Loop by file
    for file_name in file_names:
        print(file_name.center(80, "-"))

        # Read excel file
        raw_df = pd.read_excel(io=os.path.join(file_path, file_name + ".xls"))
        # Filter by important columns
        filter_df = raw_df[extract_cols]

        # Remove last three numbers in Chromatogram_name
        filter_df.loc[:, "Chromatogram Name"] = filter_df["Chromatogram Name"].str[:-4]
        print(filter_df)

        # Append dataframes
        appended_df = pd.concat([appended_df, filter_df], ignore_index=True)

    # Sort data
    """ print(appended_df)
    group_df = appended_df.sort_values(by="Peak Name")
    # group_df = df.sort_values(by="CH")
    print(group_df) """

    print("Final dataframe".center(80, "-"))
    print(appended_df)

    return appended_df
