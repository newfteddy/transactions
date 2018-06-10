import pandas as pd
import datetime as dt
import numpy as np

def get_features_all(data):
    data.date = data.date.apply(lambda x: dt.datetime.strptime(x, "%Y-%m-%d"))
    data["weekday"] = data.date.apply(lambda x: x.weekday())
    data["month"] = data.date.apply(lambda x: x.month)

    gb = data.groupby(["airport_from", "airport_to"])["date"].shift(1)
    data["last_flight"] = (data["date"] - gb).dt.days
    return data


def get_features_row(data, row):
    data = pd.concat([data, row], axis=0)
    data.date = data.date.apply(lambda x: dt.datetime.strptime(x, "%Y-%m-%d"))
    data["weekday"] = data.date.apply(lambda x: x.weekday())
    data["month"] = data.date.apply(lambda x: x.month)
    gb = data.groupby(["airport_from", "airport_to"])["date"].shift(1)
    data["last_flight"] = (data["date"] - gb).dt.days

    return pd.DataFrame(data.iloc[-len(row):])

