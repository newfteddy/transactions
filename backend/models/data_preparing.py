import pandas as pd
import datetime as dt
import numpy as np

data = pd.read_csv("../../../schedule.csv")

def convert_to_date(x):
    try:
        date = dt.datetime.fromtimestamp(x)
        date = dt.datetime(date.year, date.month, date.day)
        return date
    except:
        return np.nan

data["date"] = data.actual_departure_time.apply(lambda x: convert_to_date(x))

data = data.groupby(["airport_from", "airport_to", "date"]).size().to_frame("number_of_people")
data = data.reset_index()

people = np.random.normal(140, 10, len(data))
data.number_of_people *= people

data.to_csv("../../../data.csv", index=False)