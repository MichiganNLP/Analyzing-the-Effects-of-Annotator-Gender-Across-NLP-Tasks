from collections import defaultdict

import numpy as np
import pandas as pd

from src.config.data_columns import ANNOTATOR_ID_COL
from src.tasks.wordsim.load_data import load_data


def create_reliability_matrix(df: pd.DataFrame, measure: str):
    input_a_fmt = "Input.Act_{}A"
    input_b_fmt = "Input.Act_{}B"
    sim_rel_fmt = "Answer.{}_{}"
    pair_to_idx = {}
    for _, row in df.iterrows():
        for i in range(1, 26):
            pair = (row[input_a_fmt.format(i)], row[input_b_fmt.format(i)])
            if pair not in pair_to_idx:
                pair_to_idx[pair] = len(pair_to_idx)
    
    def init_nan():
        array = np.empty(len(pair_to_idx))
        array[:] = np.NaN
        return array

    worker_annotations = defaultdict(init_nan)
    
    for _, row in df.iterrows():
        for i in range(1, 26):
            pair = (row[input_a_fmt.format(i)], row[input_b_fmt.format(i)])
            if pair not in pair_to_idx:
                pair_to_idx[pair] = len(pair_to_idx)
            worker_annotations[row[ANNOTATOR_ID_COL]][pair_to_idx[pair]] = row[sim_rel_fmt.format(measure, i)]
            
    columns = [x[0] for x in sorted(pair_to_idx.items(), key=lambda x: x[1])]
    return pd.DataFrame.from_dict(worker_annotations, orient="index", columns=columns)

def create_wordsim_reliability_matrix_rel():
    data = load_data(time_spent=True)
    return create_reliability_matrix(data, "rel")


def create_wordsim_reliability_matrix_sim():
    data = load_data(time_spent=True)
    return create_reliability_matrix(data, "sim")
