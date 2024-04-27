import re
import unittest
from global_functions.prometheus_output_functions import (
    extract_db_and_collection_info
)


class TestPrometheusFunctions(unittest.TestCase):
    def test_extract_db_and_collection_info(self):
        database = "some_db"
        collection = "very.hard.collection"
        collection_path = '.'.join([database, collection])
        prometheus_info = extract_db_and_collection_info(collection_path)
        db_info = re.search('database="(\w+)"', prometheus_info)
        self.assertIsNotNone(db_info)
        self.assertTrue(
            database == db_info.group(1)
        )
        collection_info = re.search('collection="([a-zA-Z0-9\.]+)"', prometheus_info)
        self.assertIsNotNone(collection_info)
        self.assertTrue(
            collection == collection_info.group(1)
        )
