# Combines data from the Yahoo CSV and the projection CSV to return a CSV with a lot more information.

import pandas as pd
from fantasy_settings import current_season_id

proj_df = pd.read_csv(f'/Users/andrewderango/Documents/Programming Files/NHL API/Recency Bias/{current_season_id[:4]}-{current_season_id[6:]}_recency_adj_projections.csv')
yahoo_df = pd.read_csv(f'/Users/andrewderango/Documents/Programming Files/NHL API/Recency Bias/yahoo_data_scrape.csv')

proj_df = proj_df.drop(['Unnamed: 0'], axis=1)
yahoo_df = yahoo_df.drop(['Unnamed: 0'], axis=1)

yahoo_pos_list = []
team_list = []
owner_list = []

for index, row in proj_df.iterrows():
    try: 
        yahoo_pos_list.append(yahoo_df.loc[yahoo_df['Player'] == row['Player']]['Yahoo Position'].values[0]) 
        team_list.append(yahoo_df.loc[yahoo_df['Player'] == row['Player']]['Team'].values[0]) 
        owner_list.append(yahoo_df.loc[yahoo_df['Player'] == row['Player']]['Owner'].values[0]) 
    except IndexError: 
        yahoo_pos_list.append('-')
        team_list.append('-')
        owner_list.append('-')

proj_df.insert(loc=proj_df.columns.get_loc('GP'), column='Yahoo Position', value=yahoo_pos_list)
proj_df.insert(loc=proj_df.columns.get_loc('GP'), column='Team', value=team_list)
proj_df.insert(loc=proj_df.columns.get_loc('GP'), column='Owner', value=owner_list)

proj_df = proj_df.sort_values(by=['Weighted Season Average'], ascending=False).reset_index(drop=True)
proj_df.index += 1

print(proj_df)
proj_df.to_csv(f'/Users/andrewderango/Documents/Programming Files/NHL API/Recency Bias/expanded_recency_adj_projections.csv')