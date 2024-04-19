from pymongo import MongoClient
import time
import argparse
import pandas as pd

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
previous_top_df = pd.DataFrame.from_dict(previous_top, orient="index")[['total']]

time.sleep(5)

next_top = admin_db.command("top")["totals"]
next_top.pop('note')
next_top_df = pd.DataFrame.from_dict(next_top, orient="index")[['total']]

print(previous_top_df.to_string())

print("Try to get next top")

print(next_top_df.to_string())

print("Let's try to merge frames")

merged_df = next_top_df.merge(
    previous_top_df,
    how="inner",
    left_index=True,
    right_index=True,
    suffixes=["_next", "_previous"]
)
time_lambda = lambda x: x['time']
count_lambda = lambda x: x['count']
merged_df['total_time_delta'] = (
        (
                merged_df['total_next'].map(time_lambda)
                - merged_df['total_previous'].map(time_lambda)
        ) / (
                merged_df['total_next'].map(count_lambda)
                - merged_df['total_previous'].map(count_lambda)
        )
)
merged_df.fillna(0, inplace=True)
print(merged_df.to_string())
