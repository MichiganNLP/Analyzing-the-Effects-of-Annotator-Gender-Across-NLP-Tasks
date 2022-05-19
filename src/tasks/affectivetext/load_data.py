# coding: utf-8
import json
import os

import pandas as pd

from src.config.data_columns import ANNOTATOR_ID_COL, GENDER_COL, ITEM_ID_COL, ITEM_TEXT_COL, LABEL_COL

EMOTION_COLS = ["anger", "disgust", "fear", "joy", "sadness", "surprise", "valence"]
ALL_COLS = [ITEM_ID_COL] + EMOTION_COLS


def load_full_df():
    with open("config/affectivetext.json") as f:
        data_paths = json.load(f)["data_paths"]
        annotations_dir = data_paths["annotations_dir"]
        affective_text_path = data_paths["affective_text"]

    all_annotator_df = []
    for annotator_txt in os.listdir(annotations_dir): # loop through all annotator txt files in path
        annotator_data = pd.read_csv(os.path.join(annotations_dir, annotator_txt), names=ALL_COLS, sep="\s", engine='python') # each emotion score in a separate column
        annotator_name = annotator_txt.split(".")[0]
        annotator_data[ANNOTATOR_ID_COL] = annotator_name # gets the name of the annotator
        annotator_data[GENDER_COL] = annotator_name[0]
        all_annotator_df.append(annotator_data) # list of dfs with annotator id, gender col, emotion cols with each emotion
    annotation_df = pd.concat(all_annotator_df)
    text_df = pd.read_xml(affective_text_path, parser="etree", names=[ITEM_ID_COL, ITEM_TEXT_COL])
    annotation_df.join(text_df, on=ITEM_ID_COL, rsuffix="_drop")
    return annotation_df.merge(text_df, on=ITEM_ID_COL)


def _build_emo_column_slice(emotion):
    return [ANNOTATOR_ID_COL, GENDER_COL, ITEM_ID_COL, ITEM_TEXT_COL, emotion]


def load_emotion_data(emotion: str):
    complete_annotator_df = load_full_df()
    if emotion in EMOTION_COLS:
        emotion_df = complete_annotator_df.loc[:, _build_emo_column_slice(emotion)]
        emotion_df = emotion_df.rename(columns={emotion: LABEL_COL})
    else:
        raise Exception(f"Invalid emotion: {emotion}")
    return emotion_df


def load_test(emotion: str):
    return load_emotion_data(emotion).head(1500)


def load_train(emotion: str):
    return load_emotion_data(emotion).tail(4500)
