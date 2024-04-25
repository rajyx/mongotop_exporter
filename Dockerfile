FROM python:3.9.19
RUN pip install pandas flask pymongo && useradd -m -s /bin/bash mongotop_exporter
USER mongotop_exporter