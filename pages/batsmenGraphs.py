import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import pathlib
from app import app
from utils import colors, fonts

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

bar_colors = ['#47D0E8', '#EF9A45', '#8DF279', '#E076D5', '#EE442F', '#FFFCF4']
line_colors = ['#47D0E8', '#EF9A45', '#006DDB', '#D16C00', '#8DF279']
df_main = pd.read_csv(DATA_PATH.joinpath("rollingMaster.csv"))
df_dis = df_main[df_main.DisType != 'not out']
df_KM = pd.read_csv(DATA_PATH.joinpath("kmMaster.csv"))
df_KM_OVR = pd.read_csv(DATA_PATH.joinpath("kmOverall.csv"))
df_haz = pd.read_csv(DATA_PATH.joinpath("hazMaster.csv"))
df_haz_OVR = pd.read_csv(DATA_PATH.joinpath("hazOverall.csv"))
available_players = df_main['Name'].unique()
rolling_periods = [10, 20, 30, 40, 50, 70, 100]
slider_labels = [1896, 1910, 1920, 1930, 1939, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2019]
teams = ['India', 'England', 'Australia', 'South Africa',
         'Pakistan', 'New Zealand', 'Sri Lanka', 'West Indies',
         'Bangladesh', 'Zimbabwe']

# app
left_column = [
    dcc.Graph(
        id='rolling-line-graph',
        style={
            'height': '500px',
            'backgroundColor': colors['paper']
        },
        config={
            'displayModeBar': False
        }
    ),
    html.Div([
            'Length of rolling average periods: ',
            html.Div(
                children=[
                    dcc.Dropdown(
                        className='dropdown-period',
                        id='rolling-period',
                        options=[{'label': i, 'value': i} for i in rolling_periods],
                        value=30
                    ),
                ],
                style={
                    'width': '80px',
                    'display': 'inline-block',
                    'color': '#000000',
                    'position': 'relative',
                    'top': '12px',
                    'textAlign': 'left',
                    'fontFamily': fonts['body']
                }
            ),
        ],
        style={
            'textAlign': 'left',
            'textIndent': '10%',
            'color': colors['text'],
            'backgroundColor': colors['paper'],
            'padding-bottom': '20px',
            'fontFamily': fonts['body']
        }
    ),
    dcc.Graph(
        id='dismissal-bar-graph',
        style={
            'height': '250px',
            'position': 'relative',
            'top': '12px',
            'padding-bottom': '12px',
            'backgroundColor': colors['paper']
        },
        config={
            'displayModeBar': False
        }
    ),
    dcc.Graph(
        id='opposition-bar-graph',
        style={
            'height': '390px',
            'backgroundColor': colors['paper']
        },
        config={
            'displayModeBar': False
        }
    ),
    html.Div([
        'Date Range:    .',
        html.Div(
            children=[
                dcc.RangeSlider(
                    id='dismissal-bar-slider',
                    min=df_main.Date.min(),
                    max=df_main.Date.max(),
                    marks={
                        int(i): {
                            'label': str(i) if int(i) in slider_labels else None,
                            'style': {'color': colors['text']}
                        }
                        for i in df_main.Date.unique()
                    },
                    value=[df_main.Date.min(), df_main.Date.max()]
                ),
            ],
            style={
                'width': '80%',
                'display': 'inline-block'
            }
        ),
    ],
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'backgroundColor': colors['paper'],
            'padding-bottom': '20px'
        }
    )
]
right_column = [
    dcc.Graph(
        id='KM-line-graph',
        style={
            'height': '650px',
            'padding-bottom': '20px',
            'backgroundColor': colors['paper']
        },
        config={
            'displayModeBar': False
        }
    ),
    dcc.Graph(
        id='hazard-line-graph',
        style={
            'height': '450px',
            'padding-bottom': '20px',
            'backgroundColor': colors['paper'],
            'position': 'relative',
            'top': '12px'
        },
        config={
            'displayModeBar': False
        }
    ),
    html.Div([
            html.Div([
                    ''' All data sourced from cricinfo statsguru, last updated 17/Nov/2019.                
                        Kaplan Meier confidence bands calculated using BPCP. 
                        Kernel density plot made using the reflection method and a linear kernel with bandwidth 20.
                    '''
                ],
                style={
                    'textAlign': 'center',
                    'font-size': '14px',
                    'backgroundColor': colors['paper'],
                    'fontFamily': fonts['body']
                }
            )
        ],
            style={
                'color': colors['text'],
                'position': 'relative',
                'top': '22px',
                'backgroundColor': colors['paper'],
                'padding-top': '10px',
                'padding-bottom': '10px'
            }
    )
]


