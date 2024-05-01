import random

import pandas as pd

from common.global_vars import metrics


def prepare_merged_df(collection_path):
    df_dict = {
        collection_path: {}
    }
    for metric in metrics:
        metric_time = random.randint(0, 100)
        metric_count = random.randint(0, 100)
        df_dict[collection_path].update(
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
    merged_top = pd.DataFrame.from_dict(
        df_dict,
        orient="index"
    )
    return merged_top