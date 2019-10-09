import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import pathlib

PATH = pathlib.Path(__file__)
DATA_PATH = PATH.joinpath("../data").resolve()

#setup
colors = {
    'background':'#1D313F',
    'paper': '#192A35',
    'text':'#D6D6D6',
    'title':'#FFFFFF'
}
df_main = pd.read_csv(DATA_PATH.joinpath("rollingMaster.csv"))
df_dis = df_main[df_main.DisType != 'not out']
df_KM = pd.read_csv(DATA_PATH.joinpath("kmMaster.csv"))
df_KM_OVR = pd.read_csv(DATA_PATH.joinpath("kmOverall.csv"))
df_haz = pd.read_csv(DATA_PATH.joinpath("hazMaster.csv")) 
df_haz_OVR = pd.read_csv(DATA_PATH.joinpath("hazOverall.csv"))
available_players = df_main['Name'].unique()
rolling_periods = [10, 20, 30, 40, 50, 70, 100]
dates = [1896,1910,1920,1930,1939,1950,1960,1970,1980,1990,2000,2010,2019]
bar_colors = ['#006DDB', '#D16C00', '#E076D5', '#EE442F', '#63ACBE', '#F9F4EC']
line_colors = ['#006DDB', '#D16C00','#00CBFF', '#FFE605', '#E076D5', '#8C4A85']  
teams =['India', 'England', 'Australia', 'South Africa', 'Pakistan', 
        'New Zealand', 'Sri Lanka', 'West Indies', 'Bangladesh', 'Zimbabwe']
tabtitle='Cricket Dashboard'

#initiate
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

#app
left_column=[
    dcc.Graph(
        id='rolling-line-graph',
        style={
            'height':'500px',
            'backgroundColor':colors['paper']                              
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
                'textAlign': 'left'
            }
        ),
        ],
        style={
            'textAlign':'left',
            'textIndent':'10%',
            'color': colors['text'],
            'backgroundColor':colors['paper'],
            'padding-bottom': '20px'
        }
    ),
    dcc.Graph(
        id='opposition-bar-graph',
        style={
            'height':'400px',
            'position': 'relative',
            'top': '12px',
            'padding-bottom': '20px',
            'backgroundColor':colors['paper']
        }
    ),
    dcc.Graph(
        id='dismissal-bar-graph',
        style={
            'height':'210px',
            'padding-bottom': '10px',
            'backgroundColor':colors['paper']
        }
    ),
    html.Div([
        'Date Range:    .',
        html.Div(
            children=[
                dcc.RangeSlider(
                    id='dismissal-bar-slider',
                    min=min(df_main.Date),
                    max=max(df_main.Date),
                    marks={
                        int(i): {
                            'label': i if i in dates else None, 
                            'style':{'color':colors['text']}
                        } 
                        for i in df_main.Date.unique()
                    },
                    value=[min(df_main.Date),max(df_main.Date)]
                ),
            ],
            style={
                'width': '80%',
                'display': 'inline-block'
            }
        ),
        ],
        style={
            'textAlign':'center',
            'color': colors['text'],
            'backgroundColor':colors['paper'],
            'padding-bottom': '20px'
        }
    )    
]
right_column=[
    dcc.Graph(
        id='KM-line-graph',
        style={
            'height':'650px',
            'padding-bottom': '20px',
            'backgroundColor':colors['paper'] 
        }
    ),
    dcc.Graph(
        id='hazard-line-graph',
        style={
            'height':'400px',
            'padding-bottom': '20px',
            'backgroundColor':colors['paper'],
            'position': 'relative',
            'top': '12px'
        }
    ),
    html.Div([                                   
        'Smoothing Applied: ',                            
        html.Div(
            children=[
                dcc.Dropdown(
                className='dropdown-period',
                id='hazard-smoothing',
                options=[
                    {'label': 'Low', 'value': 'hazard1'},
                    {'label': 'Medium', 'value': 'hazard2'},
                    {'label': 'High', 'value': 'hazard3'}
                ],
                value='hazard2'
            ),
            ],
            style={
                'width': '120px',
                'display': 'inline-block',
                'color': '#000000',
                'position': 'relative',
                'top': '12px',
                'textAlign': 'left'
            }
        ),
        ],
        style={
            'textAlign':'left',
            'textIndent':'10%',
            'color': colors['text'],
            'backgroundColor':colors['paper'],
            'padding-bottom': '20px'
        }
    ),
    html.Div([
        html.Div([ 
                '''All data sourced from cricinfo statsguru, last updated 07/Oct/19.                
                KM confidence intervals calculated using BPCP. Non-rigorous smoothing performed
                using the reflection method and a simple uniform kernel of varying bandwidths.'''
            ],
            style={
                'textAlign':'center',
                'font-size': '12px',
                'backgroundColor':colors['paper']
            }
        )
        ],
        style={
            'color': colors['text'],
            'position': 'relative',
            'top': '12px',
            'backgroundColor':colors['paper'],
            'padding-top': '10px',
            'padding-bottom': '10px'
        }
    )    
]

