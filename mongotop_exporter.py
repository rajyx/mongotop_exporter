import argparse

from flask import Flask, Response
from pymongo import MongoClient
from global_vars import metrics
from service import MongoTopPrometheusExporterService

app = Flask(__name__)
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--mongo_host", "-mh")
arg_parser.add_argument("--mongo_port", "-mp", default="27017")
arg_parser.add_argument("--username", "-u")
arg_parser.add_argument("--password", "-p")
args = arg_parser.parse_args()

client = MongoClient(
    host=args.mongo_host,
    port=int(args.mongo_port),
    username=args.username,
    password=args.password
)

top_exporter = MongoTopPrometheusExporterService(
    db=client.admin,
    metrics=metrics
)


@app.route("/metrics")
def metrics():
    return Response(top_exporter.get_top_output(), mimetype="text/plain")


if __name__ == '__main__':
    # Run app on 5000 port by default
    app.run(debug=True)
