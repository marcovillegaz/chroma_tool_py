"""Function to write your merged file into your database files"""

import pandas as pd
from openpyxl import load_workbook


def load_data(excel_path, sheet_name):
    """this function append new data to a database in a
    excel spreadsheet.
    input:
       excel_path: excel where the database is allocated as table
       sheet_name: sheet where the database is allocated as table
       new_data: dataframe to append to the databasetabl
    """

    # Load the existing database from the specified sheet
    database = pd.read_excel(excel_path, sheet_name=sheet_name)
    print(database)
