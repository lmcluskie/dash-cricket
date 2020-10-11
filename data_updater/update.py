"""Create csv's needed for https://burningtin-cricket.herokuapp.com/ cricket dashboard"""

import pandas as pd
import datetime
import pathlib
import json
from player_dict import create_player_dict
from player import Batsman


pd.options.mode.chained_assignment = None
DATA_PATH = pathlib.Path(__file__).parent.joinpath("../dash-cricket/data").resolve()


def make_app_data(i_n, download=False):
    """create csv's and send them to app data folder"""
    
    innings, summary, survival, hazard = [], [], [], []    
    for i, n in i_n.items():
        player = Batsman(n, i, 'test')
        innings.append(player.get_innings_df(download))
        summary.append(player.get_summary_df())
        survival.append(player.get_survival_df())
        hazard.append(player.get_hazard_df())    
    innings_overall = pd.concat(innings)
    summary_overall = pd.concat(summary)
    innings_overall.to_csv('data/batting/test/innings/overall.csv')
    summary_overall.to_csv('data/batting/test/summary/overall.csv')
    
    player = Batsman('overall', 1, 'test')
    survival.append(player.get_survival_df())
    hazard.append(player.get_hazard_df())
    
    survival_overall = pd.concat(survival)
    hazard_overall = pd.concat(hazard)
    
    innings_overall.to_csv(DATA_PATH.joinpath('innings.csv'))
    summary_overall.to_csv(DATA_PATH.joinpath('summary.csv'))
    survival_overall.to_csv(DATA_PATH.joinpath('survival.csv'))
    hazard_overall.to_csv(DATA_PATH.joinpath('hazard.csv'))


def update_data(download=False):
    """run this function with download=True to update data
    running with download=False will recreate output csv's with the existing data"""
    d = 'batting'
    s = 'test'
    with open('data/batting/test/ids_names.json') as file:
        i_n = json.load(file)
    create_player_dict(s, d)
    make_app_data(i_n, download)
    

if __name__ == '__main__':
    update_data()
    last_updated = open(DATA_PATH.joinpath('last_updated.txt'), 'w') 
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    last_updated.write(date)
    last_updated.close()
    