# Main script to generate synthetic data sets

from code.create_gmm_data_hhd import create_initial_hhd_data
from code.create_gmm_data_dwe import create_initial_dwe_data
from code.create_final_datasets_from_initial_ones import create_final_data
import sys

print(sys.argv)

city_name = sys.argv[1]
amount_addresses = int(sys.argv[2])
proportion_workplaces = float(sys.argv[3])

# Generate initial household data set
create_initial_hhd_data(amount_addresses = amount_addresses, 
                        proportion_workplaces = proportion_workplaces,
                        city_name = city_name,
                        param_path="data/GMM_parameters/",
                        data_path="data/datasets/initial")

# Generate initial dwelling data set
create_initial_dwe_data(amount_addresses = amount_addresses, 
                        proportion_workplaces = proportion_workplaces,
                        city_name = city_name,
                        param_path="data/GMM_parameters/",
                        data_path="data/datasets/initial")

# Generate final data sets
create_final_data(initial_dwe_df_name = "Houses_" + city_name + str(amount_addresses) + "addr(" + str(int(proportion_workplaces * 100)) + "%workplaces)seed=10.csv",
                    initial_hhd_df_name = "Households_" + city_name + str(amount_addresses) + "addr(" + str(int(proportion_workplaces * 100)) + "%workplaces)seed=10.csv",
                    amount_dwe = int(sys.argv[4]),
                    amount_hhd = int(sys.argv[5]),
                    final_dwe_df_name = "Houses_" + city_name + str(sys.argv[4]) + "(" + str(sys.argv[5]) + "hhd)seed=10.csv",
                    final_hhd_df_name = "Households_" + city_name + str(sys.argv[4]) + "(" + str(sys.argv[5]) + "hhd)seed=10.csv")