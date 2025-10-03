# -*- coding: utf-8 -*-
"""
@author: Lucas Moschen

This script generates the initial dwelling data set with the procedure shown in
Section 4.2 of the thesis.
"""

import numpy as np
import pandas as pd
import json 
from code.get_files import get_path_to_folder

def gmm_address(data_size: int, list_parameters: list):

    """
    This function generates the data set of residential addresses using GMM.

    Parameters
    ----------
    data_size: int
        Number of elements in the data set that will be generated.
        
    list_parameters : list
        It must have the form [list_of_characteristics_considered, probabilities, 
        list_means_1, list_standard_deviations_1, list_correlations_1, ..., 
        list_means_N, list_standard_deviations_N, list_correlations_N], where:
        * list_of_characteristics_considered is the list of characteristics that we will 
          consider in the data set except for the IDs;
        * probabilities is the list containing the probability of a point to belong to 
          each distribution of the GMM, i.e., of a residential address to belong to each 
          nucleus of the urban model;  
        * list_means_i is the list of means of distribution (nucleus) i; 
        * list_standard_deviations_i is the list of standard deviations of distribution (nucleus) i;
        * list_correlations_i is the correlation matrix of distribution (nucleus) i in 
          "list of lists" (LIL) format.

    Returns
    -------
    df : dataframe
        The generated data set.
    """

    # Get input
    w = list_parameters[1]
    num_nucleus = len(w) 
    select_nucleus = np.random.uniform(low=0.0, high=1.0,size=data_size)
    num_characteristics = len(list_parameters[0])
    
    # Build the list of selected nuclei
    nuclei_selected = []
    for i in select_nucleus:
        upper = w[0]
        index = 0
        found = False 
        while found == False: 
            if i <= upper: 
                nuclei_selected.append(index)  
                found = True 
            else: 
                index += 1
                upper += w[index]
                
    # Build a list containing the cholesky factorizations of the covariance matrices
    list_cholesky = []
    for i in range(num_nucleus):
        
        # Create the diagonal matrix of standard deviations
        sd_matrix = np.zeros((num_characteristics, num_characteristics))
        for j in range(num_characteristics):
            sd_matrix[j,j] = round(list_parameters[(3*i)+3][j], 2) 
        
        # Get the covariance matrix and store the matrix from its cholesky factorization
        cov = sd_matrix @ np.array(list_parameters[(3*i)+4]) @ sd_matrix
        q = np.linalg.cholesky(cov) 
        list_cholesky.append(q)    
        
    # Initialize dataframe and ID count
    df = []
    id = 0
    
    # Generate the elements of the data set
    for j in nuclei_selected:

        # Get a vector from the standard Gaussian distribution
        z = np.random.normal(size=num_characteristics) 

        # Transform into the Gaussian distribution with parameters associated to nucleus j
        # (this x stores the observation in a vector where the sequence of values follows the sequence 
        # of characteristics inserted in the parameters of the input)
        x = (list_cholesky[j] @ z) + list_parameters[(3*j) + 2]    
        
        # Transform the numpy arrays into lists
        x = list(x) 
        
        # Insert ID and nucleus number into x 
        x.insert(0, id)
        x.append(j)

        # Insert x into the dataframe
        df.append(x) 

        # Update ID count 
        id += 1  
        
    # Initialize the head of the dataframe
    characteristics = list_parameters[0].copy() 
    characteristics.insert(0, "ID")
    characteristics.append("Cluster Nr.")

    # Identify the coordinates of the input corresponding to lables X and Y
    for j in range(len(characteristics)):
        if characteristics[j] == "X":
            x_coor = j 
        if characteristics[j] == "Y":
            y_coor = j 
    
    # Round some necessary values for the dataframe and insert grid cell information
    for vector in df: 

        # Treat information on amount of dwellings per building
        vector[3] = int(round(vector[3]))
        if vector[3] <= 0:
            vector[3] = 1
        
        # Insert grid cell labels and information on its lower-left corner coordinates
        grid_cell_name = "100mN" + str(round(vector[y_coor] - (vector[y_coor] % 100))) + "E" + str(round(vector[x_coor] - (vector[x_coor] % 100)))
        vector.append(grid_cell_name)
        vector.append(round(vector[x_coor] - (vector[x_coor] % 100)))
        vector.append(round(vector[y_coor] - (vector[y_coor] % 100)))

    # Insert more information into the head of the dataframe    
    characteristics.append("Gitter_ID_100m")
    characteristics.append("coord_x_grid")
    characteristics.append("coord_y_grid")
        
    # Generate dataframe
    df = pd.DataFrame(df, columns = characteristics)    
    
    return df  

