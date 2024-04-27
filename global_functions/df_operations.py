import re
from io import StringIO
import pandas as pd
import csv


def time_lambda(x):
    return x['time']


def count_lambda(x):
    return x['count']


def add_all_metrics_prometheus_output(dataframe, metrics):
    for metric in metrics:
        add_prometheus_output(dataframe, metric)


def add_prometheus_output(dataframe, metric):
    dataframe[f"prometheus_{metric}_output"] = (f"mongotop_{metric}"
                                                + dataframe.index.map(extract_database_and_collection_info)
                                                + " " + dataframe[f'{metric}_delta'].astype(str))


def extract_database_and_collection_info(collection_path):
    match = re.search('^(\w+)\.(.*)', collection_path)
    info = ",".join(
        [
            f'collection="{match.group(2)}"',
            f'database="{match.group(1)}"'
        ]
    )
    return "{" + info + "}"


def add_metrics_delta(dataframe, metrics):
    for metric in metrics:
        dataframe[f'{metric}_delta'] = round(
            (
                    dataframe[f'{metric}_next'].map(time_lambda)
                    - dataframe[f'{metric}_previous'].map(time_lambda)
            ) / (
                    dataframe[f'{metric}_next'].map(count_lambda)
                    - dataframe[f'{metric}_previous'].map(count_lambda)
            )
        )
    dataframe.fillna(0, inplace=True)


def get_all_metrics_prometheus_output(dataframe, metrics):
    result = StringIO()
    for metric in metrics:
        result.write(get_metric_prometheus_output(dataframe, metric))
    return result.getvalue()


def get_metric_prometheus_output(dataframe, metric):
    output = StringIO()
    dataframe[
        [
            f"prometheus_{metric}_output"
        ]
    ].to_csv(
        output,
        header=False,
        index=False,
        quoting=csv.QUOTE_NONE,
        escapechar='\\',
        sep=';'  # sep length must be equals or greater then 1
    )
    return output.getvalue()


def get_top_df(db, metrics):
    top = db.command("top")["totals"]
    top.pop('note')
    return pd.DataFrame.from_dict(
        top,
        orient="index"
    )[metrics]
