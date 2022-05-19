from collections import defaultdict

import numpy as np
import pandas as pd

from src.config.data_columns import ANNOTATOR_ID_COL, ITEM_ID_COL, LABEL_COL
from src.tasks.sentiment.load_data import load_test, load_train


def create_reliability_matrix():
    data = pd.concat((load_train(), load_test()))
    unit_ids = sorted(data[ITEM_ID_COL].unique())

    def init_nan():
        array = np.empty(len(unit_ids))
        array[:] = np.NaN
        return array

    unit_id_to_idx = {unit_id: idx for idx, unit_id in enumerate(unit_ids)}

    worker_annotations = defaultdict(init_nan)
    for _, row in data.iterrows():
        worker_annotations[row[ANNOTATOR_ID_COL]][unit_id_to_idx[row[ITEM_ID_COL]]] = row[LABEL_COL]

    return pd.DataFrame.from_dict(worker_annotations, orient="index", columns=unit_ids)
