import pandas as pd
from sqlalchemy import create_engine
import os
from datetime import datetime, timedelta

DATABASE_TYPE = os.getenv("DATABASE_TYPE")
DBAPI = os.getenv("DBAPI")
ENDPOINT = os.getenv("ENDPOINT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWD")
PORT = os.getenv("PORT")
DATABASE = os.getenv("DATABASE")

def get_leaderboard():

    connection_string = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"

    try:
        engine = create_engine(connection_string)
    except Exception as e:
        print(f"Error creating engine: {e}")

    sql_query = """
    SELECT users.name, score.score_value 
    FROM theneglin.users 
    LEFT JOIN theneglin.score 
    ON theneglin.score.user_id = theneglin.users.id;
    """

    try:
        df = pd.read_sql(sql_query, con=engine)
        df = df.rename(columns={'name': 'Name', 'score_value': 'Score'})
    except Exception as e:
        print(f"Error executing query: {e}")
        
    return df

def get_last_score():

    connection_string = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"

    try:
        engine = create_engine(connection_string)
    except Exception as e:
        print(f"Error creating engine: {e}")

    sql_query = """
    select distinct theneglin.score.score_date from theneglin.score;
    """

    df = pd.read_sql(sql_query, con=engine)
    score = df.iloc[0,0].strftime("%m/%d/%Y, %H:%M:%S")
        
    return score


def get_odds():
    
    connection_string = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"

    try:
        engine = create_engine(connection_string)
    except Exception as e:
        print(f"Error creating engine: {e}")

    sql_query = f"""
    select odds.time, odds.favorite, odds.spread, odds.underdog, odds.over_under, picks.choice_id, picks.dd, picks.over_under_id, picks.user_id, odds.week, odds.game_id from odds
    left join picks on picks.game_id = odds.game_id
    where odds.week = {get_week()};
    """

    odds_df = pd.read_sql(sql_query, con=engine)
    odds_df = odds_df.rename(columns={'time': 'Time', 'favorite': 'Favorite', 'spread': 'Spread', 'underdog': 'Underdog', 'over_under': 'Over/Under',
                                      'choice_id': 'Spread Pick', 'dd': 'Double Down?', 'over_under_id': 'Over/Under Pick'})
    return odds_df
    


def get_week():
    def get_nfl_weeks(start_date, end_date):
        nfl_weeks = []
        current_week_start = start_date
        week_number = 1

        while current_week_start <= end_date:
            week_end = current_week_start + timedelta(days=6)
            if week_end > end_date:
                week_end = end_date
            nfl_weeks.append({
                'Week': week_number,
                'Start Date': current_week_start,
                'End Date': week_end
            })
            current_week_start = week_end + timedelta(days=1)
            week_number += 1

        return nfl_weeks

    def get_current_week(nfl_weeks, today_date):
        if today_date < nfl_weeks[0]['Start Date']:
            return 1  # Default to Week 1 if today is before the season starts

        for week in nfl_weeks:
            if week['Start Date'] <= today_date <= week['End Date']:
                return week['Week']
        return None

    # Define the start and end dates of the NFL season
    season_start = datetime(2024, 9, 4)  # Example start date
    season_end = datetime(2025, 1, 7)    # Example end date

    # Get the list of NFL weeks
    nfl_weeks = get_nfl_weeks(season_start, season_end)

    # Get today's date
    today_date = datetime.now()

    # Determine the current NFL week
    current_week = get_current_week(nfl_weeks, today_date)
    
    return current_week