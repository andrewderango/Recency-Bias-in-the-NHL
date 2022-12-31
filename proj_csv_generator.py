# Uses the regression data derived in recency_regression_func to prepare a CSV with relevant player information and their projections.

import pandas as pd
import numpy as np
from recency_regression_func import perform_regression
from fantasy_settings import current_season_id

df = pd.read_csv(f'{current_season_id[:4]}-{current_season_id[6:]}_recency_bias.csv').drop(['Unnamed: 0'], axis=1)
column_dict_rename = {}
for column_header in df.columns[1:]:
    try:
        column_dict_rename[column_header] = int(column_header) + 1
    except ValueError:
        pass

column_dict_rename['Actual Points'] = 1
df.rename(columns=column_dict_rename, inplace=True)
df = df.drop_duplicates(subset='Player').reset_index(drop=True).drop(columns=['Game #'])

df.insert(loc=df.columns.get_loc(1), column='GP', value=df[[_ for _ in range(1,df.columns[-1]+1)]].count(axis=1))
df.insert(loc=df.columns.get_loc(1), column='Season Average', value=df[[_ for _ in range(1,df.columns[-1]+1)]].sum(axis=1) / df[[_ for _ in range(1,df.columns[-1]+1)]].count(axis=1))
df.insert(loc=df.columns.get_loc(1), column='Weighted Season Average', value=None)
df.insert(loc=df.columns.get_loc(1), column='Last 10 Games Average', value=df[[_ for _ in range(1,11)]].sum(axis=1)/df[[_ for _ in range(1,11)]].count(axis=1))
df.insert(loc=df.columns.get_loc(1), column='Last 20 Games Average', value=df[[_ for _ in range(1,21)]].sum(axis=1)/df[[_ for _ in range(1,21)]].count(axis=1))
df.insert(loc=df.columns.get_loc(1), column='Last 35 Games Average', value=df[[_ for _ in range(1,36)]].sum(axis=1)/df[[_ for _ in range(1,36)]].count(axis=1))

a, b, c, _, _ = perform_regression()
w_avg_list = []
for index, row in df.iterrows():
    weighted_average = used_weightings = 0
    for game in range(1,row['GP']+1):
        weighted_average += row[game] * 1/(a+np.exp((game-b)/c))
        used_weightings += 1/(a+np.exp((game-b)/c))
    w_avg_list.append(weighted_average/used_weightings)
df['Weighted Season Average'] = w_avg_list

df['Season Average'] = df['Season Average'].apply(lambda float: f'{float:.2f}')
df['Weighted Season Average'] = df['Weighted Season Average'].apply(lambda float: f'{float:.2f}')
df['Last 10 Games Average'] = df['Last 10 Games Average'].apply(lambda float: f'{float:.2f}')
df['Last 20 Games Average'] = df['Last 20 Games Average'].apply(lambda float: f'{float:.2f}')
df['Last 35 Games Average'] = df['Last 35 Games Average'].apply(lambda float: f'{float:.2f}')

print(df)
df.to_csv(f'{current_season_id[:4]}-{current_season_id[6:]}_recency_adj_projections.csv')
