"""Download, clean and perform calculations on test match batting data from 
cricinfo statsguru for a given player. Provide the players name as seen on 
their cricinfo profile, and the id found in the url of their profile page"""

import pandas as pd
import numpy as np
from survival import event_table, smooth_hazard
from bpcpy import confidence_intervals


class Batsman:
    def __init__(self, name, player_id, match):
        """The batsman's name, cricinfo id, match format are assigned for use."""
        
        self.name = name
        self.player_id = player_id
        self.match = match
        

    def download_data(self):
        """Download test match innings table from the players cricinfo batting summary page"""
        
        if self.match == 'odi':
            df = pd.read_html(f'http://stats.espncricinfo.com/ci/engine/player/{self.player_id}.html?class=2;template=results;type=batting;view=innings')
        else:
            df = pd.read_html(f'http://stats.espncricinfo.com/ci/engine/player/{self.player_id}.html?class=1;template=results;type=batting;view=innings')
        summary = df[2]
        summary['Name'] = self.name
        summary = summary[['Name', 'Span', 'Mat', 'Inns', 'Runs', 'HS', 'Ave', '50', '100']]
        summary.to_pickle(f'data/batting/{self.match}/summary/{self.name}.pkl')
        df = df[3]
        df.to_pickle(f'data/batting/{self.match}/original/{self.name}.pkl')            
        return df

    
    def edit_data(self, df):
        """Clean data and extract desired features."""
        
        #removing unwanted cols and preparing data
        df = df[['Runs', 'BF', 'Pos', 'Dismissal', 'Opposition', 'Start Date']]
        df['Name'] = self.name
        df.rename(columns={'Start Date':'Date'}, inplace=True)
        df['Date'] = df['Date'].apply(lambda x: x[-4:])
        df['Opposition'] = df['Opposition'].apply(lambda x: x[2:])
        df['Out'] = df['Dismissal'].isin(['lbw', 'caught', 'run out', 'bowled',
                                       'stumped', 'hit wicket', 'obstruct field',
                                       'handled ball', 'retired out']) * 1
        df = df.replace({'Runs': ['absent', '-', 'DNB', 'TDNB', 'sub']}, np.NaN)
        df.dropna(inplace=True)
        df = df.reset_index()
        del df['index']
        df = df.replace({'BF': ['-']}, 0)
        df['Runs'] = df['Runs'].str.replace(r"*",'')
        df[['Runs', 'BF']] = df[['Runs', 'BF']].apply(pd.to_numeric)
        df = df.replace({'Dismissal': 'retired notout'}, 'not out')
        df = df.replace({'Dismissal': ['handled ball', 'hit wicket', 'obstruct field', 'retired out']}, 'other')
        
        #calculating and adding cols for career average/rolling averages
        df['RunTally'] = df.Runs.cumsum()
        df['DisTally'] = df.Out.cumsum()
        df['Ave'] = round(df['RunTally']/df['DisTally'], 2)
        lengths = [10, 20, 30, 40, 50, 70, 100]
        for length in lengths:
            df[f'rolling{length}'] = round((df['Runs'].rolling(window=length, center=False).sum() /
                                            df['Out'].rolling(window=length, center=False).sum()), 2)
        df = df[['Name', 'Runs', 'Dismissal', 'Pos', 'Opposition', 'Ave', 'RunTally', 
             'DisTally', 'Date', 'Out', 'rolling10', 'rolling20', 'rolling30',
             'rolling40', 'rolling50', 'rolling70', 'rolling100']]
        return df
    
    
    def get_summary_df(self):
        df = pd.read_pickle(f'data/batting/{self.match}/summary/{self.name}.pkl')
        return df
    
    
    def get_innings_df(self, download=False):
        """Get the cleaned innings dataframe, downloading data if wanted or needed"""
        if download:
            df = self.download_data()
        else:
            try:
                df = pd.read_pickle(f'data/batting/{self.match}/original/{self.name}.pkl')
            except FileNotFoundError:
                df = self.download_data()
        df = self.edit_data(df)
        df.to_csv(f'data/batting/{self.match}/innings/{self.name}.csv')
        return df
    
        
    def get_survival_df(self):
        """Create Survival Curve statistics"""
        events = event_table(self.name, self.match)
        events.drop(events.index[0], inplace=True)
        df = confidence_intervals(events)
        df['Name'] = self.name
        df.to_csv(f'data/batting/{self.match}/KM/{self.name}.csv')
        return df


    def get_hazard_df(self):
        """Calculate hazard statistics and smooth for plotting"""
        events = event_table(self.name, self.match)
        df = smooth_hazard(events, self.name)
        df.to_csv(f'data/batting/test/hazard/{self.name}.csv')
        return df