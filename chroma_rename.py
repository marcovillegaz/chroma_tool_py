"""This script changes the names of the chromatograms allocated as csv in a given directory. 
In my case, the data extracted from the HPLC software has a format that i don't like,
so i made this program to extract the main sample name, add the number of the replicated,
and change the name of each file for easy processing.

example:
    MV__21072023 M0_011 (10).csv    has been renames as      M0_01.csv
    MV__21072023 M0_012 (10).csv    has been renames as      M0_02.csv
    MV__21072023 M0_013 (10).csv    has been renames as      M0_03.csv

"""
# This program need to be rewrite defining functions

import os
import sys
import pandas as pd


# ==============================================================================
def main(path, index_number, new_tag):
    dir_list = os.listdir(path)  # name of files in directory

    # Extract sample name
    #   example: MV__21072023 M0_013 (10).csv
    #                         ^^^^^^
    sample_names = [None] * len(dir_list)
    flag_name = " "  # This is for counting duplicated samples
    for i, file_name in enumerate(dir_list):
        print(file_name)
        words = file_name.split()
        sample_name = words[1]
        # print(sample_name)

        new_sample_name = new_tag + sample_name[index_number]

        # Count duplicates
        if new_sample_name == flag_name:
            j = j + 1
        else:
            j = 1

        flag_name = new_sample_name

        new_sample_name = new_sample_name + " (" + str(j) + ").csv"
        print(new_sample_name)

    """  # Loop for changing name in specified order
    loop_path = path + "\{}"
    for i in range(0, n):
        # Creating old_name and new_name paths
        new_name_path = loop_path.format(new_names[i])
        old_name_path = loop_path.format(old_names[i])
        # Rename chromatograms files
        os.rename(old_name_path, new_name_path)
        print(old_names[i], "\thas been renames as\t", new_names[i]) """


if __name__ == "__main__":
    print(sys.argv)
    path = sys.argv[1]
    index = int(sys.argv[2])
    new_tag = sys.argv[3]
    main(path, index, new_tag)
