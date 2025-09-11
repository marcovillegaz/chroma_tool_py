"""This script rename chromatogram files. When exporting data points and peak 
information from ChromNAV, the name of the file are difficult to manage due 
long names"""

import os

# TARGER FOLDER PATH
target_folder = r"path/to/data"
# target_folder = r"path/to/data"
[print(f) for f in os.listdir(target_folder)]

# RENAME FILES INF TARGET FOLDER
for f in os.listdir(target_folder):
    # Descompose file name
    name = f.split()[1]
    extention = f.split(".")[-1]
    num = name.split("_")[1]

    # new and old paths
    new_name = os.path.join(target_folder, "point_" + num + "." + extention)
    old_name = os.path.join(target_folder, f)

    # rename file
    os.rename(old_name, new_name)


""" # RENAME FILES IN TARGET FOLDER FOR DESORPTION
for f in os.listdir(target_folder):
    # Descompose file name
    name = f.split()[1]
    extention = f.split(".")[-1]
    sample = name.split("_")[0]
    time = name.split("_")[1]

    # new and old paths
    new_name = os.path.join(target_folder, f"{sample}_{time}.{extention}")
    old_name = os.path.join(target_folder, f)

    # rename file
    os.rename(old_name, new_name) """
