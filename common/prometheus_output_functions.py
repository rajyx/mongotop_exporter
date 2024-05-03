import re
from io import StringIO
import csv


def add_all_metrics_prometheus_output(dataframe, metrics):
    for metric in metrics:
        add_prometheus_output_column(dataframe, metric)


def add_prometheus_output_column(dataframe, metric):
    dataframe[f"prometheus_{metric}_output"] = (f"mongotop_{metric}"
                                                + dataframe.index.map(extract_db_and_collection_info)
                                                + " " + dataframe[f'{metric}_delta'].map(lambda x: str(int(x))))


def extract_db_and_collection_info(collection_path):
    match = re.search('^(\w+)\.([\w\.]+)', collection_path)
    info = ",".join(
        [
            f'collection="{match.group(2)}"',
            f'database="{match.group(1)}"'
        ]
    )
    return "{" + info + "}"


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
