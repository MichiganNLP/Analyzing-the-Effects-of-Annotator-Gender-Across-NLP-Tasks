"""
This dictionary configures which tasks are plotted in src/scripts/distributions/distribution_plot.py.
Barplots are used if annotation_type is ordinal, otherwise KDE plots are used
"""
DISTRIBUTION_CONFIG = {
    "wordsim_sim": {
        "annotation_type": "ordinal",
        "compare_cols": [2, 3, 4],
    },
    "wordsim_rel": {
        "annotation_type": "ordinal",
        "compare_cols": [2, 3, 4],
    },
    "sentiment": {
        "annotation_type": "ordinal",
        "compare_cols": [1, 3],
    },
    "commitmentbank": {
        "annotation_type": "ordinal",
        "compare_cols": [4, 5, 6],
    },
    "affectivetext_valence": {
        "annotation_type": "interval",
        "min_val": -100,
        "max_val": 100
    },
    "affectivetext_anger": {
        "annotation_type": "interval",
        "min_val": 0,
        "max_val": 100
    },
    "affectivetext_disgust": {
        "annotation_type": "interval",
        "min_val": 0,
        "max_val": 100
    },
    "affectivetext_fear": {
        "annotation_type": "interval",
        "min_val": 0,
        "max_val": 100
    },
    "affectivetext_joy": {
        "annotation_type": "interval",
        "min_val": 0,
        "max_val": 100
    },
    "affectivetext_sadness": {
        "annotation_type": "interval",
        "min_val": 0,
        "max_val": 100
    },
    "affectivetext_surprise": {
        "annotation_type": "interval",
        "min_val": 0,
        "max_val": 100
    }
}