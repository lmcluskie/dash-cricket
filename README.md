# dash-cricket

## A dashboard ([hosted here](https://burningtin-cricket.herokuapp.com/)) that provides visual summaries and comparisons of the batting careers of test cricketers. 

Batsmen available are the top 200 players with test match batting average > 35 when sorting by runs scored.

The data_updater folder scrapes data from cricinfo then cleans it and extracts features to prepare the data set for use by the dash-cricket dashboard , which resides in the dashboard folder.
 
Dashboard data is updated when data_updater/updater.py is run.

### Dashboard

### Data preparation process:

* HTML extracted from the appropriately filtered cricinfo leaderboard page is parsed to provide a dictionary of cricinfo_id:player_name pairs, which is saved as a json.
* Cricinfo_id's in this dictionary are iterated through to download the innings list table available on each players cricinfo page as a dataframe, these are stored as pkl's as each is downloaded. 

This data is used to do the following for each player individually, and for the 200 players in aggregate:

* Rolling averages, average by opposition, and style of dismissal proportions are calculated.
* Dismissals are viewed as observed events for the purpose of performing survival analysis. An event table is made showing how many innings were ongoing and how many dismissals or censored events (not outs) occurred at each score.
* From this event table, survival probabilities for use in a Kaplan-Meier plot are extracted, with confidence intervals for these survival probabilities calculated using bpcpy.py\* 

The resulting dataframes are combined and saved as .csv's in the dashboard's data folder, ready for use.

\*bpcp.py is an implementation of the beta product confidence procedure for calculating confidence intervals described [here](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3769999/) made specifically for use in this project. Earlier versions of this repository used the R package [bpcp](https://cran.r-project.org/web/packages/bpcp/bpcp.pdf) to calculate these confidence intervals. 
The confidence intervals output by bpcp.py were confirmed against those output by the R package on this dataset on 20/May/2020.
