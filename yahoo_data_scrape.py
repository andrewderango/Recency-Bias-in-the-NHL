# Scrapes player data from the Yahoo fantasy website.
# This file is not necessary to make the projections, but it allows the resultant CSV to contain data about which team owns each player so that filters may be applied.
# The four-digit league ID must be entered.

import requests
from bs4 import BeautifulSoup
import pandas as pd

def retrieve_csv(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    table1 = soup.find('table', {'class':'Table Ta-start Fz-xs Table-mid Table-px-xs Table-interactive'})

    headers = []
    for i in table1.find_all('th'):
        title = i.text
        headers.append(title)

    subdf = pd.DataFrame(columns = headers)

    for j in table1.find_all('tr'):
        row_data = j.find_all('td')
        row = [i.text for i in row_data] + [None for i in range(len(headers) - len([i.text for i in row_data]))]
        subdf.loc[len(subdf)] = row

    subdf = subdf.iloc[2: , 1:]
    subdf.columns = [_ for _ in range(len(subdf.columns))]

    name_row, team_row, pos_row = [], [], []

    for index, row in subdf.iterrows():
        name_row.append(row[0][2:][row[0][2:].index('\n')+1:][:row[0][2:][row[0][2:].index('\n')+1:].index('- ')-4].strip())
        team_row.append(row[0][row[0].index((row[0][2:][row[0][2:].index('\n')+1:][:row[0][2:][row[0][2:].index('\n')+1:].index('- ')-4].strip()))+len(row[0][2:][row[0][2:].index('\n')+1:][:row[0][2:][row[0][2:].index('\n')+1:].index('- ')-4].strip())+1:row[0].index('- ')].strip())
        pos_row.append(row[0][2:][row[0][2:].index('\n')+1:][row[0][2:][row[0][2:].index('\n')+1:].index('- ')+2:][:row[0][2:][row[0][2:].index('\n')+1:][row[0][2:][row[0][2:].index('\n')+1:].index('- ')+2:].index('\n')-1].strip())
        # print('Rest:', row[0][2:][row[0][2:].index('\n')+1:].replace('\n', '')[row[0][2:][row[0][2:].index('\n')+1:].replace('\n', '').index('- ')+len(row[0][2:][row[0][2:].index('\n')+1:][row[0][2:][row[0][2:].index('\n')+1:].index('- ')+2:][:row[0][2:][row[0][2:].index('\n')+1:][row[0][2:][row[0][2:].index('\n')+1:].index('- ')+2:].index('\n')-1].strip())+3:])
    
    subdf.iloc[:, 0] = name_row
    subdf.iloc[:, 1] = team_row
    subdf.iloc[:, 2] = pos_row

    subdf.columns = ['Player', 'Team', 'Yahoo Position', 'Owner', 'GP', 'Fantasy Points', 'Pre-Season', 'Current', '%Rostered', 'ATOI', 'G', 'A', '+/-', 'PIM', 'PPG', 'PPA', 'SHG', 'SHA', 'GWG', 'SOG', 'FW', 'FL', 'HIT', 'BLK'] + [None for i in range(len(subdf.columns)-24)]
    subdf = subdf.loc[: , :'BLK'].reset_index(drop=True)

    return subdf

df = pd.DataFrame() #Initialization of dataframe
players_wanted = 1000
league_id = XXXX #INSERT LEAGUE ID HERE

for i in range(0,players_wanted,25):
    df = pd.concat([df, retrieve_csv(f'https://hockey.fantasysports.yahoo.com/hockey/{league_id}/players?status=ALL&pos=P&cut_type=33&stat1=S_S_2022&myteam=1&sort=PTS&sdir=1&count={i}')])
    print(f'{i+25} players scraped')

df = df.reset_index(drop=True)
df.index += 1
df.to_csv(f'yahoo_data_scrape.csv')
