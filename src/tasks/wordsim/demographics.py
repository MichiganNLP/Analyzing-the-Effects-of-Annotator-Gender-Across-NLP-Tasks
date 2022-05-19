from typing import Dict, List

from src.config.data_columns import ANNOTATOR_ID_COL, GENDER_COL
from src.tasks.wordsim.load_data import load_data


def create_demographics_map() -> Dict[str, List[str]]:
    data = load_data()
    demographics = {gender: 
    list(set(data[data[GENDER_COL] == gender][ANNOTATOR_ID_COL].tolist()))
                    for gender in data[GENDER_COL].unique()}
    return demographics
