import pandas as pd


def time_lambda(x):
    return x['time']


def count_lambda(x):
    return x['count']




def add_metrics_delta(dataframe, metrics):
    for metric in metrics:
        dataframe[f'{metric}_delta'] = round(
            (
                    dataframe[f'{metric}_next'].map(time_lambda)
                    - dataframe[f'{metric}_previous'].map(time_lambda)
            ) / (
                    dataframe[f'{metric}_next'].map(count_lambda)
                    - dataframe[f'{metric}_previous'].map(count_lambda)
            )
        ).astype(int)
    dataframe.fillna(0, inplace=True)



def get_top_df(db, metrics):
    top = db.command("top")["totals"]
    top.pop('note')
    return pd.DataFrame.from_dict(
        top,
        orient="index"
    )[metrics]
