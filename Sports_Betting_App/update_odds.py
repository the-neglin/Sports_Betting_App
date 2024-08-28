import requests
import pandas as pd
from datetime import datetime
import pytz
import os
from sqlalchemy import create_engine, text


def fetch_odds():
    api_key = os.getenv("ODDS_API")
    sport = 'americanfootball_nfl'
    regions = 'us'
    markets = 'spreads'+','+'totals'
    start_date = '2024-09-01T00:00:00Z'
    end_date = '2024-09-07T23:59:59Z'
    odds_url = f'https://api.the-odds-api.com/v4/sports/{sport}/odds/'
    params = {
        'apiKey': api_key,
        'regions': regions,
        'markets': markets,
        'dateFormat': 'iso',
        'startDate': start_date,
        'endDate': end_date
    }
    response = requests.get(odds_url, params=params)
    data = response.json()
    
    return data

def process_odds(data):
    week1_start_date = datetime(2024, 9, 5).replace(tzinfo=pytz.utc)
    central_tz = pytz.timezone('America/Chicago')
    games_list = []

    def calculate_week(game_date):
        delta = (game_date - week1_start_date).days
        return (delta // 7) + 1

    for game in data:
        game_id = game['id']
        game_time_utc = game['commence_time']
        game_time = datetime.fromisoformat(game_time_utc[:-1]).replace(tzinfo=pytz.utc)
        game_time_central = game_time.astimezone(central_tz)
        home_team = game['home_team']
        away_team = game['away_team']
        favorite = None
        underdog = None
        highest_negative_spread = None
        most_recent_update_time = None
        over_under = None

        for bookmaker in game['bookmakers']:
            for market in bookmaker['markets']:
                if market['key'] == 'spreads':
                    outcomes = market['outcomes']
                    if len(outcomes) == 2:
                        team1 = outcomes[0]
                        team2 = outcomes[1]
                        update_time = datetime.now()
                        if most_recent_update_time is None or update_time > most_recent_update_time:
                            most_recent_update_time = update_time
                            if team1['point'] < team2['point']:
                                favorite = team1['name']
                                underdog = team2['name']
                                highest_negative_spread = team1['point']
                            else:
                                favorite = team2['name']
                                underdog = team1['name']
                                highest_negative_spread = team2['point']
                            if favorite == home_team:
                                favorite = f"at {home_team}"
                            elif underdog == home_team:
                                underdog = f"at {home_team}"
                                # Handling over/under
                elif market['key'] == 'totals':  # 'totals' usually represents the over/under market
                    outcomes = market['outcomes']
                    if len(outcomes) == 2:
                        over_under = f"+/- {outcomes[0]['point']}"

        week = calculate_week(game_time)
        formatted_time = game_time_central.strftime('%A %I:%M %p')
        games_list.append({
            'game_id': game_id,
            'time': formatted_time,
            'favorite': favorite,
            'spread': highest_negative_spread,
            'underdog': underdog,
            'week': week,
            'over_under': over_under
        })

    return games_list

def save_odds(data):
        DATABASE_TYPE = os.getenv("DATABASE_TYPE")
        DBAPI = os.getenv("DBAPI")
        ENDPOINT = os.getenv("ENDPOINT")
        USER = os.getenv("USER")
        PASSWORD = os.getenv("PASSWD")
        PORT = os.getenv("PORT")
        DATABASE = os.getenv("DATABASE")


        connection_string = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"

        # Create SQLAlchemy engine
        engine = create_engine(connection_string)

        df = pd.DataFrame(data)
        df.to_sql('odds', con=engine, if_exists='replace', index=False)
        
        with engine.connect() as connection:
            connection.execute(text("""
                ALTER TABLE odds 
                ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST;
            """))

def fetch_scores():
    api_key = os.getenv("ODDS_API")  # Update with your scores API key
    sport = 'americanfootball_nfl'
    days_from = '1'
    scores_url = f'https://api.the-odds-api.com/v4/sports/{sport}/scores/'
    params = {
        'daysFrom': days_from,
        'apiKey': api_key
    }
    response = requests.get(scores_url, params=params)
    data = response.json()

    return data


def process_scores(scores_data, processed_odds):
    # Convert processed_odds to a dictionary for easy lookup
    odds_dict = {game['game_id']: game for game in processed_odds}
    
    # Create a DataFrame from scores_data
    df = pd.DataFrame(scores_data)
    
    # Filter completed games
    completed_games = df[df['completed'] == True]

    results = []
    for _, row in completed_games.iterrows():
        game_id = row['id']
        scores = {score['name']: int(score['score']) for score in row['scores']}
        home_team_score = scores.get(row['home_team'], 0)
        away_team_score = scores.get(row['away_team'], 0)
        
        # Look up odds for this game
        game_odds = odds_dict.get(game_id, {})
        spread = game_odds.get('spread', None)
        favorite = game_odds.get('favorite', None)
        underdog = game_odds.get('underdog', None)
        over_under = game_odds.get('over_under', None)

        # Determine if the spread was covered
        spread_win = None
        if spread is not None and favorite and underdog:
            spread_value = float(spread)
            if favorite in row['home_team']:
                # Favorite is home team
                spread_win = 1 if home_team_score - away_team_score >= spread_value else 2
            elif favorite in row['away_team']:
                # Favorite is away team
                spread_win = 1 if away_team_score - home_team_score >= spread_value else 2

        # Determine if the over/under was covered
        over_under_win = None
        if over_under is not None:
            total_score = home_team_score + away_team_score
            over_under_value = float(over_under.split(' ')[-1])
            over_under_win = 1 if total_score > over_under_value else 2
        
        # Append result
        results.append({
            'game_id': game_id,
            'home_score': home_team_score,
            'away_score': away_team_score,
            'spread_win': spread_win,
            'over_under_win': over_under_win
        })

    # Convert results to DataFrame
    score_results = pd.DataFrame(results)
    
    # Print the results DataFrame
    return score_results

def save_scores(processed_scores):
    DATABASE_TYPE = os.getenv("DATABASE_TYPE")
    DBAPI = os.getenv("DBAPI")
    ENDPOINT = os.getenv("ENDPOINT")
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWD")
    PORT = os.getenv("PORT")
    DATABASE = os.getenv("DATABASE")


    connection_string = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"

    # Create SQLAlchemy engine
    engine = create_engine(connection_string)

    df = pd.DataFrame(processed_scores)
    df.to_sql('game_results', con=engine, if_exists='replace', index=False)
    
    with engine.connect() as connection:
        connection.execute(text("""
            ALTER TABLE game_results 
            ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST;
        """))

def main():
    odds_data = fetch_odds()
    processed_odds = process_odds(odds_data)
    save_odds(processed_odds)
    scores_data = fetch_scores()
    processed_scores = process_scores(scores_data, processed_odds)
    save_scores(processed_scores)
if __name__ == '__main__':
    main()