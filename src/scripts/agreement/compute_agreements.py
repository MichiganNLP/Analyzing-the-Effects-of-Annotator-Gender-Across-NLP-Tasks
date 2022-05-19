"""
A script for computing various agreement metrics for a given task

* How do individuals compare to aggregated annotations from different demographic groups?
  --> output: raw JSON results, PDF of boxplots, ttest results
  --> location: output/agreement/{task}/agreement_with_aggregate

TO ADD NEW TASKS: add to the dictionaries in src/config/agreement.py
"""
import argparse
import json
import os
from multiprocessing import Pool

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import mode, ttest_ind

from src.config.agreement import PAIRWISE_AGGREGATE_AGREEMENT_FN_MAP, PAIRWISE_AGREEMENT_FN_MAP
from src.config.data import DEMOGRAPHICS_FN_MATRIX_MAP, REALIABILITY_FN_MATRIX_MAP
from src.agreement.demographic_agreement import agreement_with_aggregate


AGGREGATION_STR_TO_FN = {
    "mean": np.mean,
    "median": np.nanmedian,
    "mode": lambda x: mode(x).mode[0]
}

CONFIG_MAPS = [DEMOGRAPHICS_FN_MATRIX_MAP, PAIRWISE_AGREEMENT_FN_MAP, REALIABILITY_FN_MATRIX_MAP]


def _output_distribution_results(raw_data, output_dir, boxplot_title, boxplot_figname, ttest_pairs):
    """
    Output results where there is a range of values - such that we can perform t-tests and output boxplots
    """
    # save raw results
    with open(os.path.join(output_dir, f"raw_results_{boxplot_figname}.json"), "w") as f:
        json.dump(raw_data, f)

    # create boxplot
    plt.boxplot(raw_data.values(), labels=raw_data.keys())
    plt.title(boxplot_title)
    plt.savefig(os.path.join(output_dir, f"{boxplot_figname}.pdf"))
    plt.close()

    # output results of t-tests
    # NOTE: pvals not corrected for multiple comparisons (corrected in final table creation code)
    ttest_results = []
    for stat0, stat1 in ttest_pairs:
        stat, pval = ttest_ind(raw_data[stat0], raw_data[stat1])
        ttest_results.append((stat0, stat1, stat, pval))
    pd.DataFrame(ttest_results, columns=["dist1", "dist2", "tval", "pval"]).to_csv(
        os.path.join(output_dir, f"ttest_{boxplot_figname}.csv"), index=False)


def _create_dir(output_path: str) -> str:
    os.makedirs(output_path, exist_ok=True)
    return output_path


class AgreementComputer:
    OUTPUT_DIR = "output/agreement"

    def __init__(self, task, n_processes):
        self.task = task
        self.reliability_matrix = REALIABILITY_FN_MATRIX_MAP[task]()
        self.reliability_matrix.sort_index(inplace=True)
        self.demographics = DEMOGRAPHICS_FN_MATRIX_MAP[task]()
        self.pairwise_agreement_fn = PAIRWISE_AGREEMENT_FN_MAP[task]
        # pairwise aggregate fn only needs to be defined if it differs from the typical pairwise fn
        self.pairwise_agreement_aggregate_fn = PAIRWISE_AGGREGATE_AGREEMENT_FN_MAP.get(task, self.pairwise_agreement_fn)

        self.pool = Pool(n_processes) if n_processes > 1 else None

    def agreement_with_aggregate(self, aggregation):
        # if not using mean, shouldn't use pairwise_agreement_aggregate_fn (that switches to interval measure)
        agreement_fn = self.pairwise_agreement_aggregate_fn \
            if aggregation == "mean" else self.pairwise_agreement_fn

        # compute agreement scores
        agreement_data = agreement_with_aggregate(
            self.reliability_matrix, self.demographics, aggregation=AGGREGATION_STR_TO_FN[aggregation], 
            agreement_fn=agreement_fn, mp_pool=self.pool)

        out_dir = _create_dir(os.path.join(self.OUTPUT_DIR, self.task, "agreement_with_aggregate"))
        _output_distribution_results(agreement_data, out_dir, f"Agreement with {aggregation}",
            f"agreement_{aggregation}", [("M-ALLM", "M-ALLF"), ("F-ALLF", "F-ALLM"), ("F-ALL", "M-ALL")])


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", 
                        choices=set.intersection(*[set(x.keys()) for x in CONFIG_MAPS]), 
                        required=True,
                        help="The task to run on. Must provide demographics function and reliability function in config files.")
    parser.add_argument("--aggregation",
                        choices=AGGREGATION_STR_TO_FN.keys(),
                        required=True,
                        help="The way to aggregate individual annotator's annotations.")
    parser.add_argument("--n_processes",
                        type=int,
                        default=1,
                        help="The number of processes to run.")
    return parser.parse_args()


def main():
    args = _parse_args()
    ac = AgreementComputer(args.task, args.n_processes)
    ac.agreement_with_aggregate(args.aggregation)


if __name__ == "__main__":
    main()
