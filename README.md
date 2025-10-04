# Procedures for Data Construction

This repository contains implementations of the procedures for data construction used in the context of my doctoral research.
The folder `subsets_real_data` have the procedure to obtain subsets from the real-world data sets as described in Section 4.1.4
of the thesis.
The folder `synthetic_data_generation` contains the implementation of the procedure that consider Gaussian mixture models (GMMs) 
and urban models to generate synthetic data sets, as described in Section 4.2.

## Installation

The methods are implemented in `Python 3.8.10`.

Clone the repository and install the remaining required dependencies:

```bash
git clone https://github.com/lucas-moschen/synthetic-data-construction.git
cd synthetic-data-construction
pip install -r requirements.txt
```

## Usage

### Subsetting real-world data sets

Firstly, since the complete data sets are non-public, it is necessary to insert them into the sub-directory
`subsets_real_data/data`.
Then, to extract the subsets, run

```bash
python3 reduce_data.py proportion name_dwe_df_file name_hhd_df_file
```

at the sub-directory `subsets_real_data/code`.

### Arguments:

`proportion` Proportion of the original data sets that the subsets must correspond to.

`name_dwe_df_file` Name of the file containing the complete dwelling data set.

`name_hhd_df_file` Name of the file containing the complete household data set. 

### Example:

```bash
python3 reduce_data.py 0.5 Houses_trier.csv Households_trier.csv
```

### Generating synthetic data sets

Firstly, the parameters for the GMM must be in JSON files located at `synthetic_data_generation/data/GMM_parameters`.
The name of these files must be `[name of municipality]_[addresses or hhd or houses or workplaces].json` according to
the type of the data sets that will be generated.

The parameter file for the data set of residential addresses must contains a list with the form 
`[list_of_address_features, probabilities, list_means_1, list_standard_deviations_1, list_correlations_1, ..., list_means_N, list_standard_deviations_N, list_correlations_N]`, where:

`list_of_address_features` The list of features that will be considered in the data set except for the IDs.

`probabilities` List containing the probability of a point to belong to each distribution of the GMM, i.e., 
of a residential address to belong to each nucleus of the urban model.

`list_means_i` List of means of distribution (nucleus) i.

`list_standard_deviations_i` List of standard deviations of distribution (nucleus) i.

`list_correlations_i` Correlation matrix of distribution (nucleus) i in "list of lists" (LIL) format.

The file with parameters for the workplace data set must have an analogous structure.
Finally, the parameter files for the household and dwelling data sets must have an analogous strucuture except 
for the list `probabilities`, which does not exists in these cases.

Then, the synthetic data sets can be generated with

```bash
python3 main.py municipality_name number_addresses proportion_workplaces number_dwellings number_households
```

at the sub-directory `synthetic_data_generation`.

### Arguments:

`municipality_name` Name of the synthetic municipality.

`number_addresses` Number of residential addresses within this municipality.

`proportion_workplaces` Proportion of the number of residential addresses that corresponds to the number of workplaces in the data set.

`number_dwellings` Number of dwellings within this municipality.

`number_households` Number of households within this municipality.

### Example:

With the parameter files at the sub-directory `synthetic_data_generation/data/GMM_parameters`, synthetic data sets with 20000 dwellings
and 18000 households can be generated with a GMM with 4 nuclei by running
 
```bash
python3 main.py city 15000 0.3 20000 18000
```

at the sub-directory `synthetic_data_generation`.
In this case, the municipality is called "city", it has initially 15000 residential addresses and a number of workplaces corresponding to 
30% of the number of addresses.

### Reproducing the synthetic data sets of the thesis:

The synthetic data sets generated for my doctoral reserach can be reproduced with

```bash
python3 main_reproduction.py number_dwellings number_households
```

at the sub-directory `synthetic_data_generation`.

### Arguments:

`number_dwellings` Number of dwellings of the data set.

`number_households` Number of households of the data set.

### Example:

The synthetic data set with 10000 dwellings and 9700 households can be generated with
 
```bash
python3 main_reproduction.py 10000 9700
```

at the sub-directory `synthetic_data_generation`.


## Repository Structure
```bash
synthetic-data-construction/
│
├── subsets_real_data/			# Subsetting real-world data sets
├── synthetic_data_generation/	# Synthetic data sets with GMMs and urban models
│
├── requirements.txt			# Dependencies
├── LICENSE				# License file (GPL-3.0)
├── CITATION.cff			# Citation file
├── AUTHORS				# List of contributors
└── README.md				# This file
```


## Citation
If you use this code, please cite the related article and thesis:
See `CITATION.cff` file.


## License
This repository is licensed under the GPL-3.0 License.


## Author
Lucas Moschen

Doctoral Researcher, University of Trier

See the `AUTHORS` file for a complete list of contributors.


## Acknowledgments

The synthetic data generation methodology implemented here was conceptually builds upon the ideas introduced in the work of Kendra M. Reiter, as cited in the associated thesis and article.
Parts of the modules `subsets_real_data/code/get_files.py` and `synthetic_data_generation/code/get_files.py` of this project are adapted from code in [msc-thesis-microsimulations](https://github.com/ReiterKM/msc-thesis-microsimulations) by Kendra M. Reiter, licensed under the GPL-3.0.
