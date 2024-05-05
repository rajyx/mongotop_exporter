import argparse

from flask import Flask, Response
from pymongo import MongoClient
from common.global_vars import metrics
from service import MongoTopPrometheusExporterService

app = Flask(__name__)
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--mongo_host", "-mh", help="mongo db host")
arg_parser.add_argument("--mongo_port", "-mp", default="27017", help="mongo db port")
arg_parser.add_argument("--username", "-u", help="mongo user name")
arg_parser.add_argument("--password", "-p", help="mongo user pwd")
arg_parser.add_argument("--limit", "-l", default=None, help="limit output collections quantity")
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
    return Response(
        top_exporter.get_top_output(
            int(args.limit)
        ),
        mimetype="text/plain"
    )


if __name__ == '__main__':
    # Run app on 5000 port by default
    # Expose app to any machine of current network
    app.run(debug=True, host="0.0.0.0")
