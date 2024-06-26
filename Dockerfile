FROM python:3.9.19
ARG user=mongotop_exporter
RUN pip install pandas flask pymongo \
    && useradd -m -s /bin/bash $user
USER $user
WORKDIR /home/$user
COPY --chown=$user . .
RUN python3 -m unittest \
    && rm test_*.py \
    && rm -r test_utils
ENTRYPOINT ["python3", "mongotop_exporter.py"]