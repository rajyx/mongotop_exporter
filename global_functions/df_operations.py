import re


def add_prometheus_output_column(dataframe, metric):
    dataframe["prometheus_output"] = (f"mongotop_{metric}"
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
