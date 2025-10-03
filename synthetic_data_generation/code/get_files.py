# -*- coding: utf-8 -*-
"""
Adapted from code originally written by Kendra M. Reiter. 
Original source: https://github.com/ReiterKM/msc-thesis-microsimulations 
Modifications by Lucas Moschen.

This script contains a function that takes the sub-directory of a folder and 
returns its full path.

    Parameters
    ----------
    sub_dir : string, optional
        Sub-directory. It should start one directory level above the current file location.
        The default is "data".

    Returns
    -------
    path_to_folder : os.path
        Full path to the folder, i.e., to the desired sub-directory.
"""

import os


def get_path_to_folder(sub_dir="data"):

    # Divides sub_dir by "/"
    sub_dir = sub_dir.strip("/")

    # Get the path to current file
    file_path = os.path.dirname(os.path.realpath(__file__))

    # Go up one directory
    dir_path = os.path.dirname(file_path)

    # Get directory
    path_to_folder = os.path.join(dir_path, sub_dir)

    if not os.path.exists(path_to_folder):
        raise Exception("The path: " + path_to_folder + " does not exist.")

    return path_to_folder