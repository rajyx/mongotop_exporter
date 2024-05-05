import pandas as pd
import numpy as np


def time_lambda(x):
    return x['time']


def count_lambda(x):
    return x['count']


def add_metrics_delta(dataframe, metrics):
    for metric in metrics:
        add_metric_delta(dataframe, metric)


def add_metric_delta(dataframe, metric):
    dataframe[f'{metric}_delta'] = round(
        (
                dataframe[f'{metric}_next'].map(time_lambda)
                - dataframe[f'{metric}_previous'].map(time_lambda)
        ) / (
                dataframe[f'{metric}_next'].map(count_lambda)
                - dataframe[f'{metric}_previous'].map(count_lambda)
        )
    )
    dataframe.replace([np.inf, -np.inf, np.nan], 0, inplace=True)


def get_top_df(db, metrics):
    top = db.command("top")["totals"]
    top.pop('note')
    return pd.DataFrame.from_dict(
        top,
        orient="index"
    )[metrics]


def get_limited_df(dataframe, sort_by, row_limit):
    return dataframe.sort_values(
        by=sort_by,
        ascending=False
    ).iloc[:row_limit]
