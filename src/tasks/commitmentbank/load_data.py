import json

import pandas as pd

from src.config.data_columns import ANNOTATOR_ID_COL, GENDER_COL, ITEM_ID_COL, \
    LABEL_COL
from src.util import remove_inconsistent_gender_annotators

COL_MAPPING = {
    "uID": ITEM_ID_COL, 
    "gender": GENDER_COL, 
    "AnonymizedWorkerID": ANNOTATOR_ID_COL, 
    "Answer": LABEL_COL
}

# NOTE: genders not covered: genderless, non-binary, one spam entry
GENDER_MAPPING = {
    "MALE": "M",
    "MALE+": "M",
    "FEMALE": "F",
    "WOMAN": "F",
    "FEMAL": "F",
    "FEMALLE": "F"
}


def _cleanup_gender(gender_col: pd.Series) -> pd.Series:
    gender_col = gender_col.str.upper()
    gender_col = gender_col.apply(
        lambda x: GENDER_MAPPING.get(x, x)).str.upper()
    return gender_col


def load_commitmentbank_data() -> pd.DataFrame:
    with open("config/commitmentbank.json") as f:
        data_path = json.load(f)["data_paths"]["data"]

    cb_df = pd.read_csv(data_path)
    cb_df.rename(columns=COL_MAPPING, inplace=True)
    cb_df = cb_df[COL_MAPPING.values()]
    cb_df[GENDER_COL] = _cleanup_gender(cb_df[GENDER_COL])

    # keep M/F (other classes are too small)
    cb_df = cb_df[cb_df[GENDER_COL].isin({"M", "F"})]

    # remove annotators who reported inconsistent gender (1 annotator)
    cb_df = remove_inconsistent_gender_annotators(cb_df)

    return cb_df
