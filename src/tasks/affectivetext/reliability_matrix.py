from src.config.data_columns import ANNOTATOR_ID_COL, ITEM_ID_COL, LABEL_COL
from src.tasks.affectivetext.load_data import load_emotion_data


def create_reliability_matrix(emotion: str):
    annotation_df = load_emotion_data(emotion)
    return annotation_df.pivot_table(
        values=LABEL_COL, index=ANNOTATOR_ID_COL, columns=ITEM_ID_COL)
