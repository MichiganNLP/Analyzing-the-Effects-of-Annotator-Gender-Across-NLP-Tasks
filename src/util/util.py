import pandas as pd

from src.config.data_columns import ANNOTATOR_ID_COL, GENDER_COL


def _multiple_gender_annotators(df: pd.DataFrame) -> pd.Series:
    genders_reported =  df.groupby(
        ANNOTATOR_ID_COL)[GENDER_COL].unique().apply(lambda x: len(x))
    return set(genders_reported[genders_reported != 1].index.tolist())


def remove_inconsistent_gender_annotators(df: pd.DataFrame) -> pd.DataFrame:
    return  df[~df[ANNOTATOR_ID_COL].isin(_multiple_gender_annotators(df))]
