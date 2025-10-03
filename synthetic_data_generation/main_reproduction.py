# Main script to replicate synthetic data sets generated for the thesis

from code.create_gmm_data_hhd import create_initial_hhd_data
from code.create_gmm_data_dwe import create_initial_dwe_data
from code.create_final_datasets_from_initial_ones import create_final_data
import sys

print(sys.argv)

# Data set with 10000 dwellings 
if int(sys.argv[1]) == 10000:

    # 7000 households
    if int(sys.argv[2]) == 7000:

        amount_addresses = 3450 
        proportion_workplaces = 0.2

    # 8000 households                            
    if int(sys.argv[2]) == 8000:

        amount_addresses = 3450 
        proportion_workplaces = 0.25

    # 9000 households
    if int(sys.argv[2]) == 9000:

        amount_addresses = 3450
        proportion_workplaces = 0.3

    # 9700 households
    if int(sys.argv[2]) == 9700:

        amount_addresses = 3450
        proportion_workplaces = 0.3

# Data set with 15000 dwellings and 14500 households
if int(sys.argv[1]) == 15000:

    if int(sys.argv[2]) == 14500:

        amount_addresses = 5175
        proportion_workplaces = 0.3

# Data set with 25000 dwellings and 24250 households
if int(sys.argv[1]) == 25000:

    if int(sys.argv[2]) == 24250:

        amount_addresses = 10000
        proportion_workplaces = 0.3

# Data set with 50000 dwellings and 48500 households
if int(sys.argv[1]) == 50000:

    if int(sys.argv[2]) == 48500:

        amount_addresses = 17250
        proportion_workplaces = 0.3

# Data set with 100000 dwellings and 97000 households
if int(sys.argv[1]) == 100000:

    if int(sys.argv[2]) == 97000:

        amount_addresses = 34500
        proportion_workplaces = 0.3

# Generate initial household data set
create_initial_hhd_data(amount_addresses = amount_addresses, 
                        proportion_workplaces = proportion_workplaces,
                        city_name = "city",
                        param_path="data/GMM_parameters_reproduction/" + str(sys.argv[1]) + "_dwe_" + str(sys.argv[2]) + "_hhd",
                        data_path="data/datasets/initial")

# Generate initial dwelling data set
create_initial_dwe_data(amount_addresses = amount_addresses, 
                        proportion_workplaces = proportion_workplaces,
                        city_name = "city",
                        param_path="data/GMM_parameters_reproduction/" + str(sys.argv[1]) + "_dwe_" + str(sys.argv[2]) + "_hhd",
                        data_path="data/datasets/initial")

# Generate final data sets
create_final_data(initial_dwe_df_name = "Houses_city" + str(amount_addresses) + "addr(" + str(int(proportion_workplaces * 100)) + "%workplaces)seed=10.csv",
                    initial_hhd_df_name = "Households_city" + str(amount_addresses) + "addr(" + str(int(proportion_workplaces * 100)) + "%workplaces)seed=10.csv",
                    amount_dwe = int(sys.argv[1]),
                    amount_hhd = int(sys.argv[2]),
                    final_dwe_df_name = "Houses_city" + str(sys.argv[1]) + "(" + str(sys.argv[2]) + "hhd)seed=10.csv",
                    final_hhd_df_name = "Households_city" + str(sys.argv[1]) + "(" + str(sys.argv[2]) + "hhd)seed=10.csv")