layout = html.Div(
    [
        html.Div(
            className='row no-pad',
            children=[
                html.Div(
                    className='six columns',
                    children=left_column,
                    style={
                        'padding-left': '30px'
                    }
                ),
                html.Div(
                    className='six columns',
                    children=right_column,
                    style={
                        'padding-right': '30px'
                    }
                )
            ]
        )
    ],
    style={
            'backgroundColor': colors['background']
        }
)


@app.callback(
    Output('KM-line-graph', 'figure'),
    [Input('first-player', 'value'),
     Input('second-player', 'value'),
     Input('rolling-period', 'value')])
def update_km_line_graph(first_player, second_player, dummy):
    df1 = df_KM[df_KM['Name'] == first_player]
    df2 = df_KM[df_KM['Name'] == second_player]

    x1 = list(df1.time)
    x1rev = x1[::-1]
    y1 = df1.survival * 100
    upper1 = list(df1.upper * 100)
    lower1 = list(df1.lower * 100)
    lower1 = lower1[::-1]
    x2 = list(df2.time)
    x2rev = x2[::-1]
    y2 = df2.survival * 100
    upper2 = list(df2.upper * 100)
    lower2 = list(df2.lower * 100)
    lower2 = lower2[::-1]
    x3 = list(df_KM_OVR.time)
    x3rev = x3[::-1]
    y3 = df_KM_OVR.survival * 100
    upper3 = list(df_KM_OVR.upper * 100)
    lower3 = list(df_KM_OVR.lower * 100)
    lower3 = lower3[::-1]

    return {
        'data': [
            go.Scatter(
                x=x1,
                y=y1,
                mode='lines',
                line={
                    'color': line_colors[0],
                    'shape': 'hv'
                },
                name=f'{first_player}'
            ),
            go.Scatter(
                x=x2,
                y=y2,
                mode='lines',
                line={
                    'color': line_colors[1],
                    'shape': 'hv'
                },
                name=f'{second_player}'
            ),
            go.Scatter(
                x=x3,
                y=y3,
                mode='lines',
                line={
                    'color': line_colors[4],
                    'shape': 'hv'
                },
                name=f'Top 200'
            ),
            go.Scatter(
                x=x1rev + x1,
                y=lower1 + upper1,
                line={
                    'color': line_colors[0],
                    'shape': 'hv',
                    'dash': 'solid'
                },
                name=f'{first_player}',
                visible=False
            ),
            go.Scatter(
                x=x2rev + x2,
                y=lower2 + upper2,
                line={
                    'color': line_colors[1],
                    'shape': 'hv',
                    'dash': 'solid'
                },
                name=f'{second_player}',
                visible=False
            ),
            go.Scatter(
                x=x3rev + x3,
                y=lower3 + upper3,
                line={
                    'color': line_colors[4],
                    'shape': 'hv',
                    'dash': 'solid'
                },
                name='Top 200',
                visible=False
            )
        ],
        'layout': go.Layout(
            title=(
                'Survival Curve (Kaplan-Meier plot)'
            ),
            titlefont={
                'color': colors['title'],
                'family': fonts['title']
            },
            xaxis={
                'title': 'Runs',
                'showline': True,
                'linewidth': 2,
                'linecolor': colors['text'],
                'showgrid': True,
                'gridwidth': 1,
                'gridcolor': colors['text'],
                'range': [0, 150]
            },
            yaxis={
                'title': 'Survival (%)',
                'showline': True,
                'linewidth': 2,
                'linecolor': colors['text'],
                'showgrid': True,
                'gridwidth': 1,
                'gridcolor': colors['text'],
                'range': [0, 100],
                'hoverformat': '.2f'
            },
            legend={
                'orientation': 'h',
                'y': 1.06,
                'x': 0
            },
            font={
                'color': colors['text'],
                'family': fonts['body']
            },
            margin=go.layout.Margin(
                l=60,
                r=30,
                b=40,
                t=80,
                pad=3
            ),
            plot_bgcolor=colors['paper'],
            paper_bgcolor=colors['paper'],
            updatemenus=[
                go.layout.Updatemenu(
                    buttons=list([
                        dict(
                            args=[{"visible": [True] * 3 + [False] * 3}],
                            label="Point Estimates",
                            method="restyle"
                        ),
                        dict(
                            args=[{"visible": [False] * 3 + [True] * 3}],
                            label="95% Confidence Bands",
                            method="restyle"
                        )
                    ]),
                    type="buttons",
                    direction="down",
                    x=1,
                    y=1
                )
            ]
        )
    }