app.layout = html.Div([
        html.H1([
            'International Cricket'
            ],
            style={
                'textAlign':'center',
                'color': colors['title'],
                'padding-top': '20px'
            }
        ),
        
        html.H3([
            'Compare performance summaries of the top 200 runscorers in test matches (min ave 35)'
            ],
            style={
                'textAlign':'center',
                'color': colors['title']
            }
        ),
        
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='first-player',
                    options=[{'label': i, 'value': i} for i in available_players],
                    value='V Kohli'
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
                    value='SPD Smith'
                    )
                ],
                style={
                    'width': '300px',
                    'display': 'inline-block'
                }
            ),
            ],
            style={
                'textAlign':'center',
                'padding-bottom': '15px'                 
            }
        ),
        
        html.Div(
            className='row no-pad',
            children=[
                html.Div(
                    className='six columns',
                    children=left_column,
                    style={
                        'padding-left':'30px'
                    }
                ),
                html.Div(
                    className='six columns',
                    children=right_column,
                    style={
                        'padding-right':'30px'
                    }
                )
            ]
        )
    ],
    style={
        'backgroundColor':colors['background']
    },
)
            
@app.callback(
    Output('KM-line-graph', 'figure'),
    [Input('first-player', 'value'),
     Input('second-player', 'value'),
     Input('rolling-period', 'value')])
