import json

from src.tasks.affectivetext.config import SUBTASKS as EMOTION_SUBTASKS

DATA_FILES = "output/agreement/{task}/agreement_with_aggregate/raw_results_agreement_{aggregation}.json"
MEDIAN_COMPUTED_TASKS = ["wordsim_sim", "wordsim_rel", "sentiment", "commitmentbank"]
TASKS = MEDIAN_COMPUTED_TASKS + [f"affectivetext_{task}" for task in EMOTION_SUBTASKS]


def load_data(task):
    """
    Load saved annotator agreement data
    """
    aggregation = "median" if task in MEDIAN_COMPUTED_TASKS else "mean"
    with open(DATA_FILES.format(task=task, aggregation=aggregation)) as f:
        return json.load(f)
