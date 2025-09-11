"""Process a single batch of data."""

from chroma_tool_py.io import merge_channels, update_xlsx_db

# Important information to be extracted, columns
extract_cols = ["Acquisition Date", "Chromatogram Name", "CH", "Peak Name", "Area"]

RAW_DATA_FOLDER = r"path/to/data"
DATABASE_PATH = r"path/to/data"

# Merge peak information into a single dataframe
appended_df = merge_channels(RAW_DATA_FOLDER, extract_cols)

print(appended_df)

# Load information into the database workbook
update_xlsx_db(
    new_df=appended_df,
    workbook_path=DATABASE_PATH,
    sheet_name="TABLE",
    table_name="DataTable",
    batch_name="Batch4_01",
)



