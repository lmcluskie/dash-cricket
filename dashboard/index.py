import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pathlib
import pandas as pd
from app import app, server
from utils import colors, fonts, header
from pages import batsmenGraphs

PATH = pathlib.Path(__file__)
DATA_PATH = PATH.joinpath("../data").resolve()

selected = ['V Kohli', 'SPD Smith']
df_main = pd.read_csv(DATA_PATH.joinpath("innings.csv"))
available_players = df_main['Name'].unique()

app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        
        html.Div(header()),

        html.Div(
            id='batsmenGraphs-head',
            children=[
                html.H3([
                    'Batsmen Compared'
                ],
                    style={
                        'textAlign': 'center',
                        'color': colors['title'],
                        'fontFamily': fonts['title'],
                        'position': 'relative',
                        'top': '-100px',
                        'left': '20%'
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
                                'width': '170px',
                                'display': 'inline-block',
                                'position': 'relative',
                                'top': '-20px',
                                'font-size': '12px',
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
                                'width': '170px',
                                'display': 'inline-block',
                                'position': 'relative',
                                'top': '-20px',
                                'font-size': '12px',
                            }
                        ),
                    ],
                    style={
                        'textAlign': 'center',
                        'padding-bottom': '0px',
                        'fontFamily': fonts['body'],
                        'position': 'relative',
                        'top': '-90px',
                        'left': '20%'
                    }
                )
            ]
        ),

        html.Div(
            id='page-content',
            style={
                'position':'relative',
                'top':'-70px',
            }
        )
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
        return batsmenGraphs.layout, {'display': 'block'}
    

if __name__ == '__main__':
    app.run_server()