def update_KM_line_graph(first_player, second_player, length):
    df1 = df_KM[df_KM['Name'] == first_player]
    df2 = df_KM[df_KM['Name'] == second_player]
    
    x1 = list(df1.time)
    x1rev = x1[::-1]
    y1 = df1.survival*100
    upper1 = list(df1.upper*100)
    lower1 = list(df1.lower*100)
    lower1 = lower1[::-1]    
    x2 = list(df2.time)
    x2rev = x2[::-1]
    y2 = df2.survival*100
    upper2 = list(df2.upper*100)
    lower2 = list(df2.lower*100)
    lower2 = lower2[::-1]
    x3 = list(df_KM_OVR.time)
    x3rev = x3[::-1]
    y3 = df_KM_OVR.survival*100
    upper3 = list(df_KM_OVR.upper*100)
    lower3 = list(df_KM_OVR.lower*100)
    lower3 = lower3[::-1]    
    
    return {
        'data': [
            go.Scatter(
                x = x1,
                y= y1, 
                mode='lines',
                line={
                    'color':line_colors[0],
                    'shape': 'hv'
                },
                name=f'{first_player}'
            ),
            go.Scatter(
                x = x2,
                y= y2,
                mode='lines',
                line={
                    'color':line_colors[1],
                    'shape': 'hv'
                },
                name=f'{second_player}'
            ),
            go.Scatter(
                x = x3,
                y= y3,
                mode='lines',
                line={
                    'color':line_colors[4],
                    'shape': 'hv'                    
                    },
                name=f'Top 200'                
            ),                   
            go.Scatter(
                x=x1rev+x1,
                y=lower1+upper1,
                line={
                    'color':line_colors[0],
                    'shape': 'hv',
                    'dash': 'solid'
                },
                name=f'{first_player} CB',
                visible=False
            ),
            go.Scatter(
                x=x2rev+x2,
                y=lower2+upper2,
                line={
                    'color':line_colors[1],
                    'shape': 'hv',
                    'dash': 'solid'
                },
                name=f'{second_player} CB',
                visible=False
            ),
            go.Scatter(
                x=x3rev+x3,
                y=lower3+upper3,
                line={
                    'color':line_colors[4],
                    'shape': 'hv',
                    'dash': 'solid'
                },
                name='Top 200 CB',
                visible=False
            )
        ],
        'layout': go.Layout(
            title=(
                f'Survival Curve (Kaplan-Meier plot)' 
            ),
            titlefont={
                'color':colors['title']
            },
            xaxis={
                'title':'Runs',
                'showline':True,
                'linewidth':2, 
                'linecolor':colors['text'],
                'showgrid':True,
                'gridwidth':1,
                'gridcolor':colors['text'],
                'range':[0,150]
            },
            yaxis={
                'title':'Survival (%)',
                'showline':True,
                'linewidth':2, 
                'linecolor':colors['text'],
                'showgrid':True,
                'gridwidth':1,
                'gridcolor':colors['text'],
                'range':[0,100],
                'hoverformat':'.2f'
            },
            legend={
                'orientation':'h', 
                'y':1.06,
                'x':0
            },                   
            font={
                'color':colors['text']
            },
            margin=go.layout.Margin(
                l=60,
                r=20,
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
                            args=[{"visible":[True]*3+[False]*3}],
                            label="Point Estimates",
                            method="restyle"
                        ),
                        dict(
                            args=[{"visible": [False]*3+[True]*3}],
                            label="95% Confidence Bands",
                            method="restyle"
                        )                        
                    ]),
                    type = "buttons",
                    direction = "down",                    
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
                x = list(range(10,len(df1))) if length != None else None,
                y= df1[f'rolling{length}'][10:] if length != None else None, 
                mode='lines',
                line={'color':line_colors[0]},
                name=f'ROLL {first_player}'
            ),            
            go.Scatter(
                x = list(range(10,len(df2))) if length != None else None,
                y= df2[f'rolling{length}'][10:] if length != None else None, 
                mode='lines',
                line={'color':line_colors[1]},
                name=f'ROLL {second_player}'
            ),
            go.Scatter(
                x = list(range(10,len(df1))),
                y= df1.Ave[10:],
                mode='lines',
                line={'color':line_colors[2]},
                name=f'OVR {first_player}'
                
            ),
            go.Scatter(
                x = list(range(10,len(df2))),
                y= df2.Ave[10:], 
                mode='lines',
                line={'color':line_colors[3]},
                name=f'OVR {second_player}'
            )
        ],
        'layout': go.Layout(
            title=(
                f'Overall Average and {length} innings Rolling Average' 
                if length != None
                else 'Progression of Overall Average'
            ),
            titlefont={
                'color':colors['title']
            },
            xaxis={
                'title':'Innings',
                'showline':True,
                'linewidth':2, 
                'linecolor':colors['text'],
                'showgrid':True,
                'gridwidth':1,
                'gridcolor':colors['text']
            },
            yaxis={
                'title':'Runs',
                'showline':True,
                'linewidth':2, 
                'linecolor':colors['text'],
                'showgrid':True,
                'gridwidth':1,
                'gridcolor':colors['text']
            },
            legend={
                'orientation':'h', 
                'y':1.09,
                'x':0
            },                   
            font={
                'color':colors['text']
            },
            margin=go.layout.Margin(
                l=60,
                r=20,
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
    dfcopy = df_dis[(df_dis['Date']>=dates[0]) & (df_dis['Date']<=dates[1])]
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
        while len(counts[i])<categories:
            counts[i].append(np.NaN)
    totals =[
        [dfcopy.DisType.value_counts().values.sum()]*categories,
        [df1.DisType.value_counts().values.sum()]*categories,
        [df2.DisType.value_counts().values.sum()]*categories
    ]
    props = np.array(counts)/np.array(totals)    
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
                x=props[:,i],
                name=labels[i],
                orientation='h',
                text=np.array(counts)[:,i],
                hoverinfo='text',
                marker={
                    'color':bar_colors[i],
                }
            )
        )
    return {
        'data': data,
        'layout': go.Layout(
            title=f'Mode of Dismissal ({dates[0]}-{dates[1]})',
            titlefont={
                'color':colors['title']    
            },
            xaxis={
                'title':'Proportion',
                'domain':[0,1]
            },
            font={
                'color':colors['text']
            },   
            barmode='stack',
            margin=go.layout.Margin(
                l=120,
                r=20,
                b=30,
                t=45,
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
    dfcopy = df_main[(df_main['Date']>=dates[0]) & (df_main['Date']<=dates[1])]
    df1 = dfcopy[dfcopy['Name'] == first_player]
    df2 = dfcopy[dfcopy['Name'] == second_player]
    values=[[],[],[]]
    for team in teams:
        dftemp = df1[df1['Opposition']==team]
        values[0].append(np.NaN if dftemp.empty else round(dftemp.Runs.sum()/max(1, dftemp.Dismissed.sum()),2))
        dftemp = df2[df2['Opposition']==team]
        values[1].append(np.NaN if dftemp.empty else round(dftemp.Runs.sum()/max(1, dftemp.Dismissed.sum()),2))
        dftemp = dfcopy[dfcopy['Opposition']==team]
        values[2].append(np.NaN if dftemp.empty else round(dftemp.Runs.sum()/max(1, dftemp.Dismissed.sum()),2))
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
                text=[int(n) if n==n else n for n in values[i]],
                textposition='outside',
                hoverinfo='y+name',
                marker={
                    'color':bar_colors[i],
                }
            )
        )
    return {
        'data': data,
        'layout': go.Layout(
            title=f'Average by Opposition ({dates[0]}-{dates[1]})',
            titlefont={
                'color':colors['title']   
            },
            yaxis={
                'title':'Runs',
                'showgrid':True,
                'gridwidth':1,
                'gridcolor':colors['text']
            },
            font={
                'color':colors['text']
            },
            legend={
                'orientation':'h', 
                'y':1.09,
                'x':0
            },         
            margin=go.layout.Margin(
                l=60,
                r=20,
                b=40,
                t=80,
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
     Input('hazard-smoothing', 'value')])
def update_hazard_line_graph(first_player, second_player, bandwidth):
    df1 = df_haz[df_haz['Name'] == first_player]
    df2 = df_haz[df_haz['Name'] == second_player]
    
    return {
        'data': [
            go.Scatter(
                x=df1.time[:120],
                y=df1[f'{bandwidth}'][:120], 
                mode='lines',
                line={
                    'color':line_colors[0],
                    'shape': 'hv'
                },
                name=f'{first_player}'
            ),
            go.Scatter(
                x=df2.time[:120],
                y=df2[f'{bandwidth}'][:120],
                mode='lines',
                line={
                    'color':line_colors[1],
                    'shape': 'hv'
                },
                name=f'{second_player}'
            ),
            go.Scatter(
                x=df_haz_OVR.time[:120],
                y=df_haz_OVR[f'{bandwidth}'][:120],
                mode='lines',
                line={
                    'color':line_colors[4],
                    'shape': 'hv'                    
                    },
                name=f'Top 200'                
            ),
        ],
        'layout': go.Layout(
            title=(
                f'Estimated Hazard Function' 
            ),
            titlefont={
                'color':colors['title']
            },
            xaxis={
                'title':'Runs',
                'showline':True,
                'linewidth':2, 
                'linecolor':colors['text'],
                'showgrid':True,
                'gridwidth':1,
                'gridcolor':colors['text']
            },
            yaxis={
                'title':'Estimated Hazard Function',
                'showline':True,
                'linewidth':2, 
                'linecolor':colors['text'],
                'showgrid':True,
                'gridwidth':1,
                'gridcolor':colors['text'],
                'hoverformat':'.4f'
            },
            legend={
                'orientation':'h', 
                'y':1.1,
                'x':0
            },                   
            font={
                'color':colors['text']
            },
            margin=go.layout.Margin(
                l=60,
                r=20,
                b=40,
                t=80,
                pad=3
            ),
            plot_bgcolor=colors['paper'],
            paper_bgcolor=colors['paper']
        )
    }

if __name__ == '__main__':
    app.run_server()