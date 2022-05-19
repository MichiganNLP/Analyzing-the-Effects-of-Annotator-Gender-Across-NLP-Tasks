"""
This file configures functions that should be used to compute agreement metrics for various tasks.
To add a new task for agreement, you must add a function to the following maps:
* PAIRWISE_AGREEMENT_FN_MAP: the function to call to compute pairwise agreement between two annotators
* PAIRWISE_AGGREGATE_AGREEMENT_FN_MAP: the function to call to compute pairwise agreement between two annotators if one measure is an aggregate
                                       when aggregated, ordinal data may become interval data (OPTIONAL)

Notes on agreement metrics:
Agreement functions are always called on a reliability matrix
To use Cohen/Fleiss, use the functions in src.agreement.agreement_utils - the first argument is a list of labels
So on a binary dataset, your function in an AGREEMENT_FN_MAP could one of the following:
* partial(cohen_kappa_reliability_matrix, [True, False])
* partial(fleiss_kappa_reliability_matrix, [True, False])
"""
from functools import partial

import krippendorff

from src.tasks.affectivetext.config import SUBTASKS as AFFECTIVE_TEXT_SUBTASKS


PAIRWISE_AGREEMENT_FN_MAP = {
    "wordsim_rel": partial(krippendorff.alpha, level_of_measurement="ordinal", value_domain=list(range(-2, 3))),
    "wordsim_sim": partial(krippendorff.alpha, level_of_measurement="ordinal", value_domain=list(range(-2, 3))),
    "sentiment": partial(krippendorff.alpha, level_of_measurement="ordinal", value_domain=list(range(0, 5))),
    "commitmentbank": partial(krippendorff.alpha, level_of_measurement="ordinal", value_domain=list(range(-3, 4))),
} | {
    f"affectivetext_{subtask}": partial(krippendorff.alpha, level_of_measurement="interval") for subtask in AFFECTIVE_TEXT_SUBTASKS
}


# NOTE: this is OPTIONAL, only required if the agreement function changes when using an aggregate metric
#       this function is used when non-integer values are expected, otherwise the function from 
#       PAIRWISE_AGREEMENT_FN_MAP  is used.
PAIRWISE_AGGREGATE_AGREEMENT_FN_MAP = {
    "wordsim_rel": partial(krippendorff.alpha, level_of_measurement="interval"),
    "wordsim_sim": partial(krippendorff.alpha, level_of_measurement="interval"),
    "sentiment": partial(krippendorff.alpha, level_of_measurement="interval"),
    "commitmentbank": partial(krippendorff.alpha, level_of_measurement="interval"),
}
