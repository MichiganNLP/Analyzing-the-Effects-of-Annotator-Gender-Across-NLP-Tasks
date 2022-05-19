from functools import partial

import pandas as pd
from src.tasks.commitmentbank.demographics import create_demographics_map as create_cb_demographics_map
from src.tasks.commitmentbank.reliability_matrix import create_reliability_matrix as create_cb_reliability_matrix
from src.tasks.affectivetext.demographics import create_demographics_map as create_at_demographics_map
from src.tasks.affectivetext.reliability_matrix import create_reliability_matrix as create_at_reliability_matrix
from src.tasks.wordsim.demographics import create_demographics_map as create_wordsim_demographics_map
from src.tasks.wordsim.reliability_matrix import create_wordsim_reliability_matrix_sim
from src.tasks.sentiment.demographics import create_demographics_map as create_sentiment_demographics_map
from src.tasks.sentiment.reliability_matrix import create_reliability_matrix as create_sentiment_reliability_matrix


TASKS = {
    "affectivetext": "Affective Text",
    "wordsim": "Word Similarity",
    "sentiment": "Sentiment Analysis",
    "commitmentbank": "Natural Language Inference",
}


DEMOGRAPHICS_MAP_FNS = {
    "affectivetext": create_at_demographics_map,
    "wordsim": create_wordsim_demographics_map,
    "sentiment": create_sentiment_demographics_map,
    "commitmentbank": create_cb_demographics_map,
}


REL_MATRIX_FNS = {
    "affectivetext": partial(create_at_reliability_matrix, "anger"),
    "wordsim": create_wordsim_reliability_matrix_sim,
    "sentiment": create_sentiment_reliability_matrix,
    "commitmentbank": create_cb_reliability_matrix,
}


OUTPUT_COLS = ["Dataset", "# Male Annotators", "# Female Annotators",
               "# Datapoints", "Mean Annotations per Datapoint"]


def main():
    out_data = []
    for task, task_name in TASKS.items():
        dem_map = DEMOGRAPHICS_MAP_FNS[task]()
        n_male = len(dem_map["M"])
        n_female = len(dem_map["F"])
        rel_matrix = REL_MATRIX_FNS[task]()
        n_datapoints = len(rel_matrix.columns)
        avg_annotations_per_datapoint = rel_matrix.count().sum() / n_datapoints
        out_data.append((
            task_name,
            n_male,
            n_female,
            n_datapoints,
            avg_annotations_per_datapoint
        ))
    df = pd.DataFrame(out_data, columns=OUTPUT_COLS).set_index("Dataset")
    print(df.to_string())
        


if __name__ == "__main__":
    main()
