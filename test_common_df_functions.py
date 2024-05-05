import random
import unittest

import pandas as pd

from common.df_functions import (
    add_metric_delta,
    add_metrics_delta,
    get_limited_df
)
from common.global_vars import metrics
from test_utils.setup import (
    prepare_merged_df,
    prepare_multi_collection_merged_df
)


class TestCommonDFFunctions(unittest.TestCase):
    def setUp(self):
        self.collection_path = "db.collection"
        self.merged_top = prepare_merged_df(self.collection_path)

    def test_add_metric_delta_creates_delta_column_and_save_correct_value(self):
        df = self.merged_top
        metric = metrics[random.randint(0, len(metrics) - 1)]
        add_metric_delta(df, metric)
        self.__check_dataframe_metric_delta_column_exists_and_has_correct_value(
            df,
            metric
        )

    def test_add_metrics_delta_creates_delta_column_for_each_input_metric(self):
        df = self.merged_top
        add_metrics_delta(df, metrics)
        for metric in metrics:
            self.__check_dataframe_metric_delta_column_exists_and_has_correct_value(
                df,
                metric
            )

    def __check_dataframe_metric_delta_column_exists_and_has_correct_value(self, df, metric):
        collection_row = df.loc[self.collection_path]
        next_metric_value = collection_row[f"{metric}_next"]
        prev_metric_value = collection_row[f"{metric}_previous"]
        delta = float(collection_row[f"{metric}_delta"])
        self.assertTrue(
            f"{metric}_delta" in df.columns
        )
        count_delta = next_metric_value["count"] - prev_metric_value["count"]
        expected_delta = round(
            (next_metric_value["time"] - prev_metric_value["time"]) /
            (1 if count_delta == 0 else count_delta)
        )
        self.assertTrue(expected_delta == delta)

    def test_get_sorted_limited_df_returns_rows_in_predefined_quantity(self):
        df_len = 50
        limited_df_len = 10
        df = prepare_multi_collection_merged_df(df_len)
        add_metrics_delta(df, metrics)
        metric = metrics[random.randint(0, len(metrics) - 1)]
        limited_df = get_limited_df(df, f"{metric}_delta", limited_df_len)
        self.assertTrue(
            limited_df_len == len(limited_df)
        )
        min_metric_delta = limited_df.min().loc[f"{metric}_delta"]
        merged_df = pd.merge(
            df,
            limited_df,
            how="outer",
            left_index=True,
            right_index=True,
            indicator='Exists'

        )
        max_metric_delta_of_non_top_collections = (
            merged_df[
                merged_df['Exists'] != 'both'
                ].max().loc[f"{metric}_delta_x"]
        )
        self.assertTrue(
            min_metric_delta >= max_metric_delta_of_non_top_collections
        )
