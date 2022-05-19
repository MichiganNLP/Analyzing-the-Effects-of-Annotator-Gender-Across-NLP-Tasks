""""
Helper functions for loading wordsim data
"""
from datetime import datetime

import pandas as pd

def parse_time(time_string) -> datetime:
    """
    Function for parsing time strings
    For some reason, parsing the timezone is leading to issues, so just getting rid of that.
    """
    split = time_string.split()
    removed_timezone = " ".join((split[:-2] + split[-1:]))
    return datetime.strptime(removed_timezone, "%a %b %d %H:%M:%S %Y")


def time_spent(df) -> pd.Series:
    """
    Create a pandas series representing the time spent by the annotator
    """
    return (df["SubmitTime"].apply(parse_time) - df["AcceptTime"].apply(parse_time)).apply(
        lambda x: x.total_seconds())
