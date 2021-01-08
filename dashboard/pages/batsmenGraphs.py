import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table as dt
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import pathlib
from app import app
from utils import colors, fonts


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

update_date = open(DATA_PATH.joinpath("last_updated.txt"), "r").read()
bar_colors = [ '#EE442F','#E076D5', '#47D0E8', '#8DF279',  '#EF9A45', '#FFFCF4']
line_colors = ['#006DDB', '#D16C00', 'rgba(101, 252, 71, .4)', '#47D0E8', '#EF9A45']
grid_color = 'rgba(201, 201, 201, 0.5)'

df_main = pd.read_csv(DATA_PATH.joinpath("innings.csv"))
df_km = pd.read_csv(DATA_PATH.joinpath("survival.csv"))
df_km_overall = df_km[df_km['Name']=='overall']
df_haz = pd.read_csv(DATA_PATH.joinpath("hazard.csv"))
df_haz_overall = df_haz[df_haz['Name']=='overall']
df_sum = pd.read_csv(DATA_PATH.joinpath("summary.csv"))

df_dis = df_main[df_main.Dismissal != 'not out']
available_players = df_main['Name'].unique()
summary_columns = ['Name', 'Span', 'Mat', 'Inns', 'Runs', 'HS', 'Ave', '50', '100']
rolling_periods = [10, 20, 30, 40, 50, 70, 100]
slider_labels = [1896, 1910, 1920, 1930, 1939, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
teams = ['India', 'England', 'Australia', 'South Africa',
         'Pakistan', 'New Zealand', 'Sri Lanka', 'West Indies',
         'Bangladesh', 'Zimbabwe']

# app
right_column = [
    dcc.Graph(
        id='rolling-line-graph',
        style={
            'height': '450px',
            'backgroundColor': colors['paper']
        },
        config={
            'displayModeBar': False
        }
    ),
    html.Div([
            'Rolling Period Length: ',
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
            'textAlign': 'center',
            'textIndent': '10%',
            'color': colors['text'],
            'fontFamily': fonts['body'],
            'position': 'relative',
            'top':'-60px',
            'left': '25%'
        }
    ),
    dcc.Graph(
        id='dismissal-bar-graph',
        style={
            'height': '230px',
            'position': 'relative',
            'top': '-32px',
            'padding-bottom': '20px',
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
            'backgroundColor': colors['paper'],
            'position': 'relative',
            'top': '-40px',
        },
        config={
            'displayModeBar': False
        }
    ),
    html.Div([
        html.Div(
            'Date Range:',
            style={
                'position':'relative',
                'top':'20px',
                'left':'20px',
                'textAlign': 'left',
            }
        ),
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
                'display': 'inline-block',
                'position':'relative',
                'left':'20px',
            }
        )
        ],
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'backgroundColor': colors['paper'],
            'padding-bottom': '20px',
            'position': 'relative',
            'top': '-50px',
        }
    )
]
left_column = [
    html.Div(
        id='summary-table',
        style={
            'width': '100%',
            'display': 'inline-block',
            'position': 'relative',
            'top': '0px',
            'padding-bottom': '12px'
        }
    ),
    dcc.Graph(
        id='KM-line-graph',
        style={
            'height': '514px',
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
                   'Source code available here: ',
                    dcc.Link(href='https://github.com/lmcluskie/dash-cricket')
                ],
                style={
                    'textAlign': 'center',
                    'font-size': '14px',
                    'backgroundColor': colors['paper'],
                    'fontFamily': fonts['body']
                }
            ),
            html.Div([
                    f'All data sourced from ESPNcricinfo.com\'s Statsguru. Last updated {update_date}.'
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
                        'padding-left': '60px',
                        'position': 'relative',
                        'left': '20px'
                    }
                ),
                html.Div(
                    className='six columns',
                    children=right_column,
                    style={
                        'padding-right': '60px',
                        'position': 'relative',
                        'right': '20px'
                    }
                )
            ]
        )
    ],
    style={
            'backgroundColor': colors['background'],
            'position': 'relative',
            'top': '-25px'
        }
)


