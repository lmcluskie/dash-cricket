import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import numpy as np
import pandas as pd
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
teams = [
    'India', 'England', 'Australia', 'South Africa', 'Pakistan', 'New Zealand',
    'Sri Lanka', 'West Indies', 'Bangladesh', 'Zimbabwe'
]

dismissal_table_columns = ['Name'] + list(df_main['DisType'].unique())
dismissal_table_data = {i: [] for i in dismissal_table_columns}
for name in available_players:
    df = df_main[df_main['Name'] == name]
    counts = df['DisType'].value_counts().to_dict()
    total = sum(counts.values())
    dismissal_table_data['Name'].append(name)
    for i in dismissal_table_columns[1:]:
        try:
            dismissal_table_data[i].append(round(counts[i]/total * 100, 2))
        except KeyError:
            dismissal_table_data[i].append(0)
dismissal_df = pd.DataFrame(data=dismissal_table_data)

rolling_periods = [10, 20, 30, 40, 50, 70, 100]
rolling_table_columns = ['Name', 'Overall'] + [f'Max {i}' for i in rolling_periods]
rolling_table_data = {i: [] for i in rolling_table_columns}
for name in available_players:
    df = df_main[df_main['Name'] == name]
    rolling_table_data['Name'].append(name)
    rolling_table_data['Overall'].append(round(df.Tally.max() / df.Dismissal.max(), 2))
    for i in rolling_periods:
        rolling_table_data[f'Max {i}'].append(round(df[f'rolling{i}'].max(), 2))
rolling_df = pd.DataFrame(data=rolling_table_data)

# app

layout = html.Div(
    [
        html.H3([
                'Sortable tables of the top 200 run scorers in test matches (min ave 35)'
            ],
            style={
                'textAlign': 'center',
                'color': colors['title']
            }
        ),
        html.H6([
            'Rolling Averages ("Max x" is the players peak rolling average over x innings)'
        ],
            style={
                'textAlign': 'center',
                'color': colors['title']
            }
        ),
        html.Div([
                dash_table.DataTable(
                    id='rolling-table',
                    columns=[{'name': i, 'id': i} for i in rolling_table_columns],
                    data=rolling_df.to_dict('records'),
                    editable=False,
                    style_as_list_view=False,
                    sort_action='native',
                    style_header={
                        'backgroundColor': colors['paper'],
                        'fontWeight': 'bold',
                        'color': colors['title']
                    },
                    fixed_rows={'headers': True, 'data': 0},
                    style_cell={
                        'fontFamily': fonts['body'],
                        'backgroundColor': colors['text'],
                        'color': '#000000',
                        'textAlign': 'center'
                    },
                    css=[
                        {'selector': 'td.cell--selected, td.focused', 'rule': 'background-color: #D6D6D6 !important;'},
                        {'selector': 'td.cell--selected *, td.focused *', 'rule': 'color: #000000 !important;'}
                    ]
                ),
            ],
            style={
                'width': '900px',
                'display': 'inline-block',
                'padding-bottom': '20px'
            }
        ),
        html.H6([
                'Survival Rates (%)'
            ],
            style={
                'textAlign': 'center',
                'color': colors['title']
            }
        ),
        html.Div([
                'Custom Range:       .',
                html.Div(
                    children=[
                        dcc.RangeSlider(
                            id='survival-table-slider',
                            min=0,
                            max=201,
                            step=10,
                            marks={
                                int(i): {
                                    'label': i,
                                    'style': {'color': colors['text']}
                                }
                                for i in range(0,201,10)
                            },
                            value=[0, 100]
                        ),
                    ],
                    style={
                        'width': '800px',
                        'display': 'inline-block',
                    }
                ),
            ],
            style={
                'color': colors['text'],
                'padding-bottom': '20px'
            }
        ),
        html.Div(
            id='survival-table',
            style={
                'width': '900px',
                'display': 'inline-block',
                'padding-bottom': '20px'
            },
        ),
        html.H6([
                'Methods of Dismissal (%)'
            ],
            style={
                'textAlign': 'center',
                'color': colors['title']
            }
        ),
        html.Div([
                dash_table.DataTable(
                    id='dismissal-table',
                    columns=[{'name': i, 'id': i} for i in dismissal_table_columns],
                    data=dismissal_df.to_dict('records'),
                    editable=False,
                    style_as_list_view=False,
                    sort_action='native',
                    style_header={
                        'backgroundColor': colors['paper'],
                        'fontWeight': 'bold',
                        'color': colors['title']
                    },
                    fixed_rows={'headers': True, 'data': 0},
                    style_cell={
                        'fontFamily': fonts['body'],
                        'backgroundColor': colors['text'],
                        'color': '#000000',
                        'textAlign': 'center'
                    },
                    css=[
                        {'selector': 'td.cell--selected, td.focused', 'rule': 'background-color: #D6D6D6 !important;'},
                        {'selector': 'td.cell--selected *, td.focused *', 'rule': 'color: #000000 !important;'}
                    ]
                ),
            ],
            style={
                'width': '900px',
                'display': 'inline-block',
                'padding-bottom': '20px'
            }
        ),
    ],

    style={
        'textAlign': 'center',
        'backgroundColor': colors['background'],
        'fontFamily': fonts['title']
    }
)

@app.callback(
    Output('survival-table', 'children'),
    [Input('survival-table-slider', 'value')])
def update_survival_table(scores):
    survival_table_columns = [
        'Name', 'Survival from 0 to 50', 'Survival from 50 to 100', f'Custom Range ({scores[0]} to {scores[1]})'
    ]
    survival_table_data = {i: [] for i in survival_table_columns}
    for name in available_players:
        survival_table_data['Name'].append(name)
        df_player = df_KM[(df_KM['Name'] == name)]
        df = df_player[df_player['time'] <= 50]
        surv_50 = df.survival.min()
        survival_table_data[f'Survival from 0 to 50'].append(round(surv_50 * 100, 2))
        df = df_player[df_player['time'] <= 100]
        surv_100 = df.survival.min()
        survival_table_data[f'Survival from 50 to 100'].append(round(surv_100 / surv_50 * 100, 2))
        df = df_player[(df_player['time'] >= scores[0]) & (df_player['time'] <= scores[1])]
        survival_table_data[f'Custom Range ({scores[0]} to {scores[1]})'].append(round(df.survival.min()/df.survival.max() * 100, 2))
        survival_df = pd.DataFrame(data=survival_table_data)
    survival_df.sort_values(by=f'Custom Range ({scores[0]} to {scores[1]})', ascending=False, inplace=True)

    return dash_table.DataTable(
        columns=[{'name': i, 'id': i} for i in survival_table_columns],
        data=survival_df.to_dict('records'),
        editable=False,
        style_as_list_view=False,
        sort_action='native',
        style_header={
            'backgroundColor': colors['paper'],
            'fontWeight': 'bold',
            'color': colors['title']
        },
        fixed_rows={'headers': True, 'data': 0},
        style_cell={
            'fontFamily': fonts['body'],
            'backgroundColor': colors['text'],
            'color': '#000000',
            'textAlign': 'center'
        },
        style_cell_conditional=[
            {'if': {'column_id': 'Name'},
             'width': '30%'}
        ],
        css=[
            {'selector': 'td.cell--selected, td.focused', 'rule': 'background-color: #D6D6D6 !important;'},
            {'selector': 'td.cell--selected *, td.focused *', 'rule': 'color: #000000 !important;'}
        ]
    )
