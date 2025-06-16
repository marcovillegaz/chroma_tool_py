import pandas as pd
import os

def extract_calibration_data(excel_path, summary_sheet_name="Calibration_Summary"):
    """
    Extracts calibration curve parameters from each sheet in an Excel file and creates a summary table.

    Parameters:
        excel_path (str): Path to the Excel file.
        summary_sheet_name (str): Name of the sheet where the summary will be stored.

    Returns:
        pd.DataFrame: Summary DataFrame containing calibration parameters.
    """
    # Load the Excel file
    with pd.ExcelFile(excel_path, engine="openpyxl") as xls:
        summary_data = []

        for sheet_name in xls.sheet_names:
            # Read only the required range (H2:I4)
            df = pd.read_excel(xls, sheet_name=sheet_name, usecols="H:I", skiprows=1, nrows=3, header=None)

            if df.shape == (3, 2):  # Ensure the data is in the expected format
                slope, intercept, r_squared = df.iloc[:, 1]  # Extract values
                summary_data.append([sheet_name, slope, intercept, r_squared])

        # Create a summary DataFrame
        summary_df = pd.DataFrame(summary_data, columns=["Sheet Name", "Slope", "Intercept", "R²"])

        # Save the summary to a new sheet
        with pd.ExcelWriter(excel_path, engine="openpyxl", mode="a") as writer:
            summary_df.to_excel(writer, sheet_name=summary_sheet_name, index=False)

    print(f"Calibration summary saved in '{summary_sheet_name}' sheet of {excel_path}")
    return summary_df  # Return the summary DataFrame for verification

# Example Usage:
# extract_calibration_data("/path/to/chromatogram_data.xlsx")
