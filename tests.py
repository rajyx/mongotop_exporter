import random
import re
import unittest
from global_functions.prometheus_output_functions import (
    extract_db_and_collection_info,
    add_prometheus_output_column
)
from global_functions.common_df_functions import add_metrics_delta
from global_vars import metrics
import pandas as pd


class TestPrometheusFunctions(unittest.TestCase):
    def setUp(self):
        self.collection_path = "db.collection"
        df_dict = {
            self.collection_path: {}
        }
        for metric in metrics:
            metric_time = random.randint(0, 100)
            metric_count = random.randint(0, 100)
            df_dict[self.collection_path].update(
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
        self.merged_top = pd.DataFrame.from_dict(
            df_dict,
            orient="index"
        )

    def test_extract_db_and_collection_info_returns_correct_db_and_collection(self):
        database = "some_db"
        collection = "very.hard.collection"
        collection_path = '.'.join([database, collection])
        prometheus_info = extract_db_and_collection_info(collection_path)
        db_info = re.search('database="(\w+)"', prometheus_info)
        self.assertIsNotNone(db_info)
        self.assertTrue(
            database == db_info.group(1)
        )
        collection_info = re.search('collection="([a-zA-Z0-9\._]+)"', prometheus_info)
        self.assertIsNotNone(collection_info)
        self.assertTrue(
            collection == collection_info.group(1)
        )

    def test_extract_db_and_collection_info_result_has_braces_and_no_spaces_inside(self):
        prometheus_info = extract_db_and_collection_info("db.collection")
        self.assertIsNotNone(
            re.search('{[a-zA-Z0-9\._,"=]+}', prometheus_info)
        )

    def test_add_prometheus_output_column_creates_column_metric(self):
        merged_df = self.merged_top
        add_metrics_delta(merged_df, metrics)
        for metric in metrics:
            add_prometheus_output_column(merged_df, metric)
        self.assertTrue(
            set(
                [f"prometheus_{metric}_output" for metric in metrics]
            ).issubset(
                merged_df.columns
            )
        )

    def test_add_prometheus_output_returns_delta_from_metric_delta_column(self):
        merged_df = self.merged_top
        add_metrics_delta(merged_df, metrics)
        for metric in metrics:
            add_prometheus_output_column(merged_df, metric)

        for metric in metrics:
            delta = merged_df.loc[self.collection_path][f"{metric}_delta"]
            output_delta = re.search(
                "(\d+)$",
                merged_df.loc[self.collection_path][f"prometheus_{metric}_output"]
            ).group(1)
            self.assertEquals(delta, int(output_delta))
