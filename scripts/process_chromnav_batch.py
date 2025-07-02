"""Process a single batch of data."""

from src.io.merge_channels import merge_files
from src.io.update_excel_db import load_data

# Important information to be extracted, columns
extract_cols = ["Acquisition Date", "Chromatogram Name", "CH", "Peak Name", "Area"]

RAW_DATA_FOLDER = r"path/to/data"
DATABASE_PATH = r"path/to/data"

# Merge peak information into a single dataframe
appended_df = merge_files(RAW_DATA_FOLDER, extract_cols)

print(appended_df)

# Load information into the database workbook
load_data(
    new_df=appended_df,
    workbook_path=DATABASE_PATH,
    sheet_name="TABLE",
    table_name="DataTable",
    batch_name="Batch1_03",
)
