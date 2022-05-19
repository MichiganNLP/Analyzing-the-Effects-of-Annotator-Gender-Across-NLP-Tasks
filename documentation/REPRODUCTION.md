# Reproducing Our Results
This file contains information on how to reproduce our results, and how to 

## Configuration
### Python Setup
The code in this repository was run with python 3.9.0. All scripts require that the PYTHONPATH is set to the root directory of the repository.

Install the required libraries by running `pip install -r requirements.txt`.

### Computational Resources
The code was run on a computer with 16GB of RAM (no GPU required).  
The agreement computation script provides an option to run with multiple processes, if desired.

### Data
Please see [this README](../config/README.md) for information on how to get access to the datasets included in the paper (where possible) and how to write configuration files that indicate where necessary files are stored on your computer.

If you would like to analyze __new datasets__, please see [NEW_DATA.md](NEW_DATA.md)

## Reproduction Steps
These reproduction steps assume that you have access to all of the necessary data and have already followed the aforementioned configuration steps.
### Data Summary
#### Table 1
To reproduce Table 1 (data summary) use the following command:
```bash
PYTHONPATH=. python src/scripts/lrec_data_summary.py
```
_This reproduces the numerical data in the table; some additional data is added. The output table is human-readable (not LaTeX)._


### Distribution Analysis
### Figure 2 & Figure 3
Use the following command to recreate Figures 2 and 3:
```bash
PYTHONPATH=. python src/scripts/distributions/distribution_plot.py
```
_The figures will be saved to output/distribution/combo/kde\_distribution.pdf (Figure 2) and output/distribution/combo/kde\_distribution.pdf (Figure 3)_

### Table 2
Use the following command to recreate Table 2:
```bash
PYTHONPATH=. python src/scripts/distributions/significance_table.py
```
_**NOTE**: this runs all of the permutation tests, and therefore may be slow._  
_The LaTeX table will be saved to output/range/combo/significance.txt_

### Agreement Analysis
First, run [src/scripts/agreement/compute_agreements.py](../src/scripts/agreement/compute_agreements.py). This script (a) stores data about agreement metrics for later use and (b) creates figures for single tasks. The figures and tables in the paper include multiple tasks, so require running additional scripts, which read the saved data from this script.

We have provided a bash script that runs the python script with all settings shown in the paper. It should be run from the root directory of the repository, and can be referenced to see how to run the python script for an individual task. You may choose to add the argument `--n_processes {num_processes_desired}` if you want to run with more than one process.
```bash
./src/scripts/agreement/compute_all_agreements.sh
```
#### Figure 4
To create the figure, run the following:
```bash
PYTHONPATH=. python src/scripts/agreement/agreement_plot.py --use_median
```
_The figure will be saved to output/agreement/combo/agreement\_plot\_with\_medians.pdf_

#### Table 3
To create the table, run the following:
```bash
PYTHONPATH=. python src/scripts/agreement/significance_table.py
```
_The LaTeX table will be saved to output/agreement/combo/significance.txt_
