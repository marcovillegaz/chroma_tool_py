"""In ChromNAV you can extract your peak info in an excel file by channels. For
further analysis, this script extract the important info (e.g. peak area, peak name,
etc.) and merged them in a single excel file, where each sheet correspond to a
single analyte. Then the information can be added to and spreadhseet that works
as database."""

import os
import shutil

from post_processing.merged import *
from post_processing.data_base import *

# Important information to be extracted
extract_cols = ["Chromatogram Name", "CH", "Peak Name", "Area"]

# Folder that contains peak information of multiple experiment.
new_folder = r"path/to/data"
# File where information of all experiments is stored
database_file = r"path/to/data"

# Date when the data was added
date_value = "30-09-2024"

experiments = os.listdir(new_folder)


# Merge peak information into a single dataframe
appended_df = merge_files(os.path.join(new_folder, experiment), extract_cols)

# Load information into the database workbook
load_data(
    new_df=appended_df,
    workbook_path=database_file,
    sheet_name="TABLE",
    table_name="DataTable",
    date=date_value,
    batch_name=experiment,
)


for experiment in experiments:
    # Merge peak information into a single dataframe
    appended_df = merge_files(os.path.join(new_folder, experiment), extract_cols)

    # Load information into the database workbook
    load_data(
        new_df=appended_df,
        workbook_path=database_file,
        sheet_name="TABLE",
        table_name="DataTable",
        date=date_value,
        batch_name=experiment,
    )

    """ # Move experiment to old-files folder
    new_experiment_path = os.path.join(new_folder, experiment)
    old_experiment_path = os.path.join(old_folder, experiment)

    # Move the entire folder to the destination
    shutil.move(new_experiment_path, old_experiment_path) """

    print(f"{experiment}' has been moved to Old_files\n")
