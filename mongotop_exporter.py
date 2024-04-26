import argparse

from flask import Flask, Response
from pymongo import MongoClient

from service import MongoTopPrometheusExporterService

app = Flask(__name__)
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--mongo_host", "-mh")
arg_parser.add_argument("--mongo_port", "-mp")
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
    metrics=['total']
)


@app.route("/metrics")
def metrics():
    return Response(top_exporter.get_top_output(), mimetype="text/plain")


if __name__ == '__main__':
    # Run app on 5000 port by default
    # Expose app for all machines in current network
    app.run(debug=True, host="0.0.0.0")
