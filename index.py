import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pathlib
import pandas as pd
from app import app
from utils import colors, fonts, header
from pages import (
    batsmenGraphs,
    batsmenSummary
)

PATH = pathlib.Path(__file__)
DATA_PATH = PATH.joinpath("../data").resolve()

selected = ['V Kohli', 'SPD Smith']
df_main = pd.read_csv(DATA_PATH.joinpath("rollingMaster.csv"))
available_players = df_main['Name'].unique()

app.layout = html.Div([
        dcc.Location(id='url', refresh=False),

        html.Div(header()),

        html.Div(
            id='batsmenGraphs-head',
            children=[
                html.H3([
                    'Pick batsmen to visually compare performance summaries'
                ],
                    style={
                        'textAlign': 'center',
                        'color': colors['title'],
                        'fontFamily': fonts['title']
                    }
                ),

                html.Div([
                        html.Div([
                            dcc.Dropdown(
                                id='first-player',
                                options=[{'label': i, 'value': i} for i in available_players],
                                value=selected[0]
                            )
                        ],
                            style={
                                'width': '300px',
                                'display': 'inline-block'
                            }
                        ),
                        html.Div([
                            dcc.Dropdown(
                                id='second-player',
                                options=[{'label': i, 'value': i} for i in available_players],
                                value=selected[1]
                            )
                        ],
                            style={
                                'width': '300px',
                                'display': 'inline-block'
                            }
                        ),
                    ],
                    style={
                        'textAlign': 'center',
                        'padding-bottom': '15px',
                        'fontFamily': fonts['body']
                    }
                )
            ]
        ),

        html.Div(id='page-content')
    ],
    style={
        'backgroundColor': colors['background']
    }
)


@app.callback(
    [Output('page-content', 'children'),
     Output('batsmenGraphs-head', 'style')],
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/BatsmenGraphs':
        return batsmenGraphs.layout, {'display': 'block'}
    elif pathname == '/BatsmenSummary':
        return batsmenSummary.layout, {'display': 'none'}
    else:
        return batsmenSummary.layout, {'display': 'none'}


if __name__ == '__main__':
    app.run_server()