@app.callback(
    Output('summary-table', 'children'),
    [Input('first-player', 'value'),
     Input('second-player', 'value')])
def update_summary_table(first_player, second_player):
    df1 = df_sum[df_sum['Name'] == first_player]
    df2 = df_sum[df_sum['Name'] == second_player]
    
    column_titles = ['Name', 'Career Span', 'Matches', 'Innings', 'Runs',
                     'High Score', 'Average', '50s', '100s']
    column_widths=[
        {'if': {'column_id': 'Name'}, 'width': '22%'},
        {'if': {'column_id': 'Span'},'width': '15%'},
        {'if': {'column_id': 'Mat'}, 'width': '9%'},
        {'if': {'column_id': 'Inns'},'width': '9%'},
        {'if': {'column_id': 'Runs'}, 'width': '9%'},
        {'if': {'column_id': 'HS'},'width': '11%'},
        {'if': {'column_id': 'Ave'}, 'width': '11%'},
        {'if': {'column_id': '50'},'width': '7%'},
        {'if': {'column_id': '100'}, 'width': '7%'},        
    ]
    
    return [
        dt.DataTable(
            columns=[
                {'name': column_titles[i],
                 'id': summary_columns[i],
                 'editable': False}
                for i in range(len(column_titles))
            ],
            data=[],
            style_as_list_view=True,
            style_header={
                'backgroundColor': colors['paper'],
                'color': colors['text']
            },
            style_cell_conditional=column_widths        
        ),
        dt.DataTable(
            columns=[
                {'name': df1[i].iloc[0],
                 'id': f'{i}',
                 'editable': False}
                for i in summary_columns
            ],
            data=[],
            style_as_list_view=True,
            style_header={
                'backgroundColor': line_colors[0],
                'color': colors['text']
            },
            style_cell_conditional=column_widths        
        ),
        dt.DataTable(
            columns=[
                {'name': df2[i].iloc[0],
                 'id': f'{i}',
                 'editable': False}
                for i in summary_columns
            ],
            data=[],
            style_as_list_view=True,
            style_header={
                'backgroundColor': line_colors[1],
                'color': colors['text']
            },
            style_cell_conditional=column_widths        
        )        
    ]

@app.callback(
    Output('KM-line-graph', 'figure'),
    [Input('first-player', 'value'),
     Input('second-player', 'value'),
     Input('rolling-period', 'value')])
