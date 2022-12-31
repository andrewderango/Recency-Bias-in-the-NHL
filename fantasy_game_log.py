# Scrapes data from the NHL's API to output a CSV file that shows how many fantasy points a player got in each game they played, in order.
# Will not include players that are not currently on an NHL roster.

import urllib.request, json
import pandas as pd
from fantasy_settings import scoring, season_id

class Player():
    def __init__(self, name, id, position, games):
        self.name = name
        self.id = id
        self.position = position
        self.games = games
    
    def add_game(self, game):
        self.games.insert(0, game)

    def introduce(self):
        print(f'Name: {self.name}\nID: {self.id}\nPosition: {self.position}\nGames Played: {len(self.games)}')

class Game():
    def __init__(self, id, team, opp_team, date, is_home, win, toi, goals, assists, points, shots, hits, blocks, pim, plus_minus, ppg, ppp, shg, shp, gwg):
        self.id = id
        self.team = team
        self.opp_team = opp_team
        self.date = date
        self.is_home = is_home
        self.win = win
        self.toi = toi
        self.goals = goals
        self.assists = assists
        self.points = points
        self.shots = shots
        self.hits = hits
        self.blocks = blocks
        self.pim = pim
        self.plus_minus = plus_minus
        self.ppg = ppg
        self.ppp = ppp
        self.shg = shg
        self.shp = shp
        self.gwg = gwg

    def calc_fantasy_points(self):
        return round(game.goals*scoring['Goals'] + game.assists*scoring['Assists'] + game.plus_minus*scoring['+/-'] + game.pim*scoring['PIM'] + game.ppg*scoring['PPG'] + (game.ppp-game.ppg)*scoring['PPA'] + game.shg*scoring['SHG'] + (game.shp-game.shg)*scoring['SHA'] + game.gwg*scoring['GWG'] + game.shots*scoring['Shots'] + game.hits*scoring['Hits'] + game.blocks*scoring['Blocks'],1)

skater_list = []

with urllib.request.urlopen("https://statsapi.web.nhl.com/api/v1/teams") as url:
    teams = json.load(url)['teams']

for team in teams:
    try:
        with urllib.request.urlopen(f"https://statsapi.web.nhl.com/api/v1/teams/{team['id']}?expand=team.roster&season={season_id}") as url:
            roster = json.load(url)['teams'][0]['roster']['roster']

        for player in roster:
            if player['position']['abbreviation'] != 'G':
                current_player = Player(player['person']['fullName'], player['person']['id'], player['position']['abbreviation'], [])
                skater_list.append(current_player)
                print(f"{player['person']['fullName']} ({player['position']['abbreviation']})")

                with urllib.request.urlopen(f"https://statsapi.web.nhl.com/api/v1/people/{player['person']['id']}/stats?stats=gameLog&season={season_id}") as url:
                    game_log = json.load(url)['stats'][0]['splits']

                for game in game_log:
                    current_player.add_game(Game(game['game']['gamePk'], game['team']['name'], game['opponent']['name'], game['date'], game['isHome'], game['isWin'], game['stat']['timeOnIce'], game['stat']['goals'], game['stat']['assists'], game['stat']['points'], game['stat']['shots'], game['stat']['hits'], game['stat']['blocked'], game['stat']['pim'], game['stat']['plusMinus'], game['stat']['powerPlayGoals'], game['stat']['powerPlayPoints'], game['stat']['shortHandedGoals'], game['stat']['shortHandedPoints'], game['stat']['gameWinningGoals']))
                    # print(f"{player['person']['fullName']} ({team['abbreviation']}): {game['game']['gamePk']}")
    except urllib.error.HTTPError:
        pass

# for player in skater_list:
#     player.introduce()
#     print()

skater_list = list(dict.fromkeys(skater_list)) # Removes duplicates
df_rows = []

for player in skater_list:
    row_list = {'Player': player.name, 'Position': player.position}
    for game in player.games:
        row_list[player.games.index(game)+1] = game.calc_fantasy_points()
    df_rows.append(row_list)

print()

df = pd.DataFrame(df_rows)
df.to_csv(f'{season_id[:4]}-{season_id[6:]}_fantasy_game_log.csv')
