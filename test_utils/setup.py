import random

import pandas as pd

from common.global_vars import metrics


def prepare_merged_df(collection_path):
    df_dict = {
        collection_path: prepare_collection_dict()
    }
    merged_top = pd.DataFrame.from_dict(
        df_dict,
        orient="index"
    )
    return merged_top


def prepare_multi_collection_merged_df(collection_quantity):
    df_dict = {}
    for number in range(1, collection_quantity + 1):
        df_dict[f"db.collection_{number}"] = prepare_collection_dict()
    return pd.DataFrame.from_dict(
        df_dict,
        orient="index"
    )


def prepare_collection_dict():
    collection_dict = {}
    for metric in metrics:
        metric_time = random.randint(0, 100)
        metric_count = random.randint(0, 100)
        collection_dict.update(
            {
                f"{metric}_previous": {
                    "time": metric_time,
                    "count": metric_count
                },
                f"{metric}_next": {
                    "time": metric_time + random.randint(0, 100) * 10000,
                    "count": metric_count + random.randint(0, 100)
                }
            }
        )
    return collection_dict
