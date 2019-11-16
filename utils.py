import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

colors = {
    'background': '#1D313F',
    'paper': '#192A35',
    'text': '#D6D6D6',
    'title': '#FFFFFF',
    'cells': '#3D4770'
}

fonts = {
    'title': 'Bodoni',
    'body': 'Garamond'
}


def header():
    return html.Div([get_header(), get_menu()])


def get_header():
    head = html.Div(
        [
            html.H1(
                ['Explore Cricket Stats'],
                style={
                    'textAlign': 'center',
                    'color': colors['title'],
                    'padding-top': '20px',
                    'fontFamily': fonts['title']
                }
            )
        ]
    )
    return head


def get_menu():
    menu = html.Div([
            dcc.Link(
                html.Button(
                    "Comparison Graphs",
                    style={
                        'color': colors['text'],
                        'textDecoration': 'none'
                    }
                ),
                href="/BatsmenGraphs",
                className="tab"
            ),
            dcc.Link(
                html.Button(
                    "Full Tables",
                    style={
                        'color': colors['text'],
                        'textDecoration': 'none'
                    }
                ),
                href="/BatsmenSummary",
                className="tab first"
            )
        ],
        style={
            'textAlign': 'center'
        },
        className="row all-tabs",
    )
    return menu