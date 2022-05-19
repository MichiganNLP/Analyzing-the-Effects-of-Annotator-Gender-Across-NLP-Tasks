import pandas as pd

from src.config.data_columns import ANNOTATOR_ID_COL, GENDER_COL
from src.tasks.sentiment.load_data import load_test, load_train


def create_demographics_map():
    data = pd.concat((load_train(), load_test()))
    demographics = {gender: data[data[GENDER_COL] == gender][ANNOTATOR_ID_COL].unique().tolist()
                    for gender in data[GENDER_COL].unique()}
    return demographics
