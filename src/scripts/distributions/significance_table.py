import itertools
from math import comb
import os
from typing import Any

import numpy as np
import pandas as pd
from tqdm import tqdm

from src.config.data import DEMOGRAPHICS_FN_MATRIX_MAP, \
    REALIABILITY_FN_MATRIX_MAP
from src.config.distribution import DISTRIBUTION_CONFIG
from src.config.task_names import TASK_ID_TO_NAME
from src.util.fdr import fdr_correction

MAX_PERMUTATIONS = 10000
SAVE_FILE = "output/distribution/combo/significance.txt"
SEED = 123
ALPHA = 0.05


def _count_helper(annotations: pd.DataFrame) -> pd.Series:
    return pd.Series(annotations.to_numpy().flatten()).value_counts(
        normalize=True).sort_index()


def compute_difference_metric(annotations1: pd.DataFrame, 
    annotations2: pd.DataFrame, task):
    counts1 = _count_helper(annotations1)
    counts2 = _count_helper(annotations2)
    difference_df = pd.concat(
            (counts1, counts2), axis=1)

    task_conf = DISTRIBUTION_CONFIG[task]
    if DISTRIBUTION_CONFIG[task]["annotation_type"] == "ordinal":
        df = difference_df.iloc[task_conf["compare_cols"], ]
        return (df[0]-df[1]).abs().sum()
    else:
        index = pd.RangeIndex(start=task_conf["min_val"], stop=task_conf["max_val"] + 1, step=1)
        counts1 = counts1.reindex(index, fill_value=0)
        counts2 = counts2.reindex(index, fill_value=0)
        difference_df = pd.concat(
            (counts1.cumsum(), counts2.cumsum()), axis=1)
        return((difference_df[0] - difference_df[1]).abs().sum())

def create_permutations(data: pd.DataFrame, size_M: int, size_F: int):
    permutations = []
    if MAX_PERMUTATIONS > comb(len(data.index), size_F):
        for m_combo in itertools.combinations(data.index, size_M):
            f_combo = [x for x in data.index if x not in m_combo]
            assert len(f_combo) == size_F
            permutations.append((list(m_combo), f_combo))
    else:
        np.random.seed(SEED)
        assert len(data.index) == size_M + size_F
        for _ in range(MAX_PERMUTATIONS):
            permutation = np.random.permutation(data.index)
            permutations.append((permutation[:size_M], permutation[size_M:]))
    return permutations


def _latex_bold(val: Any, bold: bool = False):
    val = str(val)
    if bold:
        return f"\\textbf{{{val}}}"
    return val


def main():
    os.makedirs(os.path.split(SAVE_FILE)[0], exist_ok=True)

    results = {}
    for task, conf in tqdm(DISTRIBUTION_CONFIG.items(), desc="Task loop"):
        # ignore tasks that are ordinal and haven't specified columns
        if conf["annotation_type"] == "ordinal" and "compare_cols" not in conf:
            print(f"Skipping {task} (compare_cols not specified)")
            continue

        data = REALIABILITY_FN_MATRIX_MAP[task]()
        data.sort_index(inplace=True)
        demographics = DEMOGRAPHICS_FN_MATRIX_MAP[task]()

        observed = compute_difference_metric(data.loc[demographics["M"]], 
            data.loc[demographics["F"]], task)

        size_M = len(demographics["M"])
        size_F = len(demographics["F"])

        permutations = create_permutations(data, size_M, size_F)

        permuted_metrics = []
        count_gt = 0
        for s1, s2 in tqdm(permutations, desc=f"Processing {task} permutations", 
            leave=False):
            permuted_metrics.append(compute_difference_metric(data.loc[s1], 
                data.loc[s2], task))
            if permuted_metrics[-1] >= observed:
                count_gt += 1

        p_val = count_gt / len(permutations)
        results[task] = p_val 

    # FDR correction
    results = fdr_correction(results)
    results_list = [
        (_latex_bold(TASK_ID_TO_NAME.get(t, t), p < ALPHA),
         _latex_bold(p, p < ALPHA)) 
        for t, p in results.items()]

    # format as LaTeX table
    latex = pd.DataFrame(results_list, columns=["Task", "p-value"]).to_latex(
        caption=f"Results of permutation tests. Results significant at the "\
            f"level $\\alpha={ALPHA}$ are demarcated in \\textbf{{bold}}. "\
            "FDR correction is performed for results across the table.",
        label=f"tab:permutation_results",
        index=False,
        escape=False
    )
    with open(SAVE_FILE, "w") as f:
        f.write(latex)



if __name__ == "__main__":
    main()
