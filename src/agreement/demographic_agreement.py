"""
Functions for computing agreement between demographic groups
"""
from collections import defaultdict
from multiprocessing import Pool
from typing import Callable, Dict, List, Optional

import numpy as np
import pandas as pd
from more_itertools import flatten
from tqdm import tqdm


def _agreement_with_aggregate_computation(aggregate, user_annotations, agreement_fn: Callable, 
                                          integer_aggregate: bool):
    # special case with median: want to use as ordinal data
    # however, the medians may be non-integer values
    # compute once rounded down, once rounded up, then take the mean of those
    if integer_aggregate and (aggregate.apply(np.ceil) != aggregate).any():
        comp1 = _agreement_with_aggregate_computation(
            aggregate.apply(np.ceil), user_annotations, agreement_fn, False)
        comp2 = _agreement_with_aggregate_computation(
            aggregate.apply(np.floor), user_annotations, agreement_fn, False)
        return np.mean((comp1, comp2))
    reliability = pd.concat((aggregate, user_annotations), axis=1).dropna().T
    return agreement_fn(reliability)


def _agreement_with_aggregate_helper(reliability_matrix: pd.DataFrame, demographics: Dict[str, str], 
                                     user: str, dem: str, dem_users: List[str], agreement_fn: Callable, 
                                     aggregation: Callable = np.mean):
    user_annotations = reliability_matrix.loc[user] 
    aggregated = reliability_matrix.loc[[u for u in reliability_matrix.index if user != u]].apply(
        lambda x: aggregation(x.dropna()))
    in_group_aggregate = reliability_matrix.loc[[u for u in dem_users if u != user]].apply(
        lambda x: aggregation(x.dropna()) if len(x.dropna()) > 0 else np.nan)
    other_users = flatten([v for k, v in demographics.items() if k != dem])
    oo_group_aggregate = reliability_matrix.loc[other_users].apply(
        lambda x: aggregation(x.dropna())  if len(x.dropna()) > 0 else np.nan)

    # integer aggregate = the aggregation function requires integers
    # for ordinal aggregate when using medians - use this when aggregation is not mean
    integer_aggregate = aggregation != np.mean

    same_str = "ALLF" if dem == "F" else "ALLM"
    oth_str = "ALLF" if dem == "M" else "ALLM"

    return {
        f"{dem}-ALL": _agreement_with_aggregate_computation(aggregated, user_annotations, agreement_fn, integer_aggregate),
        f"{dem}-{same_str}": _agreement_with_aggregate_computation(in_group_aggregate, user_annotations, agreement_fn, integer_aggregate),
        f"{dem}-{oth_str}": _agreement_with_aggregate_computation(oo_group_aggregate, user_annotations, agreement_fn, integer_aggregate)
    }

def agreement_with_aggregate(reliability_matrix: pd.DataFrame, demographics: Dict[str, str], 
                             agreement_fn: Callable, aggregation: Callable = np.mean,
                             mp_pool: Optional[Pool] = None):
    """
    Following general method from https://arxiv.org/pdf/2110.05699.pdf
    """

    # 6 results:
    # F-ALLF: how much do females agree with female aggregate
    # M-ALLM: how much do males agree with male aggregate
    # F-ALLM: how much do females agree with male aggregate
    # M-ALLF: how much do males agree with female aggregate
    # F-ALL: how much do females agree with full aggregate
    # M-ALL: how much do males agree with full aggregate

    # compute M/F agreement with full aggregation
    demographic_results = defaultdict(list)
    for dem, users in tqdm(demographics.items(), desc="Demographics loop"):
        if mp_pool is None:
            results = [_agreement_with_aggregate_helper(reliability_matrix, demographics, user, dem, users, 
                                                        agreement_fn, aggregation) for user in users]
        else:
            inputs = [(reliability_matrix, demographics, user, dem, users, agreement_fn, aggregation)
                    for user in users]
            results = mp_pool.starmap(_agreement_with_aggregate_helper, inputs)

        for result in results:
            for k, v in result.items():
                # filter NaNs, which occur when there are no other annotators with the same gender 
                # or there are no annotators with the other gender
                if not np.isnan(v):
                    demographic_results[k].append(v)

    return demographic_results
