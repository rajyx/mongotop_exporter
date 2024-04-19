from pymongo import MongoClient
import time
import argparse

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

time.sleep(5)

next_top = admin_db.command("top")["totals"]
next_top.pop('note')

for collection in previous_top:
    print(f"{collection} {previous_top[collection]['total']}")

print("Try to get next top")

for coll in next_top:
    print(f"{coll} {next_top[coll]['total']}")
