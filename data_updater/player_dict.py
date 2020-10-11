"""
Create a json dictionary of player cricinfo ids:names by searching the html source
code of cricinfo leaderboards
"""

import re
import json
import requests


def get_html(style, discipline):
    """Downloads the html source code of the cricinfo leaderboard page with 
    given filters"""
    
    # top 100 odi run scorers with average > 30
    if style == 'odi':
        html = requests.get(
            'http://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;filter=advanced;orderby=runs;qualmin1=30;qualval1=batting_average;size=100;template=results;type=batting'
        ).text
        
    # top 200 test run scorers with average > 35
    else:
        html = requests.get(
            'http://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;filter=advanced;orderby=runs;qualmin1=35;qualval1=batting_average;size=200;template=results;type=batting'
        ).text
    with open(f'data/{discipline}/{style}/html.txt', 'w') as file:
        file.write(html)


def create_player_dict(style, discipline):
    """Creates dict of the names and cricinfo ids found in the html and stores
    this dictionary as a json"""
    get_html(style, discipline)
    path = f'data/{discipline}/{style}/html.txt'
    destination = f'data/{discipline}/{style}/ids_names.json'

    with open(path) as file:
        contents = file.read()
        match_regex = re.compile(r'/content/player/(\d*).html" class="data-link">(.*)</a>')
        ids_names = dict(match_regex.findall(contents))

    with open(destination, 'w') as file:
        json.dump(ids_names, file)

    return ids_names
