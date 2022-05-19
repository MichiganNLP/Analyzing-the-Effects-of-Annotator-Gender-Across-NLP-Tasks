"""
This file configures functions that should be used to load data for each task.
To add a new task, you must add a function to the following maps:
* DEMOGRAPHICS_FN_MATRIX_MAP: a function to call to get a map of demographic (e.g. M = male) -> a list of annotator IDs
* REALIABILITY_FN_MATRIX_MAP: a function to call to get a reliability matrix. Columns are items in the dataset and rows are annotator IDs
                              if an annotator didn't annotate and item, fill with np.nan
"""
from functools import partial

from src.tasks.commitmentbank.demographics import create_demographics_map as create_cb_demographics_map
from src.tasks.commitmentbank.reliability_matrix import create_reliability_matrix as create_cb_reliability_matrix
from src.tasks.affectivetext.config import SUBTASKS as AFFECTIVE_TEXT_SUBTASKS
from src.tasks.affectivetext.demographics import create_demographics_map as create_at_demographics_map
from src.tasks.affectivetext.reliability_matrix import create_reliability_matrix as create_at_reliability_matrix
from src.tasks.sentiment.demographics import create_demographics_map as create_sentiment_demographics_map
from src.tasks.sentiment.reliability_matrix import create_reliability_matrix as create_sentiment_reliability_matrix
from src.tasks.wordsim.demographics import create_demographics_map as create_wordsim_demographics_map
from src.tasks.wordsim.reliability_matrix import create_wordsim_reliability_matrix_rel, create_wordsim_reliability_matrix_sim


DEMOGRAPHICS_FN_MATRIX_MAP = {
    "wordsim_rel": create_wordsim_demographics_map,
    "wordsim_sim": create_wordsim_demographics_map,
    "sentiment": create_sentiment_demographics_map,
    "commitmentbank": create_cb_demographics_map,
} | {
    f"affectivetext_{subtask}": create_at_demographics_map
    for subtask in AFFECTIVE_TEXT_SUBTASKS
}


REALIABILITY_FN_MATRIX_MAP = {
    "wordsim_rel": create_wordsim_reliability_matrix_rel,
    "wordsim_sim": create_wordsim_reliability_matrix_sim,
    "sentiment": create_sentiment_reliability_matrix,
    "commitmentbank": create_cb_reliability_matrix,
} | {
    f"affectivetext_{subtask}": partial(create_at_reliability_matrix, subtask)
    for subtask in AFFECTIVE_TEXT_SUBTASKS
}
