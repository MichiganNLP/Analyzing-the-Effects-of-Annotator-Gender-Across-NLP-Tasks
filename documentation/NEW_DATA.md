### Adding New Data

We have attempted to make it easy to add a new dataset without significant code changes. These steps can be followed to add a new datasets for analysis:

1. Add a configuration file in [config/](../config/) to specify where to find your data on your computer.
2. Write data loading functions, of which there are examples in [src/tasks/](../src/tasks/). 
   * Reliability matrix function: this function produces a reliability matrix, as needed for Krippendorff's alpha. The matrix should be in the form of a pandas dataframe `rel`, where the index is each annotator ID and the columns are IDs for each item in the dataset. For annotator `i` and item `j`, `rel.loc[i, j]` should be the rating that annotator _i_ gave to item _j_. If annotator _i_ did not annotate item _j_, the value should be NaN.  
   An example of the first five columns of the Affective Text annotations for Anger is given for reference below:
   ```
        item_id       500  501  502  503  504
        annotator_id                         
        F1              0   52    0    0    0
        F2              0   30    0    0    0
        F3              0    0    0    0    0
        M1              0   10    0    0    5
        M2              0    0    0    0    0
        M3              0   50    0    0    0
   ```
   * Demographics function: this function returns a dictionary mapping gender (or another demographic attribute you would like to study) to a list of annotator IDs. It should have the following form:
   ```
    {
        "M": ["M_1", "M_2", ..., "M_n"],
        "F": ["F_1", "F_2", ..., "F_n"]
    }
   ```
3. Add your data loading functions to `DEMOGRAPHICS_FN_MATRIX_MAP` and `REALIABILITY_FN_MATRIX_MAP` in [`src/config/data.py`](../src/config/data.py).
4. (Optional): add your task to `TASK_ID_TO_NAME` in [`src/config/task_names.py`](../src/config/task_names.py) to show a differently formatted string than the ID you are using for your task when plotting/displaying in a table.

#### For distribution analysis
1. Add your task to [`src/config/distribution.py`](../src/config/distribution.py).
   * If the annotations are ordinal, the `annotation_type` should be `"ordinal"`; if they are on an interval, it should be `"interval"`.
   * For interval tasks, you will need to specify `min_val` and `max_val`.
   * For ordinal tasks, you will need to specify which columns are to be compared in permutation testing by providing a list in `compare_cols`. You will want to specify this after plotting.
2. You will need to update the size of the plot in [`src/scripts/distributions/distribution_plot.py`](../src/scripts/distributions/distribution_plot.py) to include your new data in the plot.
 
#### For agreement analysis
1. Add configuration to specify which agreement measure should be used for your task in [`src/config/agreement.py`](../src/config/agreement.py). The agreement function must work with a reliability matrix.
2. Run [`src/scripts/agreement/compute_agreements.py`](../src/scripts/agreement/compute_agreements.py)
   * Optionally, you may choose to add your task to [`src/scripts/agreement/compute_all_agreements.sh`](../src/scripts/agreement/compute_all_agreements.sh)
3. Add your task to `MEDIAN_COMPUTED_TASKS` in [`src/scripts/agreement/util.py`](../src/scripts/agreement/util.py) if you have computed the median; otherwise only add to `TASKS`.
4. You will need to update the size of the plot in [`src/scripts/agreement/agreement_plot.py`](../src/scripts/agreement/agreement_plot.py) to include your new data in the plot.
