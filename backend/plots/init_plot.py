import pandas as pd

from plotly.offline import init_notebook_mode, plot
from plotly.graph_objs import *
import sys
sys.path.append("../backend/models/")
import predict
import json


def read_config(config_path="../config.json"):
    with open(config_path, "rb") as f:
        config = json.loads(f.read())
    return config

def get_colors(preds, aps):
    d = {}
    b1, b2 = .33*max(preds), .66*max(preds)
    for i in range(len(preds)):
        if preds[i] < b1:
            d[aps[i]] = "green"
        elif preds[i] < b2:
            d[aps[i]] = "blue"
        else:
            d[aps[i]] = "red"

    return d, (int(b1), int(b2))

def plot_show():
    global airports
    df_coords = pd.read_csv("../data/airport-codes.csv")
    data = pd.read_csv('../../data.csv')
    aps = list(data.airport_from.unique())
    airports = {}
    for ap in aps:
        airports[ap] = [float(x) for x in df_coords[df_coords.iata_code == ap].coordinates.iloc[0].split(",")]
    df = pd.DataFrame(list(airports.values()), columns=["lat", "lon"])
    df["airport"] = list(airports.keys())
    df = df.merge(df_coords[["iata_code", "name"]], how="left", left_on="airport", right_on="iata_code")
    df["airport"] = df["airport"] + ", " + df["name"]
    scatters = []

    x = df['lon'].copy()
    y = df['lat'].copy()

    scatter = dict(type='scattermapbox',
                   lat=x.tolist(),
                   lon=y.tolist(),
                   mode='markers',
                   marker=Marker(size=9,
                                 color='rgb(232,61,116)', ),
                   showlegend=False
                   )
    scatters.append(scatter)

    scatter = dict(type='scattermapbox',
                   lat=x.tolist(),
                   lon=y.tolist(),
                   mode='markers',
                   marker=Marker(size=15,
                                 color='rgb(232,61,116)',
                                 opacity=.5, ),
                   text=df["airport"].tolist(),
                   hoverinfo='text',
                   showlegend=False
                   )
    scatters.append(scatter)

    mapbox_access_token = 'pk.eyJ1IjoidmlkZW9kYW5pbCIsImEiOiJjamRrYTlhdW4wcmhpMnFwa21ycG93d2J1In0.XPgGue7sQW-_7E76K_J6vw'

    data = Data(scatters)

    layout = Layout(
        showlegend=False,
        autosize=True,
        #width=680,
        #height=520,

        hovermode='closest',
        mapbox=dict(accesstoken=mapbox_access_token,
                    bearing=0,
                    center=dict(
                        lat=53,
                        lon=45
                    ),
                    pitch=0,
                    zoom=3,
                    style='light'),
        margin=Margin(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        ),
        paper_bgcolor = 'rgba(0,0,0,0)',
        plot_bgcolor = 'rgba(0,0,0,0)'


    )

    fig = dict(data=data, layout=layout)
    plot(fig, filename='../backend/plots/init_map.html', auto_open=False, config={'displayModeBar': False, 'showLink': False})
