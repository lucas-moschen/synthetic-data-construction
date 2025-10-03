# -*- coding: utf-8 -*-
"""
@author: Lucas Moschen

This script contains a function that takes a household data set and a dwelling data set 
located in the folder "data" and generates subsets of these data sets based on the 
proportion selected.
The reduction is made at each dwelling capacity category for the dwelling data set 
and at each household size category for the household data set, as explained in
Section 4.1.4 of the thesis.

    Parameters
    ----------
    proportion : float
        Proportion of the original data sets that the subsets will correspond to. 
    name_dwe_df_file : str
        Name of the file containing the dwelling data set.
    name_hhd_df_file : str
        Name of the file containing the household data set.

    Returns
    ----------
    None.
"""

import pandas as pd
import numpy as np
import os
import sys 
from get_files import get_path_to_folder

def reduce_data(proportion,
                name_dwe_df_file: str,
                name_hhd_df_file: str):
    
    # Seed
    np.random.seed(42)

    print("\nProcess for dwelling data:\n")

    # Get dwelling data
    data_path = get_path_to_folder("data")
    dwelling_path = os.path.join(data_path, name_dwe_df_file)
    dwelling_df = pd.read_csv(dwelling_path)
    dwelling_df = dwelling_df.reset_index(drop=True)

    print("\nThe original dwelling dataframe:")
    print(dwelling_df)

    # Get the subset taking random dwellings from each dwelling capacity class possible
    subset_dwelling_df = dwelling_df.groupby("capacity", group_keys=False).apply(
    lambda group: group.sample(frac=proportion))

    # Delete original dwelling data set
    del dwelling_df

    print("\nThe subset generated:")
    print(subset_dwelling_df)

    # Reorder the dataframe
    subset_dwelling_df = subset_dwelling_df.sort_index()

    print("\nThe subset generated reordered:")
    print(subset_dwelling_df)

    # Create save_path_dwe
    save_path_dwe = get_path_to_folder("data")

    # Get proportion as a percentage and create the name of the file
    prop = proportion * 100
    prop = int(prop) 
    save_path_dwe = os.path.join(save_path_dwe, "Houses_" + str(prop) + "%"  + ".csv")

    # Set index
    subset_dwelling_df = subset_dwelling_df.set_index("ID")

    print("\nThe subset with ID as index:")
    print(subset_dwelling_df)

    # Save the new data set file in CSV format
    subset_dwelling_df.to_csv(save_path_dwe)
    print("\nThe new dwelling data set was saved at:", save_path_dwe)

    # Delete subset
    del subset_dwelling_df

    print("_________________________________________________________")
    print("\nProcess for household data:\n")

    # Get household data
    data_path = get_path_to_folder("data")
    hhd_path = os.path.join(data_path, name_hhd_df_file)
    hhd_df = pd.read_csv(hhd_path)
    hhd_df = hhd_df.reset_index(drop=True)

    print("\nThe original household dataframe:")
    print(hhd_df)

    # Get the subset taking random households from each household size class possible
    subset_hhd_df = hhd_df.groupby("size", group_keys=False).apply(
    lambda group: group.sample(frac=proportion))

    # Delete original household data set
    del hhd_df

    print("\nThe subset generated:")
    print(subset_hhd_df)

    # Reorder the dataframe
    subset_hhd_df = subset_hhd_df.sort_index()

    print("\nThe subset generated reordered:")
    print(subset_hhd_df)

    # Create save_path_hhd
    save_path_hhd = get_path_to_folder("data")

    # Get proportion as a percentage and create the name of the file
    prop = proportion * 100
    prop = int(prop) 
    save_path_hhd = os.path.join(save_path_hhd, "Households_" + str(prop) + "%"  + ".csv")

    # Set index to ID
    subset_hhd_df = subset_hhd_df.set_index("ID")

    print("\nThe subset with ID as index:")
    print(subset_hhd_df)

    # Save the new data set file in CSV format
    subset_hhd_df.to_csv(save_path_hhd)
    print("\nThe new households data set was saved at:", save_path_hhd)

    # Delete subset
    del subset_hhd_df

if __name__ == "__main__":

    print(sys.argv)

    reduce_data(float(sys.argv[1]),
                sys.argv[2],
                sys.argv[3])