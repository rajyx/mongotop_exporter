import argparse

from flask import Flask, Response
from pymongo import MongoClient

from mongotop_exporter import MongoTopPrometheusExporter

app = Flask(__name__)
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


@app.route("/metrics")
def metrics():
    return Response(top_exporter.get_top_output(), mimetype="text/plain")


if __name__ == '__main__':
    app.run(debug=True)
