"""
Utility functions to compute Cohen's Kappa/Fleiss' Kappa from a reliability matrix
Allows for consistency in code with Krippendorff's Alpha

NOTE: this is not used in the paper, but we provide it for completeness
"""
from sklearn.metrics import cohen_kappa_score
from statsmodels.stats.inter_rater import fleiss_kappa


def cohen_kappa_reliability_matrix(labels, reliability_matrix):
    assert len(reliability_matrix) == 2, "reliability matrix must have 2 rows for Cohen's Kappa"
    return cohen_kappa_score(reliability_matrix.iloc[0].to_list(), reliability_matrix.iloc[1].to_list(), 
                             labels=labels)


def fleiss_kappa_reliability_matrix(labels, reliability_matrix):
    assert reliability_matrix.isna().sum().sum() == 0, "reliability matrix must be fully ranked for Fleiss Kappa"
    fleiss_input_table_data = []
    for col in reliability_matrix.columns:
        fleiss_input_table_data.append([(reliability_matrix[col].dropna() == label).sum() for label in labels])
    return fleiss_kappa(fleiss_input_table_data)
