from src.config.data_columns import ANNOTATOR_ID_COL, ITEM_ID_COL, LABEL_COL
from src.tasks.commitmentbank.load_data import load_commitmentbank_data


def create_reliability_matrix():
    annotation_df = load_commitmentbank_data()
    return annotation_df.pivot_table(
        values=LABEL_COL, index=ANNOTATOR_ID_COL, columns=ITEM_ID_COL)
