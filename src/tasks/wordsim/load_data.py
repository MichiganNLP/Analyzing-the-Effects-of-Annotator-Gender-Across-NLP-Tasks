"""
Functions to load data for wordsim dataset
"""
import json

import pandas as pd

from src.config.data_columns import ANNOTATOR_ID_COL, GENDER_COL
from src.util import remove_inconsistent_gender_annotators
from src.tasks.wordsim.load_data_helpers import time_spent

CONFIG_FILE = "config/wordsim.json"
APPROVAL_COLUMN = "ApprovalTime"


COLUMN_MAPPING = {
    "WorkerId": ANNOTATOR_ID_COL,
    "Answer.gender": GENDER_COL,
}


def _load_country(country_code, **kwargs):
    with open(CONFIG_FILE) as f:
        us_path = json.load(f)["data_paths"][country_code]
    df = pd.read_csv(us_path)
    df = df[~df[APPROVAL_COLUMN].isna()]
    df.rename(columns=COLUMN_MAPPING, inplace=True)
    if kwargs.get("time_spent"):
        df["TimeSpent"] = time_spent(df)
    return df


def load_india(**kwargs):
    return _load_country("india", **kwargs)


def load_us(**kwargs):
    return _load_country("us", **kwargs)


def _load_gender(gender=None, **kwargs):
    us_data = load_us(**kwargs)
    india_data = load_india(**kwargs)
    df = pd.concat((us_data, india_data))
    return df[df[GENDER_COL] == gender]


def load_male(**kwargs):
    """
    Load male data as a pandas dataframe
    """
    return _load_gender("M", **kwargs)


def load_female(**kwargs):
    """
    Load female data as a pandas dataframe
    """
    return _load_gender("F", **kwargs)


def load_data(time_spent=False):
    df = pd.concat((load_male(time_spent=time_spent), 
        load_female(time_spent=time_spent)))
    df = remove_inconsistent_gender_annotators(df)
    return df.reset_index(drop=True)