@app.callback(
    Output('rolling-line-graph', 'figure'),
    [Input('first-player', 'value'),
     Input('second-player', 'value'),
     Input('rolling-period', 'value')])
def update_rolling_line_graph(first_player, second_player, length):
    df1 = df_main[df_main['Name'] == first_player]
    df2 = df_main[df_main['Name'] == second_player]
    return {
        'data': [
            go.Scatter(
                x=list(range(10, len(df1))) if length is not None else None,
                y=df1[f'rolling{length}'][10:] if length is not None else None,
                mode='lines',
                line={'color': line_colors[0]},
                name=f'ROLL {first_player}'
            ),
            go.Scatter(
                x=list(range(10, len(df2))) if length is not None else None,
                y=df2[f'rolling{length}'][10:] if length is not None else None,
                mode='lines',
                line={'color': line_colors[1]},
                name=f'ROLL {second_player}'
            ),
            go.Scatter(
                x=list(range(10, len(df1))),
                y=df1.Ave[10:],
                mode='lines',
                line={'color': line_colors[2]},
                name=f'OVR {first_player}'

            ),
            go.Scatter(
                x=list(range(10, len(df2))),
                y=df2.Ave[10:],
                mode='lines',
                line={'color': line_colors[3]},
                name=f'OVR {second_player}'
            )
        ],
        'layout': go.Layout(
            title=(
                f'Overall Average and {length} innings Rolling Average'
                if length is not None
                else 'Progression of Overall Average'
            ),
            titlefont={
                'color': colors['title'],
                'family': fonts['title']
            },
            xaxis={
                'title': 'Innings',
                'showline': True,
                'linewidth': 2,
                'linecolor': colors['text'],
                'showgrid': True,
                'gridwidth': 1,
                'gridcolor': colors['text']
            },
            yaxis={
                'title': 'Runs',
                'showline': True,
                'linewidth': 2,
                'linecolor': colors['text'],
                'showgrid': True,
                'gridwidth': 1,
                'gridcolor': colors['text'],
                'hoverformat': '.2f'
            },
            legend={
                'orientation': 'h',
                'y': 1.09,
                'x': 0
            },
            font={
                'color': colors['text'],
                'family': fonts['body']
            },
            margin=go.layout.Margin(
                l=50,
                r=30,
                b=40,
                t=80,
                pad=3
            ),
            plot_bgcolor=colors['paper'],
            paper_bgcolor=colors['paper']
        )
    }


@app.callback(
    Output('dismissal-bar-graph', 'figure'),
    [Input('first-player', 'value'),
     Input('second-player', 'value'),
     Input('dismissal-bar-slider', 'value')])
def update_dismissal_bar_graph(first_player, second_player, dates):
    dfcopy = df_dis[(df_dis['Date'] >= dates[0]) & (df_dis['Date'] <= dates[1])]
    df2 = dfcopy[dfcopy['Name'] == first_player]
    df1 = dfcopy[dfcopy['Name'] == second_player]
    labels = list(dfcopy.DisType.value_counts().index)
    counts = [
        list(dfcopy.DisType.value_counts().values),
        list(df1.DisType.value_counts().values),
        list(df2.DisType.value_counts().values)
    ]
    categories = len(counts[0])
    for i in range(1, len(counts)):
        while len(counts[i]) < categories:
            counts[i].append(np.NaN)
    totals = [
        [dfcopy.DisType.value_counts().values.sum()] * categories,
        [df1.DisType.value_counts().values.sum()] * categories,
        [df2.DisType.value_counts().values.sum()] * categories
    ]
    props = np.array(counts) / np.array(totals)
    names = [
        'Top 200',
        second_player,
        first_player
    ]
    data = []
    for i in range(categories):
        data.append(
            go.Bar(
                y=names,
                x=props[:, i],
                name=labels[i],
                orientation='h',
                text=np.array(counts)[:, i],
                hoverinfo='text',
                marker={
                    'color': bar_colors[i],
                }
            )
        )
    return {
        'data': data,
        'layout': go.Layout(
            title=f'Mode of Dismissal ({dates[0]}-{dates[1]})',
            titlefont={
                'color': colors['title'],
                'family': fonts['title']
            },
            xaxis={
                'title': 'Proportion',
                'domain': [0, 1]
            },
            font={
                'color': colors['text'],
                'family': fonts['body']
            },
            barmode='stack',
            margin=go.layout.Margin(
                l=80,
                r=20,
                b=40,
                t=60,
                pad=3
            ),
            plot_bgcolor=colors['paper'],
            paper_bgcolor=colors['paper']
        )
    }


