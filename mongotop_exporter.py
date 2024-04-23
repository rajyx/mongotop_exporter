import argparse
import time

import pandas as pd
from pymongo import MongoClient

from global_functions.df_operations import (
    add_all_metrics_prometheus_output,
    add_metrics_delta,
    get_all_metrics_prometheus_output
)

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--host")
arg_parser.add_argument("--port")
arg_parser.add_argument("--username")
arg_parser.add_argument("--password")
args = arg_parser.parse_args()

client = MongoClient(
    host=args.host,
    port=int(args.port),
    username=args.username,
    password=args.password
)
admin_db = client.admin
previous_top = admin_db.command("top")["totals"]
previous_top.pop('note')
metrics = ['total']
previous_top_df = pd.DataFrame.from_dict(previous_top, orient="index")[metrics]

time.sleep(5)

next_top = admin_db.command("top")["totals"]
next_top.pop('note')
next_top_df = pd.DataFrame.from_dict(next_top, orient="index")[metrics]

merged_df = next_top_df.merge(
    previous_top_df,
    how="inner",
    left_index=True,
    right_index=True,
    suffixes=["_next", "_previous"]
)
add_metrics_delta(merged_df, metrics)
add_all_metrics_prometheus_output(merged_df, metrics)
output = get_all_metrics_prometheus_output(merged_df, metrics)
print(output)
