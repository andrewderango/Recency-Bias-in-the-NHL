# Contains all of the data necessary to calculate fantasy points, the season from which the data is trained from, and the current season.
# Does not execute any functions, simply a storage of variables used in all files.

scoring = {
    'Goals': 20,
    'Assists': 12,
    '+/-': 2,
    'PIM': 1.5,
    'PPG': 4,
    'PPA': 2.4,
    'SHG': 10,
    'SHA': 6,
    'GWG': 1.5,
    'Shots': 2.5,
    'FOW': 0.2,
    'FOL': -0.2,
    'Hits': 2.2,
    'Blocks': 3,

    'Games Started': 4,
    'Wins': 10,
    'Losses': -8,
    'Goals Against': -6,
    'Saves': 1.6,
    'Shutouts': 30
}

season_id = '20212022'
current_season_id = '20222023'