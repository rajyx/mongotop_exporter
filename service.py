from abc import ABC, abstractmethod
from common.df_functions import (
    get_top_df,
    add_metrics_delta,
    get_limited_df
)
from common.prometheus_output_functions import (
    add_all_metrics_prometheus_output,
    get_all_metrics_prometheus_output
)


class MongoTopExporterService(ABC):
    def __init__(self, db, metrics):
        self.__db = db
        self.__metrics = metrics
        self.__prev_top = None

    @property
    def db(self):
        return self.__db

    @property
    def metrics(self):
        return self.__metrics

    @property
    def prev_top(self):
        return self.__prev_top

    @prev_top.setter
    def prev_top(self, prev_top):
        self.__prev_top = prev_top

    @abstractmethod
    def get_top_output(self, limit):
        pass


class MongoTopPrometheusExporterService(MongoTopExporterService):
    def get_top_output(self, limit):
        if self.prev_top is None:
            self.prev_top = get_top_df(
                self.db,
                self.metrics
            )
        next_top = get_top_df(
            self.db,
            self.metrics
        )
        merged_top = next_top.merge(
            self.prev_top,
            how="inner",
            left_index=True,
            right_index=True,
            suffixes=["_next", "_previous"]
        )
        self.prev_top = next_top
        add_metrics_delta(merged_top, self.metrics)
        if limit is not None:
            merged_top = get_limited_df(
                dataframe=merged_top,
                sort_by="total_delta",
                row_limit=limit
            )
        add_all_metrics_prometheus_output(merged_top, self.metrics)
        return get_all_metrics_prometheus_output(merged_top, self.metrics)
