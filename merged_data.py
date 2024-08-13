"""In ChromNAV you can extract your peak info in an excel file by channels. For
further analysis, this script extract the important info (ex. peak area, peak name,
etc.) and merged them in a single excel file, where each sheet correspond to a 
single analyte, this facilitates the calibration curve analysis."""

import os
from post_processing.merged import *
from post_processing.data_base import *

extract_cols = ["Chromatogram Name", "CH", "Peak Name", "Area"]

# Folder that contains peak information of multiple experiment.
main_folder = r"path/to/data"
database_file = r"path/to/data"

# Specify the values for the date and experiment columns
date_value = "27-7-2024"  # Replace with the specified date
experiments = os.listdir(main_folder)

for experiment in experiments:
    # Merge peak information into a single dataframe
    appended_df = merge_files(os.path.join(main_folder, experiment), extract_cols)
    # Load information into the database workbook
    load_data(
        new_df=appended_df,
        workbook_path=database_file,
        sheet_name="TABLE",
        table_name="DataTable",
        date=date_value,
        experiment_name=experiment,
    )
