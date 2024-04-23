from abc import ABC, abstractmethod
from global_functions.df_operations import (
    get_top_df,
    add_metrics_delta,
    add_all_metrics_prometheus_output,
    get_all_metrics_prometheus_output
)


class MongoTopExporter(ABC):
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
    def get_top_output(self):
        pass


class MongoTopPrometheusExporter(MongoTopExporter):
    def get_top_output(self):
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
        add_all_metrics_prometheus_output(merged_top, self.metrics)
        return get_all_metrics_prometheus_output(merged_top, self.metrics)
