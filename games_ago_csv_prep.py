# Reads the CSV generated in fantasy_game_log.py that shows how many points a player scored in each game they played, in order.
# Breaks the data up to make a row for each game they played that shows how they performed in their games before that.
# Returns a CSV with general information about the player, the points they scored in that game, and how many points they scored in each game that season.
# Depending on the season, the returned CSV may have more than 50,000 rows. The CSV may take ~10 minutes to generate.

import pandas as pd
from fantasy_settings import season_id
import time

df = pd.read_csv(f'{season_id[:4]}-{season_id[6:]}_fantasy_game_log.csv').drop(['Unnamed: 0'], axis=1)
column_dict_rename = {}
for column_header in df.columns[1:]:
    try:
        column_dict_rename[column_header] = int(column_header)
    except ValueError:
        pass
df.rename(columns=column_dict_rename, inplace=True)
df = df.reset_index(drop=True)

column_list = ['Player', 'Position', 'Game #', 'Actual Points'] + [_ for _ in range(1,82)]
games_ago_df = pd.DataFrame(columns=column_list)
x = []
y = []

start_time = sub_csv_end_time = time.time()
print(f'The CSV generation process typically takes around 10 minutes')

for game_iter in range(82, 10, -1):
    try:
        for index, row in df.dropna(subset=[game_iter]).iterrows():
            games_ago_df.loc[len(games_ago_df)] = [row['Player'], row['Position'], game_iter] + row[game_iter-(df.columns.values.tolist()[-1]+1):1:-1].tolist() + [None for i in range(82-game_iter)]
    except KeyError: pass

    print(f'Sub-CSV for {game_iter} games has been added.\tTotal time elapsed: {round(time.time() - start_time,2)} seconds.\tSub-CSV time: {round(time.time() - sub_csv_end_time,2)} seconds.')
    sub_csv_end_time = time.time()

print(games_ago_df)
games_ago_df.to_csv(f'{season_id[:4]}-{season_id[6:]}_recency_bias.csv')
