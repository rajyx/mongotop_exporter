import random
import re
import unittest
from global_functions.prometheus_output_functions import (
    extract_db_and_collection_info
)
from global_vars import metrics
import pandas as pd


class TestPrometheusFunctions(unittest.TestCase):
    def setUp(self):
        df_dict = {
            "db.collection": {
                metric: {
                    "time": random.randint(0, 100),
                    "count": random.randint(0, 100)
                } for metric in metrics
            }
        }
        self.dataframe = pd.DataFrame.from_dict(
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

    def test_prometheus_output_has_metric_info_value_parts(self):
        pass
