import pandas as pd
from sklearn.model_selection import ParameterGrid
import pickle as pkl
import numpy as np
import feature_generation as fg
import copy
import json

def predict(row):
    data = pd.read_csv('../../data.csv')
    with open("../data/model.pkl", 'rb') as file:
        model = pkl.load(file)
    row = fg.get_features_row(data, row)
    preds = []
    for each_row in row.iterrows():
        each_row = each_row[1]
        ldf = data[(data.airport_from==each_row.airport_from)&(data.airport_to==each_row.airport_to)]
        if len(ldf) > 0:
            preds += [int((int(ldf.number_of_people.iloc[0]) + each_row.last_flight)*np.random.randint(1, 10)/20)]
        else:
            preds += [0]#[(140  + int(np.random.normal(0, 10)))*np.random.randint(1, 6)]

    return preds

def read_config(config_path="../config.json"):
    with open(config_path, "rb") as f:
        config = json.loads(f.read())
    return config

def make_row(_config):
    config = copy.deepcopy(_config)
    config["airport_to"] = [config["airport_to"]]
    config["date"] = [config["date"]]
    df = pd.DataFrame([], columns=["airport_from", "airport_to", "date"])
    for param in ParameterGrid(config):
        add = pd.DataFrame(list(param.values()), index=list(param.keys())).T
        df = pd.concat([df, add], axis=0)
    return df
