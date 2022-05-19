# things to compare per task:
# F-ALL vs M-ALL (2-sided t-test)
# F-ALLF vs F-ALLM (1-sided t-test)
# M-ALLM vs M-ALLF (1-sided t-test)

from collections import defaultdict

import pandas as pd
from scipy.stats import ttest_ind

from src.config.task_names import TASK_ID_TO_NAME
from src.scripts.agreement.util import load_data, TASKS
from src.util.fdr import fdr_correction


ALPHA = 0.05
SAVE_FILE = "output/agreement/combo/significance.txt"

def build_significance_table():
    results = defaultdict(list)
    for task in TASKS:
        task_name = TASK_ID_TO_NAME.get(task, task)
        raw_data = load_data(task)

        # compare F-ALL vs M-ALL (2-sided t-test)
        results[task_name].extend(tuple(ttest_ind(raw_data["F-ALL"], raw_data["M-ALL"])))

        # compare F-F vs F-OTH (1-sided t-test)
        results[task_name].extend(tuple(ttest_ind(raw_data["F-ALLF"], raw_data["F-ALLM"], alternative="greater")))

        # compare M-M and M-OTH (1-sided t-test)
        results[task_name].extend(tuple(ttest_ind(raw_data["M-ALLM"], raw_data["M-ALLF"], alternative="greater")))

    index = pd.MultiIndex.from_product(
        [["F-ALL vs. M-ALL", "F-ALLF vs. F-ALLM", "M-ALLM vs. M-ALLF"], ["tval", "pval"]], 
        names=["groups", "value"])
    return pd.DataFrame.from_dict(results, orient="index", columns=index)

def _correct_table_fdr(sig_table: pd.DataFrame) -> pd.DataFrame:
    copied_table = sig_table.copy(deep=True)

    # perform correction
    pval_df = copied_table.xs("pval", axis=1, level=1)
    pval_df_corrected = fdr_correction(pval_df.stack()).unstack()

    # replace values
    for l1 in copied_table.columns.get_level_values(0).unique():
        copied_table.loc[:, (l1, "pval")] = pval_df_corrected[l1]

    # return new table
    return copied_table


def main():
    sig_table = build_significance_table()
    sig_table = _correct_table_fdr(sig_table)

    # format as LaTeX table
    latex = sig_table.to_latex(
        caption=f"Results of permutation tests. No results are significant at "\
                f"the level $\\alpha={ALPHA}$ after FDR correction was "\
                 "performed for results across the table.",
        label=f"tab:agreement_sig",
        escape=False,
        float_format="%.2f"
    )
    with open(SAVE_FILE, "w") as f:
        f.write(latex)

if __name__ == "__main__":
    main()
