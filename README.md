# Recency Bias in the NHL
Quantifying adequate recency bias to predict how a player will perform in their next game using multiple and sigmoidal regression. Most data is scraped from the NHL API, and some from the Yahoo Fantasy Hockey website to allow better compatibility between the projections and the fantasy league.

The best order to execute the files is as follows:
1. fantasy_settings.py
2. fantasy_game_log.py
3. games_ago_csv_prep.py
4. recency_regression_func.py
5. proj_csv_generator.py
6. yahoo_data_scrape.py
7. expanded_projection_csv_generator.py

### Possible Future Directions
1. Goalie projections could be implemented using the same algorithms, but would require training data from the further past.
2. The accuracy of these projections could be evaluated to generate probability distributions of how many points a players will score.
3. Improvement of CSV generation time.
4. Consideration of factors such as shooting percentage, expected goals, and previous season production for better projections.
5. Projecting how a player will perform for the long-term future (i.e. remainder of the season), rather than these short-term projections.
