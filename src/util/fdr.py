from typing import Dict, Union

import pandas as pd

from statsmodels.stats.multitest import fdrcorrection


def fdr_correction(pvalue_map: Union[Dict[str, float], pd.Series], alpha: float = 0.05) -> Union[Dict[str, float], pd.Series]:
    """
    Run false discovery rate correction of p values, returns new p-values for specified tests
    Specifically, uses the Benjamini-Hochberg Procedure
    :param pvalue_map: dictionary (or pandas series) of strings to p values
    :param alpha: the error rate to use with FDR. Default to 0.05, for consistency with everything else we are doing
    :return: corrected dictionary (or pandas series) of strings to p-values after false discovery rate correction
    """
    pvalue_map_dict = pvalue_map if type(pvalue_map) == dict else pvalue_map.to_dict()
    p_vals = list(pvalue_map_dict.values())
    _, corrected_pvals = fdrcorrection(p_vals, alpha)
    corrected_dictionary = {k: corrected_pvals[i] for i, k in enumerate(pvalue_map_dict.keys())}
    if type(pvalue_map) == pd.Series:
        return pd.Series(corrected_dictionary)
    return corrected_dictionary
