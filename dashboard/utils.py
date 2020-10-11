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
    'title': 'Bookman',
    'body': 'Arial'
}


def header():
    return html.Div(get_header())


def get_header():
    head = html.Div(
        [
            html.H1(
                ['Test Match Careers'],
                style={
                    'color': colors['title'],
                    'padding-top': '10px',
                    'fontFamily': fonts['title'],
                    'position': 'relative',
                    'left': '10%',
                    'fontSize': '68px'
                }
            )
        ]
    )
    return head
