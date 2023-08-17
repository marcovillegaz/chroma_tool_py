"""This script changes the names of the chromatograms allocated as csv in a given directory. 
In my case, the data extracted from the HPLC software present a format that i don't like,
so i made this program to extract the main sample name, add the number of the replicated,
and change the name of each file for easy processing.

example:
    MV__21072023 M0_011 (10).csv    has been renames as      M0_02.csv
    MV__21072023 M0_012 (10).csv    has been renames as      M0_04.csv
    MV__21072023 M0_013 (10).csv    has been renames as      M0_06.csv

"""

import os
import pandas as pd

# INPUT
path = r"path/to/data"

# ==============================================================================
dir_list = os.listdir(path)  # name of files in directory
# print("Files and directories in '", path, "' :")
# print(dir_list)

n = len(dir_list)  # number of files in folder

# Extract sample name
#   example: MV__21072023 M0_013 (10).csv
#                         ^^^^^^
sample_names = [None] * n
for i in range(0, n):
    old_name = dir_list[i]
    words = old_name.split()
    sample_names[i] = words[1]

# Sort elements using data frames
df_files = pd.DataFrame({"old_name": dir_list, "sample_names": sample_names})
df_files = df_files.sort_values("sample_names")
# print(df_files.to_string())
old_names = df_files["old_name"].tolist()
sample_names = df_files["sample_names"].tolist()

# Create list with new sample names
flag_name = " "  # This is for counting duplicated samples
new_names = [None] * n  # Preallocation
for i in range(0, n):
    sample = sample_names[i]

    # Count duplicates
    if sample[0:2] == flag_name:
        j = j + 1
    else:
        j = 1
    flag_name = sample[0:2]

    # Save new names in list
    new_names[i] = sample[0:2] + "_0" + str(j) + ".csv"

# Loop for changing name in specified order
loop_path = path + "\{}"
for i in range(0, n):
    # Creating old_name and new_name paths
    new_name_path = loop_path.format(new_names[i])
    old_name_path = loop_path.format(old_names[i])
    # Rename chromatograms files
    os.rename(old_name_path, new_name_path)
    print(old_names[i], "\thas been renames as\t", new_names[i])
