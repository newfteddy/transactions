from sklearn.linear_model import LinearRegression
import pandas as pd
import pickle as pkl
import feature_generation as fg

data = pd.read_csv('../../../data.csv')
data = fg.get_features_all(data)

cols = ["weekday", "month", "last_flight"]
X = data[cols]
y = data["number_of_people"]

model = LinearRegression(normalize=True,
                         n_jobs=-1)

model.fit(X[cols].fillna(X[cols].mean()), y)

with open("../../data/model.pkl", 'wb') as file:
    pkl.dump(model, file)
