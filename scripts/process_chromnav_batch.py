"""Process a single batch of data."""

import os
import shutil

from src.post_processing.merged import *
from src.post_processing.data_base import *


# Important information to be extracted, columns
extract_cols = ["Acquisition Date", "Chromatogram Name", "CH", "Peak Name", "Area"]

raw_data_folder = r"path/to/data"
database_path = r"path/to/data"

# Merge peak information into a single dataframe
appended_df = merge_files(raw_data_folder, extract_cols)

print(appended_df)

# Load information into the database workbook
load_data(
    new_df=appended_df,
    workbook_path=database_path,
    sheet_name="TABLE",
    table_name="DataTable",
    batch_name="Batch1_02",
)
