# dash-cricket-data-construction

 This repository scrapes data from cricinfo then cleans it and extracts features to prepare the data set for use by the dash-cricket dashboard [hosted here](https://burningtin-cricket.herokuapp.com/). The dashboard repository can be found [here](https://github.com/burningtin/dash-cricket).
 
Code from earlier projects was repurposed and made into a pipeline that will output updated data when main.py is run.

## Process:

* HTML extracted from the appropriately filtered cricinfo leaderboard page is parsed to provide a dictionary of cricinfo_id:player_name pairs, which is saved as a json.
* Iterate through the cricinfo_id's in this dictionary to download the innings list table available on each players cricinfo page as a dataframe, these are stored as pkl's as each is downloaded. 

These dataframes are used to do the following for each player individually, and for the 200 players in aggregate:

* Rolling averages, average by opposition, and style of dismissal proportions are calculated.
* Dismissals are viewed as observed events for the purpose of performing survival analysis. An event table is made showing how many innings were ongoing and how many dismissals or censored events (not outs) occurred at each score.
* Survival probabilities for use in a Kaplan-Meier plot are calculated using this table.
* Confidence intervals for these survival probabilities are calculated using bpcpy.py\* 

* These results are combined into dataframes which are saved as csv's, ready for use by the dashboard.


\*bpcp.py is an implementation of the beta product confidence procedure for calculating confidence intervals described [here](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3769999/) made specifically for use in this project. Earlier versions of this repository used the R package [bpcp](https://cran.r-project.org/web/packages/bpcp/bpcp.pdf) to calculate these confidence intervals. 
The confidence intervals output by bpcp.py were confirmed against those output by the R package on this dataset on 20/May/2020.
