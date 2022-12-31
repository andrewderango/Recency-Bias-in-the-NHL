# This file performs the regression. The independent variable is the points scored in the game in question. The dependent variables are the points score in the games prior to the game in question. This was done using multiple linear regression (MLR).
# Next, due to the inevitable noise in these results, a sigmoidal function was regressed to fit the MLR datapoints from each prior game.
# Uncommented the bottom two lines displays a graph that demonstrates this and helps vizualize the effect of recent performance on short-term future performance.

import pandas as pd
from sklearn import linear_model
from fantasy_settings import season_id
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

def perform_regression():
    games_ago_df = pd.read_csv(f'/Users/andrewderango/Documents/Programming Files/NHL API/Recency Bias/{season_id[:4]}-{season_id[6:]}_recency_bias.csv').drop(['Unnamed: 0'], axis=1)
    column_dict_rename = {}
    for column_header in games_ago_df.columns[1:]:
        try:
            column_dict_rename[column_header] = int(column_header)
        except ValueError:
            pass
    games_ago_df.rename(columns=column_dict_rename, inplace=True)
    games_ago_df = games_ago_df.reset_index(drop=True)

    games_ago_counted = 74 #Must be <= 81. 74 was selected because there is insufficient data beyond 75 GP to make conclusions (less players play 75+ games).
    # print(games_ago_df.iloc[:, :games_ago_counted+4]) #df.iloc[row_start:row_end , col_start:col_end]

    games_ago_weight_dict = {}
    for games_ago in range(1,games_ago_counted+1):
        regression_df = games_ago_df[['Actual Points', games_ago]].dropna()
        X = regression_df[[games_ago]] # Independent variable
        y = regression_df['Actual Points'] # Dependent variable

        regression = linear_model.LinearRegression()
        regression.fit(X, y)

        games_ago_weight_dict[games_ago] = regression.coef_[0]
        # games_ago_weight_dict[games_ago] = regression.score(X, y) #R² of points n games ago and actual points

    # print(f'Games Ago\tWeight')
    # for key, value in games_ago_weight_dict.items():
    #     print(f'{key}\t\t{value: .3f}')

    xpoints = list(games_ago_weight_dict.keys())
    ypoints = list(games_ago_weight_dict.values())

    parameters, covariates = curve_fit(lambda t, a, b, c: 1/(a+np.exp((t-b)/c)), xpoints, ypoints)
    a, b, c = parameters[0], parameters[1], parameters[2]

    return a, b, c, xpoints, ypoints

def display_regression(a, b, c, xpoints, ypoints):
    x_fitted = np.linspace(np.min(xpoints), np.max(xpoints), 100)
    y_fitted = 1/(a+np.exp((x_fitted-b)/c))

    poly_reg_1deg = np.poly1d(np.polyfit(xpoints, ypoints, 1))
    poly_reg_2deg = np.poly1d(np.polyfit(xpoints, ypoints, 2))
    poly_reg_3deg = np.poly1d(np.polyfit(xpoints, ypoints, 3))

    r, p = pearsonr(xpoints, ypoints)

    if p > 0.1: significance = 'No' 
    elif p > 0.05: significance = 'Weak'
    elif p > 0.05: significance = 'Weak'
    elif p > 0.01: significance = 'Moderate'
    elif p > 0.005: significance = 'Good.'
    elif p > 0.001: significance = 'Strong evidence'
    else: significance = 'Very strong'

    print(f'\nPearson Correlation of Independent and Dependent Variables: {r:.3f}')
    print(f'Significance of Correlation (p-value): {p:.5f}\t({significance} evidence against the null hypothesis)')
    print(f'Factor of Proration: {1/sum(ypoints):.3f}')
    print(f'-----')
    print(f'R² of Regressed 3-Parameter Sigmoid Function (Black): {r2_score(ypoints, 1/(a+np.exp((xpoints-b)/c))):.3f} | 1/({a:.3f}+exp((x-{b:.3f})/{c:.3f}))')
    print(f'R² of Regressed 1 Degree Polynomial Function (Blue):  {r2_score(ypoints, poly_reg_1deg(xpoints)):.3f} | {poly_reg_1deg.c[0]:.3f}x + {poly_reg_1deg.c[1]:.3f}')
    print(f'R² of Regressed 2 Degree Polynomial Function (Green): {r2_score(ypoints, poly_reg_2deg(xpoints)):.3f} | {poly_reg_2deg.c[0]:.3f}x² + {poly_reg_2deg.c[1]:.3f}x + {poly_reg_2deg.c[2]:.3f}')
    print(f'R² of Regressed 3 Degree Polynomial Function (Red):   {r2_score(ypoints, poly_reg_3deg(xpoints)):.3f} | {poly_reg_3deg.c[0]:.3f}x³ + {poly_reg_3deg.c[1]:.3f}x² + {poly_reg_3deg.c[2]:.3f}x + {poly_reg_3deg.c[3]:.3f}')

    # plt.annotate(f'R² = {r2_score(ypoints, 1/(a+np.exp((xpoints-b)/c))):.3f}', (0.8, (max(ypoints)-min(ypoints))*0.05+min(ypoints)))
    plt.plot(xpoints, ypoints, 'o', color='grey')
    plt.plot(x_fitted, poly_reg_1deg(x_fitted), color='blue', alpha=0.3, label=f'1st Degree Polynomial (R² = {r2_score(ypoints, poly_reg_1deg(xpoints)):.3f})')
    plt.plot(x_fitted, poly_reg_2deg(x_fitted), color='green', alpha=0.3, label=f'2nd Degree Polynomial (R² = {r2_score(ypoints, poly_reg_2deg(xpoints)):.3f})')
    plt.plot(x_fitted, poly_reg_3deg(x_fitted), color='red', alpha=0.3, label=f'3rd Degree Polynomial (R² = {r2_score(ypoints, poly_reg_3deg(xpoints)):.3f})')
    plt.plot(x_fitted, y_fitted, color='black', alpha=1, label=f'Sigmoid (R² = {r2_score(ypoints, 1/(a+np.exp((xpoints-b)/c))):.3f})')
    plt.legend()
    plt.title('Recency Regression')
    plt.xlabel('Games Ago')
    plt.ylabel('Weight')
    plt.show()

### Uncomment these to view the regression graphs and analysis.
# a, b, c, xpoints, ypoints = perform_regression()
# display_regression(a, b, c, xpoints, ypoints)