def update_km_line_graph(first_player, second_player, dummy):
    df1 = df_km[df_km['Name'] == first_player]
    df2 = df_km[df_km['Name'] == second_player]

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
    x3 = list(df_km_overall.time)
    x3rev = x3[::-1]
    y3 = df_km_overall.survival * 100
    upper3 = list(df_km_overall.upper * 100)
    lower3 = list(df_km_overall.lower * 100)
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
                    'color': line_colors[2],
                    'shape': 'hv'
                },
                name='Top 200 Combined'
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
                    'color': line_colors[2],
                    'shape': 'hv',
                    'dash': 'solid'
                },
                name='Top 200 Combined',
                visible=False
            )
        ],
        'layout': go.Layout(
            title=(
                'Survival Curve'
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
                'gridcolor': grid_color,
                'range': [0, 150]
            },
            yaxis={
                'title': 'Probability of being undismissed (%)',
                'showline': True,
                'linewidth': 2,
                'linecolor': colors['text'],
                'showgrid': True,
                'gridwidth': 1,
                'gridcolor': grid_color,
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
                l=80,
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
                            label="95% CI",
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
    career_ave_1 = [df1['Ave'].iloc[-1]] if len(df1)>0 else [None]
    career_ave_2 = [df2['Ave'].iloc[-1]] if len(df2)>0 else [None]
    most_innings = max(len(df1),len(df2))
    return {
        'data': [
            go.Scatter(
                x=list(range(len(df1))) if length is not None else None,
                y=df1[f'rolling{length}'] if length is not None else None,
                mode='lines',
                line={'color': line_colors[0]},
                name=f'ROLL {first_player}'
            ),
            go.Scatter(
                x=list(range(most_innings)),
                y=career_ave_1*most_innings,
                mode='lines',
                line={'color': line_colors[3]},
                name=f'OVR {first_player}'

            ),
            go.Scatter(
                x=list(range(len(df2))) if length is not None else None,
                y=df2[f'rolling{length}'] if length is not None else None,
                mode='lines',
                line={'color': line_colors[1]},
                name=f'ROLL {second_player}'
            ),
            go.Scatter(
                x=list(range(most_innings)),
                y=career_ave_2*most_innings,
                mode='lines',
                line={'color': line_colors[4]},
                name=f'OVR {second_player}'
            )
        ],
        'layout': go.Layout(
            title=(
                f'Rolling AVG ({length} inns) and Career AVG'
                if length is not None
                else 'Overall Average'
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
                'gridcolor': grid_color
            },
            yaxis={
                'title': 'Runs',
                'showline': True,
                'linewidth': 2,
                'linecolor': colors['text'],
                'showgrid': True,
                'gridwidth': 1,
                'gridcolor': grid_color,
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
                l=80,
                r=30,
                b=80,
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
    labels = list(dfcopy.Dismissal.value_counts().index)
    counts = [
        list(dfcopy.Dismissal.value_counts().values),
        list(df1.Dismissal.value_counts().values),
        list(df2.Dismissal.value_counts().values)
    ]
    categories = len(counts[0])
    for i in range(1, len(counts)):
        while len(counts[i]) < categories:
            counts[i].append(np.NaN)
    totals = [
        [dfcopy.Dismissal.value_counts().values.sum()] * categories,
        [df1.Dismissal.value_counts().values.sum()] * categories,
        [df2.Dismissal.value_counts().values.sum()] * categories
    ]
    props = np.array(counts) / np.array(totals)
    names = [
        'Top 200 Combined',
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
                l=120,
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
        values[0].append(np.NaN if dftemp.empty else round(dftemp.Runs.sum() / max(1, dftemp.Out.sum()), 2))
        dftemp = df2[df2['Opposition'] == team]
        values[1].append(np.NaN if dftemp.empty else round(dftemp.Runs.sum() / max(1, dftemp.Out.sum()), 2))
        dftemp = dfcopy[dfcopy['Opposition'] == team]
        values[2].append(np.NaN if dftemp.empty else round(dftemp.Runs.sum() / max(1, dftemp.Out.sum()), 2))
    names = [
        first_player,
        second_player,
        'Top 200 Combined'
    ]
    data = []
    for i in range(len(names)):
        data.append(
            go.Bar(
                y=values[i],
                x=teams,
                name=names[i],
                text=[int(n) if n == n else '' for n in values[i]],
                textposition='outside',
                hoverinfo='y+name',
                marker={
                    'color': line_colors[i],
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
                'gridcolor': grid_color,
                'range': [0, np.nanmax(values)+10]
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
                l=80,
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
                x=list(range(121)),
                y=df1['Smooth2 Haz'],
                mode='lines',
                line={
                    'color': line_colors[0],
                },
                name=f'{first_player}'
            ),
            go.Scatter(
                x=list(range(121)),
                y=df2['Smooth2 Haz'],
                mode='lines',
                line={
                    'color': line_colors[1],
                },
                name=f'{second_player}'
            ),
            go.Scatter(
                x=list(range(121)),
                y=df_haz_overall['Smooth2 Haz'],
                mode='lines',
                line={
                    'color': line_colors[2],
                },
                name='Top 200 Combined'
            ),
        ],
        'layout': go.Layout(
            title=(
                'Dismissal Rate through Innings'
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
                'gridcolor': grid_color
            },
            yaxis={
                'title': 'Hazard Rate',
                'showline': True,
                'linewidth': 2,
                'linecolor': colors['text'],
                'showgrid': True,
                'gridwidth': 1,
                'gridcolor': grid_color,
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
                l=80,
                r=30,
                b=40,
                t=80,
                pad=3
            ),
            plot_bgcolor=colors['paper'],
            paper_bgcolor=colors['paper']
        )
    }
