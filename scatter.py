# -*- coding: utf-8 -*-
# Import required libraries
import os

import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go

import flask
from flask_cors import CORS
import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html


# Setup the app
app = dash.Dash(__name__)
server = app.server



app.layout = html.Div([
    html.Div(
        [
            html.Img(src='./assets/logo-apex.png',
                    className='logo'),
            html.H1('A Sample of a New Dash Waterfall',
                    className='main_title'),
            html.H4('This is fake data used for a sample demo.',
                    className='sub_title')
        ],
        className='main_header',
    ),
    html.Div(
        [
            html.Div(
                [
                    dcc.Slider(
                        min=0,
                        max=2,
                        value=0,
                        marks={i: ''.format(i + 1) for i in range(3)},
                        id='slider'
                    ),
                ],
                className='row slider_main',
                style={'margin-bottom': '10px'}
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Button('Back', id='back', style={
                                        'display': 'inline-block'}),
                            html.Button('Next', id='next', style={
                                        'display': 'inline-block'})
                        ],
                        className='nav_buttons'
                        #  columns offset-by-two'
                    ),
                    dcc.Markdown(
                        id='text',
                        className='main_body_text'
                        #  six columns'
                    ),
                ],
                className='row',
                style={'margin-bottom': '10px'}
            ),
            dcc.Graph(
                id='graph',
                style={'height': '60vh'}
            ),
        ],
        id='page'
    ),
])


# Internal logic
last_back = 0
last_next = 0

df = pd.read_csv("data/simple.csv")

xlist = list(df["Engine"].dropna())
ylist = list(df["RPM"].dropna())

del df["x"]
del df["y"]

zlist = []
for row in df.iterrows():
    index, data = row
    zlist.append(data.tolist())

UPS = {
    0: dict(x=0, y=0, z=1),
    1: dict(x=0, y=0, z=1),
    2: dict(x=0, y=0, z=1),
}

CENTERS = {
    0: dict(x=0.3, y=0.0, z=-0.5),
    1: dict(x=0, y=0, z=-0.37),
    2: dict(x=0, y=-0.7, z=0),
}

EYES = {
    0: dict(x=3.0, y=0.0, z=1.3),
    1: dict(x=0.01, y=3.8, z=-0.37),
    2: dict(x=2.6, y=-1.6, z=0),
}

TEXTS = {
    0:
    '''
    #### This is where we can explain the data or offer any info we want.
    This could be info on tests that have been done in the past or current test data.
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'''.replace('  ', ''),
    1: '''
    #### Another view with an opportunity to offer info.
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'''.replace('  ', ''),
    2: '''
    #### Last page of this waterfall display.
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'''.replace('  ', ''),
}


# Make 3d graph
@app.callback(Output('graph', 'figure'), [Input('slider', 'value')])
def make_graph(value):

    if value is None:
        value = 0

    if value in [0, 2]:
        z_secondary_beginning = [z[1] for z in zlist if z[0] == 'None']
        z_secondary_end = [z[0] for z in zlist if z[0] != 'None']
        z_secondary = z_secondary_beginning + z_secondary_end
        x_secondary = [
            '3-month'] * len(z_secondary_beginning) + ['1-month'] * len(z_secondary_end)
        y_secondary = ylist
        opacity = 0.7

    elif value == 1:
        x_secondary = xlist
        y_secondary = [ylist[-1] for i in xlist]
        z_secondary = zlist[-1]
        opacity = 0.7



    if value in range(0, 3):

        trace1 = dict(
            type="surface",
            x=xlist,
            y=ylist,
            z=zlist,
            hoverinfo='x+y+z',
            lighting={
                "ambient": 0.95,
                "diffuse": 0.99,
                "fresnel": 0.01,
                "roughness": 0.01,
                "specular": 0.01,
            },
            colorscale=[[0, "rgb(230,245,254)"], [0.4, "rgb(123,171,203)"], [
                0.8, "rgb(40,119,174)"], [1, "rgb(37,61,81)"]],
            opacity=opacity,
            showscale=False,
            zmax=9.18,
            zmin=0,
            scene="scene",
        )

        trace2 = dict(
            type='scatter3d',
            mode='lines',
            x=x_secondary,
            y=y_secondary,
            z=z_secondary,
            hoverinfo='x+y+z',
            line=dict(color='#444444')
        )

        data = [trace1, trace2]

    layout = dict(
        autosize=True,
        font=dict(
            size=12,
            color="#CCCCCC",
        ),
        margin=dict(
            t=5,
            l=50,
            b=5,
            r=50,
        ),
        showlegend=False,
        hovermode='closest',
        scene=dict(
            aspectmode="manual",
            aspectratio=dict(x=2, y=5, z=1.5),
            camera=dict(
                up=UPS[value],
                center=CENTERS[value],
                eye=EYES[value]
            ),
            xaxis={
                "showgrid": True,
                "title": "",
                "type": "category",
                "zeroline": False,
                "categoryorder": 'array',
                "categoryarray": list(reversed(xlist))
            },
            yaxis={
                "showgrid": True,
                "title": "",
                "type": "date",
                "zeroline": False,
            },
        )
    )

    figure = dict(data=data, layout=layout)
    return figure


# Display text in body
@app.callback(Output('text', 'children'), [Input('slider', 'value')])
def make_text(value):
    if value is None:
        value = 0

    return TEXTS[value]


# Contol Back/Next Btn
@app.callback(Output('slider', 'value'),
              [Input('back', 'n_clicks'), Input('next', 'n_clicks')],
              [State('slider', 'value')])
def advance_slider(back, nxt, slider):

    if back is None:
        back = 0
    if nxt is None:
        nxt = 0
    if slider is None:
        slider = 0

    global last_back
    global last_next

    if back > last_back:
        last_back = back
        return max(0, slider - 1)
    if nxt > last_next:
        last_next = nxt
        return min(2, slider + 1)


# Run Dash
if __name__ == '__main__':
    app.server.run()
