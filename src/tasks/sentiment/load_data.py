import json

import pandas as pd

from src.config.data_columns import ANNOTATOR_ID_COL, GENDER_COL, ITEM_ID_COL, ITEM_TEXT_COL, LABEL_COL


CONFIG_FILE = "config/sentiment.json"
CSV_GENDER_COL = "Please indicate your gender"


COL_MAPPING = {
    "annotation": LABEL_COL,
    "respondent_id": ANNOTATOR_ID_COL,
    "Please indicate your gender": GENDER_COL,
    "unit_id": ITEM_ID_COL,
    "unit_text": ITEM_TEXT_COL,
}

RESPONSE_MAP = {
    "Very positive": 4,
    "Somewhat positive": 3,
    "Neutral": 2,
    "Somewhat negative": 1,
    "Very negative": 0
}


def _map_response(response: str) -> int:
    return RESPONSE_MAP[response]


def _get_data_path(path_name: str) -> str:
    with open(CONFIG_FILE) as f:
        return json.load(f)["data_paths"][path_name]


def _merge_demographics(sentiment_data: pd.DataFrame) -> pd.DataFrame:
    # add gender column to data
    demographics_data = pd.read_csv(_get_data_path("demographics"), usecols=["respondent_id", CSV_GENDER_COL])
    demographics_data.rename(columns=COL_MAPPING, inplace=True)
    demographics_data[GENDER_COL] = demographics_data[GENDER_COL].str[:1]
    merged_demographics = pd.merge(sentiment_data, demographics_data, on=ANNOTATOR_ID_COL)
    
    # there is only one nonbinary annotator who cannot be modeled - reduce to M/F
    merged_demographics = merged_demographics[merged_demographics[GENDER_COL].isin({"M", "F"})]
    return merged_demographics


def _load_sentiment(train_or_test: str) -> pd.DataFrame:
    sentiment_data = pd.read_csv(_get_data_path(train_or_test), encoding="ISO-8859-1")
    sentiment_data["annotation"] = sentiment_data["annotation"].apply(_map_response)
    sentiment_data.rename(columns=COL_MAPPING, inplace=True)
    return sentiment_data


def load_train():
    return _merge_demographics(_load_sentiment("train"))[COL_MAPPING.values()]


def load_test():
    return _merge_demographics(_load_sentiment("test"))[COL_MAPPING.values()]