def gmm_dwelling(address_data, list_parameters: list):

    """
    This function generates the dwelling data set from the address data set using 
    Gaussian distributions that consider the inserted parameters.

    Parameters
    ----------
    address_data: dataframe
        Dataframe containing the address data set.
        
    list_parameters : list
        It must have the form [list_of_characteristics_considered, probabilities, 
        list_means_1, list_standard_deviations_1, list_correlations_1, ..., 
        list_means_N, list_standard_deviations_N, list_correlations_N], where:
        * list_of_characteristics_considered is the list of characteristics that we will 
          consider in the data set except for the IDs;
        * probabilities is the list containing the probability of a point to belong to 
          each distribution of the GMM, i.e., of a residential address to belong to each 
          nucleus of the urban model;  
        * list_means_i is the list of means of distribution (nucleus) i; 
        * list_standard_deviations_i is the list of standard deviations of distribution (nucleus) i;
        * list_correlations_i is the correlation matrix of distribution (nucleus) i in 
          "list of lists" (LIL) format.

    Returns
    -------
    df : dataframe
        The generated data set.
    """

    # Get input
    num_characteristics = len(list_parameters[0])

    # Define the number of nuclei
    num_nucleus = int((len(list_parameters)-1)/3) 
                
    # Build a list containing the cholesky factorizations of the covariance matrices
    list_cholesky = []
    for i in range(num_nucleus):
        
        # Get the diagonal matrix of standard deviations
        sd_matrix = np.zeros((num_characteristics, num_characteristics))
        for j in range(num_characteristics):
            sd_matrix[j,j] = round(list_parameters[(3*i)+2][j], 2) 
        
        # Get covariance matrix
        cov = sd_matrix @ np.array(list_parameters[(3*i)+3]) @ sd_matrix
        
        # Get and store matrix from cholesky factorization
        q = np.linalg.cholesky(cov) 
        list_cholesky.append(q)   
        
    # Initialize dataframe
    df = []
    
    # Generate the elements of the data set
    for index, row in address_data.iterrows():
        
        for i in range(row["amount of dwellings per building"]):

            # Initialize row of the data set
            dwelling_line = [] 

            # Insert ID with the form [building ID]_[index of dwelling in this building]
            dwelling_line.append(str(row["ID"]) + "_" + str(i))

            # Insert spatial coordinates
            dwelling_line.append(row["X"])
            dwelling_line.append(row["Y"])

            # Get vector from standard Gaussian distribution
            z = np.random.normal(size=num_characteristics) 

            # Get vector from Gaussian distribution corresponding to features [cost, size]
            x = (list_cholesky[row["Cluster Nr."]] @ z) + list_parameters[(3*row["Cluster Nr."]) + 1]

            # Insert cost and size to row
            dwelling_line.append(x[0])
            dwelling_line.append(x[1])  

            # Inset remaining information from the building
            dwelling_line.append(row["Gitter_ID_100m"])
            dwelling_line.append(row["coord_x_grid"]) 
            dwelling_line.append(row["coord_y_grid"]) 
            dwelling_line.append(row["Cluster Nr."]) 

            # Update the dataframe
            df.append(dwelling_line)  
        
    # Generate the head of the data set
    characteristics = list_parameters[0].copy() 
    characteristics.insert(0, "ID")
    characteristics.insert(1, "X")
    characteristics.insert(2, "Y")
    characteristics.append("Gitter_ID_100m")
    characteristics.append("coord_x_grid") 
    characteristics.append("coord_y_grid") 
    characteristics.append("Cluster Nr.") 
    
    # Treat values of cost and size
    for vector in df:

        vector[3] = round(vector[3], 2)    #cost
        vector[4] = int(round(vector[4]))  #size

        if vector[4] <= 0:
            vector[4] = 1

    # Create the dataframe
    df = pd.DataFrame(df, columns = characteristics)    
    
    return df

def create_initial_dwe_data(amount_addresses: int, 
                            proportion_workplaces: float, 
                            param_path: str = "data/GMM_parameters",
                            city_name: str = None,
                            data_path: str = "data/datasets"):
    """
    This function takes a file containing the list of GMM parameters and generates the dwelling data set.

    Parameters
    ----------
    amount_addresses: int
        Amount of residential addresses in the data set.
        
    proportion_workplaces: float
        Proportion of the number of residential addresses that corresponds to the number of workplaces 
        in the data set.
        
    param_path : str, optional
        Sub-directory to find the JSON files containing the GMM parameters. 
        It must start at one level above the current file. 
        The default is "data/GMM_parameters".
        
    city_name: str, optional
        Name of the municipality created. 
        The title of the JSON files must be "[name of city]_[addresses or houses].json".
        The default is None.
        
    data_path: str, optional
        Path to save the data sets created.
        The default is "data/datasets".

    Returns
    -------
    None.
    
    """

    # Set seed
    seed_value = 10
    np.random.seed(seed_value)
    
    # Get full paths
    param_path = get_path_to_folder(param_path)
    data_path = get_path_to_folder(data_path) 
    
    # Get path to parameters for the data set of residential addresses and import them
    complete_param_path_addr = param_path + "/" + city_name + "_addresses.json"
    with open(complete_param_path_addr, encoding = "utf-8") as t:
        list_param_addr = json.load(t)
        
    # Generate data set of residential addresses   
    df_addr = gmm_address(amount_addresses, list_param_addr)
    
    # Use specific information to update the path to the data set
    data_path_addr = data_path + "/Addresses_" + str(city_name) + str(amount_addresses) + "addr" + "(" + str(int(proportion_workplaces * 100)) + "%workplaces)"+ "seed=" + str(seed_value) + ".csv"
    
    # Save data set in CSV file
    df_addr.to_csv(data_path_addr, index=False) 
    print("\nThe new data set of residential addresses was saved at:", data_path_addr)

    # Get path to parameters for the dwelling data set and import them
    complete_param_path_dwe = param_path + "/" + city_name + "_houses.json"
    with open(complete_param_path_dwe, encoding = "utf-8") as t:
        list_param_dwe = json.load(t)
        
    # Generate dwelling data set   
    df_dwe = gmm_dwelling(address_data= df_addr, list_parameters= list_param_dwe)    
    
    # Use specific information to update the path to the data set
    data_path_dwe = data_path + "/Houses_" + str(city_name) + str(amount_addresses) + "addr" + "(" + str(int(proportion_workplaces * 100)) + "%workplaces)"+ "seed=" + str(seed_value) + ".csv"
    
    # Save the data set in CSV file
    df_dwe.to_csv(data_path_dwe, index=False) 
    print("\nThe new dwelling data set was saved at:", data_path_dwe)