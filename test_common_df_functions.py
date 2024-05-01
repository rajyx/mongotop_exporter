import random
import unittest

from test_utils.setup import prepare_merged_df
from common.df_functions import (
    add_metric_delta
)
from common.global_vars import metrics


class TestCommonDFFunctions(unittest.TestCase):
    def setUp(self):
        self.collection_path = "db.collection"
        self.merged_top = prepare_merged_df(self.collection_path)

    def test_add_metric_delta_creates_delta_column_and_save_correct_value(self):
        df = self.merged_top
        metric = metrics[random.randint(0, len(metrics) - 1)]
        add_metric_delta(df, metric)
        collection_row = df.loc[self.collection_path]
        next_metric_value = collection_row[f"{metric}_next"]
        prev_metric_value = collection_row[f"{metric}_previous"]
        delta = float(collection_row[f"{metric}_delta"])
        self.assertTrue(
            f"{metric}_delta" in df.columns
        )
        expected_delta = round(
            (next_metric_value["time"] - prev_metric_value["time"]) /
            (next_metric_value["count"] - prev_metric_value["count"])
        )
        self.assertTrue(expected_delta == delta)
