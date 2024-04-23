from mongotop_exporter import MongoTopPrometheusExporter
import argparse
from pymongo import MongoClient
from time import sleep

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

top_exporter = MongoTopPrometheusExporter(
    db=client.admin,
    metrics=['total']
)

for i in range(3):
    print(top_exporter.get_top_output())
    sleep(5)
