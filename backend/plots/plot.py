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
            d[aps[i]] = "yellow"
        else:
            d[aps[i]] = "red"

    return d, (int(b1), int(b2))

def plot_show(config):
    global airports

    rows = predict.make_row(config)
    aps = config["airport_from"] + [config["airport_to"]]
    df_coords = pd.read_csv("../data/airport-codes.csv")
    airports = {}
    preds = predict.predict(rows)[:len(aps)]

    for ap in aps:
        airports[ap] = [float(x) for x in df_coords[df_coords.iata_code == ap].coordinates.iloc[0].split(",")]
    df = pd.DataFrame(list(airports.values()), columns=["lat", "lon"])
    df["airport"] = list(airports.keys())
    df = df.merge(df_coords[["iata_code", "name"]], how="left", left_on="airport", right_on="iata_code")
    df["airport"] = df["airport"] + ", " + df["name"]
    scatters = []
    print(preds, aps)
    colors, bounds = get_colors(preds, aps)
    # print(bounds)
    if "thr" in config.keys():
        bounds = [int(x) for x in config['thr'].split(', ')]
    print(bounds)

    x = df['lon'].copy()
    y = df['lat'].copy()

    scatter = dict(type='scattermapbox',
                   lat=x.tolist(),
                   lon=y.tolist(),
                   mode='markers',
                   marker=Marker(size=9,
                                 color='rgb(232,61,116)' ),
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

    scatter = dict(type='scattermapbox',
                   lat=x.tolist(),
                   lon=y.tolist(),
                   mode='markers',
                   marker=Marker(size=9,
                                 color='green',
                                 opacity=1, ),
                   # text=df["airport"].tolist(),
                   hoverinfo='text',
                   name='Passengers traffic less than {} per day'.format(bounds[0]),
                   showlegend=True
                   )
    scatters.append(scatter)

    scatter = dict(type='scattermapbox',
                   lat=x.tolist(),
                   lon=y.tolist(),
                   mode='markers',
                   marker=Marker(size=9,
                                 color='rgb(250,240,0)',
                                 opacity=1, ),
                   # text=df["airport"].tolist(),
                   hoverinfo='text',
                   name='Passengers traffic between {} and {} per day'.format(bounds[0], bounds[1]),
                   showlegend=True
                   )
    scatters.append(scatter)

    scatter = dict(type='scattermapbox',
                   lat=x.tolist(),
                   lon=y.tolist(),
                   mode='markers',
                   marker=Marker(size=9,
                                 color='rgb(255,90,0)',
                                 opacity=1, ),
                   # text=df["airport"].tolist(),
                   hoverinfo='text',
                   name='Passengers traffic more than {} per day'.format(bounds[1]),
                   showlegend=True
                   )
    scatters.append(scatter)

    for ap in config["airport_from"]:
        scatter = Scattermapbox(lat=[df[df.iata_code == ap]["lon"].iloc[0], df[df.iata_code == config["airport_to"]]["lon"].iloc[0]],
                                lon=[df[df.iata_code == ap]["lat"].iloc[0], df[df.iata_code == config["airport_to"]]["lat"].iloc[0]],
                                mode='lines',
                                marker=Marker(size=12,
                                              color=colors[ap]),
                                text=[[df[df.iata_code==ap]["airport"].iloc[0]],
                                      [df[df.iata_code==ap]["airport"].iloc[0]]],
                                hoverinfo='text',
                                showlegend=False)
        scatters.append(scatter)


    mapbox_access_token = 'pk.eyJ1IjoidmlkZW9kYW5pbCIsImEiOiJjamRrYTlhdW4wcmhpMnFwa21ycG93d2J1In0.XPgGue7sQW-_7E76K_J6vw'

    data = Data(scatters)

    layout = Layout(
        showlegend=True,
        autosize=True,
        # width=680,
        # height=520,

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
        legend=dict(
            x=.01,
            y=.98,
            traceorder='normal',
            font=dict(
                family='sans-serif',
                size=12,
                color='#000'
            ),
            bgcolor='#E2E2E2',
            bordercolor='#FFFFFF',
            # borderwidth=2
            # xanchor="right"
        ),
        # paper_bgcolor = 'rgba(0,0,0,0)',
        # plot_bgcolor = 'rgba(0,0,0,0)'


    )

    fig = dict(data=data, layout=layout)
    plot(fig, filename='../backend/plots/map.html', auto_open=False, config={'displayModeBar': False, 'showLink': False})

    text = get_text(config, preds)
    return text


def get_text(config, preds):
    ap_to = config["airport_to"]
    ap_from = config["airport_from"]
    date = config["date"]
    text = "Date:   {}<br><br>".format(date)
    for i in range(len(ap_from)):
        text += "{}  ->  {} :  {}  passengers <br>".format(ap_to, ap_from[i], preds[i])

    return text