@app.callback(
    Output('opposition-bar-graph', 'figure'),
    [Input('first-player', 'value'),
     Input('second-player', 'value'),
     Input('dismissal-bar-slider', 'value')])
def update_opposition_bar_graph(first_player, second_player, dates):
    dfcopy = df_main[(df_main['Date'] >= dates[0]) & (df_main['Date'] <= dates[1])]
    df1 = dfcopy[dfcopy['Name'] == first_player]
    df2 = dfcopy[dfcopy['Name'] == second_player]
    values = [[], [], []]
    for team in teams:
        dftemp = df1[df1['Opposition'] == team]
        values[0].append(np.NaN if dftemp.empty else round(dftemp.Runs.sum() / max(1, dftemp.Dismissed.sum()), 2))
        dftemp = df2[df2['Opposition'] == team]
        values[1].append(np.NaN if dftemp.empty else round(dftemp.Runs.sum() / max(1, dftemp.Dismissed.sum()), 2))
        dftemp = dfcopy[dfcopy['Opposition'] == team]
        values[2].append(np.NaN if dftemp.empty else round(dftemp.Runs.sum() / max(1, dftemp.Dismissed.sum()), 2))
    names = [
        first_player,
        second_player,
        'Top 200'
    ]
    data = []
    for i in range(len(names)):
        data.append(
            go.Bar(
                y=values[i],
                x=teams,
                name=names[i],
                text=[int(n) if n == n else n for n in values[i]],
                textposition='outside',
                hoverinfo='y+name',
                marker={
                    'color': bar_colors[i],
                }
            )
        )
    return {
        'data': data,
        'layout': go.Layout(
            title=f'Average by Opposition ({dates[0]}-{dates[1]})',
            titlefont={
                'color': colors['title'],
                'family': fonts['title']
            },
            yaxis={
                'title': 'Runs',
                'showgrid': True,
                'gridwidth': 1,
                'gridcolor': colors['text']
            },
            font={
                'color': colors['text'],
                'family': fonts['body']
            },
            legend={
                'orientation': 'h',
                'y': 1.09,
                'x': 0
            },
            margin=go.layout.Margin(
                l=50,
                r=30,
                b=60,
                t=60,
                pad=3
            ),
            plot_bgcolor=colors['paper'],
            paper_bgcolor=colors['paper']
        )
    }


@app.callback(
    Output('hazard-line-graph', 'figure'),
    [Input('first-player', 'value'),
     Input('second-player', 'value'),
     Input('rolling-period', 'value')])
def update_hazard_line_graph(first_player, second_player, dummy):
    df1 = df_haz[df_haz['Name'] == first_player]
    df2 = df_haz[df_haz['Name'] == second_player]

    return {
        'data': [
            go.Scatter(
                x=df1.time[:121],
                y=df1.hazard[:121],
                mode='lines',
                line={
                    'color': line_colors[0],
                },
                name=f'{first_player}'
            ),
            go.Scatter(
                x=df2.time[:121],
                y=df2.hazard[:121],
                mode='lines',
                line={
                    'color': line_colors[1],
                },
                name=f'{second_player}'
            ),
            go.Scatter(
                x=df_haz_OVR.time[:121],
                y=df_haz_OVR.hazard[:121],
                mode='lines',
                line={
                    'color': line_colors[4],
                },
                name=f'Top 200'
            ),
        ],
        'layout': go.Layout(
            title=(
                f'Hazard Rate vs Batsman\'s Score'
            ),
            titlefont={
                'color': colors['title'],
                'family': fonts['title']
            },
            xaxis={
                'title': 'Runs',
                'showline': True,
                'linewidth': 2,
                'linecolor': colors['text'],
                'showgrid': True,
                'gridwidth': 1,
                'gridcolor': colors['text']
            },
            yaxis={
                'title': 'Hazard Rate',
                'showline': True,
                'linewidth': 2,
                'linecolor': colors['text'],
                'showgrid': True,
                'gridwidth': 1,
                'gridcolor': colors['text'],
                'hoverformat': '.4f'
            },
            legend={
                'orientation': 'h',
                'y': 1.1,
                'x': 0
            },
            font={
                'color': colors['text'],
                'family': fonts['body']
            },
            margin=go.layout.Margin(
                l=60,
                r=30,
                b=40,
                t=80,
                pad=3
            ),
            plot_bgcolor=colors['paper'],
            paper_bgcolor=colors['paper']
        )
    }
