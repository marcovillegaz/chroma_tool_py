"""This script changes the names of the chromatograms allocated as csv in a given directory. 
In my case, the data extracted from the HPLC software has a format that i don't like,
so i made this program to extract the main sample name, add the number of the replicated,
and change the name of each file for easy processing.

example:
    MV__21072023 M0_011 (10).csv    has been renames as      M0_01.csv
    MV__21072023 M0_012 (10).csv    has been renames as      M0_02.csv
    MV__21072023 M0_013 (10).csv    has been renames as      M0_03.csv

"""

import os
import sys
import argparse
import pandas as pd


# ==============================================================================
def main(path, index_number, new_tag):
    """
    path: folder path where crhomatograms are stored as csv files
    new_tag: new tag for sample group
    index: postion index of the identification number of individual samples
    """
    print("input arguments".center(85, "="))
    print("FOLDERPATH: ", path)
    print("NEWTAG: ", new_tag)
    print("INDEX: ", index_number, "\n")

    dir_list = os.listdir(path)  # name of files in directory

    flag_name = " "  # This is for counting duplicated samples
    # Extract sample name
    #   example: MV__21072023 M0_013 (10).csv
    #                         ^^^^^^
    for i, file_name in enumerate(dir_list):
        # Generating new name
        words = file_name.split()
        old_chroma_name = words[1]
        old_chroma_name = old_chroma_name[:-4]
        new_chroma_name = new_tag + old_chroma_name[index_number:]

        # Count replicates
        if new_chroma_name == flag_name:
            j = j + 1
        else:
            j = 1

        flag_name = new_chroma_name
        # Add replucates to name
        new_chroma_name = (
            new_chroma_name + " (" + str(j) + ").csv"
        )  # change this to formatedd string in the forure

        # New name verification
        print(file_name, "\thas been renames as\t", new_chroma_name)
        if i == 0:
            verification = input("The name changing is correct? Write 'yes' or 'not'.")
            if verification == "not":
                print("Program stopped. Verify your input argument")
                break
            elif verification == "yes":
                print("The program shall continue :)")
            else:
                print("Not a valid response. Program stopped")
                break

        # Loop for changing name in specified order
        new_name_path = os.path.join(path, new_chroma_name)
        old_name_path = os.path.join(path, dir_list[i])

        # Rename files
        os.rename(old_name_path, new_name_path)


if __name__ == "__main__":
    # Defining description adn epilogue of the program
    parser = argparse.ArgumentParser(
        description="Change the name of multiple chromatograms stored in one folder and identify replicates.\n ",
        epilog="""Example: The old chromatogram is named 'MV__21072023 M0_011 (10).csv' \n
        MV__21072023\tis the sequence name (depends of the adquicition data software).\n
        (M)0_011\tM is the is the old sample group name. All the files in FOLDERPATH are identified with the same letter.
        \t\tThis latter will be replace with NEWTAG as M0 -> NEWTAG0
        M(0)_011\tis the sample number. Each sample, and its replecates, are identified with an specific number. 
        \t\tThis number will remain intact.

        New chromatogram name will be NEWTAG0_01  (replicate 1 of sample 0 from group NEWTAG)""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    # Defining argument to use the program in Console Line Interface
    parser.add_argument(
        "-fp",
        "--folderpath",
        type=str,
        required=True,
        help="the path of the folder that contains chromatograms",
    )
    parser.add_argument(
        "-ntg",
        "--newtag",
        type=str,
        required=True,
        help="New tag for rename your chromatograms",
    )
    parser.add_argument(
        "-idx",
        "--index",
        type=int,
        required=True,
        help="Position where of the sample number. In the example M'0'_011 zero has index 1",
    )

    args = parser.parse_args()

    main(path=args.folderpath, new_tag=args.newtag, index_number=args.index)
