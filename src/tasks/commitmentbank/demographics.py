from src.config.data_columns import ANNOTATOR_ID_COL, GENDER_COL
from src.tasks.commitmentbank.load_data import load_commitmentbank_data


def create_demographics_map():
    df = load_commitmentbank_data()
    return df.groupby(GENDER_COL).agg(set)[ANNOTATOR_ID_COL].to_dict()
