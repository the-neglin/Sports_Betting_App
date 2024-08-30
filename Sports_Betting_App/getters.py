import pandas as pd
from sqlalchemy import create_engine
import os
from datetime import datetime, timedelta
import putters


DATABASE_TYPE = os.getenv("DATABASE_TYPE")
DBAPI = os.getenv("DBAPI")
ENDPOINT = os.getenv("ENDPOINT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWD")
PORT = os.getenv("PORT")
DATABASE = os.getenv("DATABASE")

def get_leaderboard():

    print("Getting latest leaderboard...")
    connection_string = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"

    try:
        engine = create_engine(connection_string)
    except Exception as e:
        print(f"Error creating engine: {e}")

    sql_query = """
    SELECT users.name, scores.score 
    FROM theneglin.users 
    LEFT JOIN theneglin.scores 
    ON theneglin.scores.user_id = theneglin.users.id;
    """

    try:
        df = pd.read_sql(sql_query, con=engine)
        df = df.rename(columns={'name': 'Name', 'score': 'Score'})
        print("Successfully retrieved leaderboard!")
    except Exception as e:
        print(f"Error executing query: {e}")
    
    return df

def get_last_score():

    print("Gettings latest score datetime...")
    connection_string = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"

    try:
        engine = create_engine(connection_string)
    except Exception as e:
        print(f"Error creating engine: {e}")

    sql_query = """
    select distinct theneglin.scores.score_date from theneglin.scores;
    """

    df = pd.read_sql(sql_query, con=engine)
    if not df.empty:
        score = df.iloc[0,0].strftime("%m/%d/%Y, %H:%M:%S")
        print("Successfully retrieved latest score datetime!")
        return score
    else:
        return


def get_odds(name, email):
    
    name = name
    email = email
    
    print(f'Getting odds for: name = {name} and email = {email}...')
    connection_string = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"

    try:
        engine = create_engine(connection_string)
    except Exception as e:
        print(f"Error creating engine: {e}")

    sql_query = f"""
    select distinct odds.time, odds.favorite, odds.spread, odds.underdog, odds.over_under, picks.choice_id, picks.dd, picks.over_under_id, picks.user_id, odds.week, odds.game_id from odds
    left join picks on picks.game_id = odds.game_id
    where odds.week = '{get_week()}'
    and picks.user_id = '{get_user_id(name=name, email=email)}';
    """

    odds_df = pd.read_sql(sql_query, con=engine)
    odds_df = odds_df.rename(columns={'time': 'Time', 'favorite': 'Favorite', 'spread': 'Spread', 'underdog': 'Underdog', 'over_under': 'Over/Under',
                                      'choice_id': 'Spread Pick', 'dd': 'Double Down?', 'over_under_id': 'Over/Under Pick'})
    print('Successfully retrieved odds!')
    return odds_df
    


def get_week():
    print("Getting current NFL week...")
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
            return 1

        for week in nfl_weeks:
            if week['Start Date'] <= today_date <= week['End Date']:
                return week['Week']
        return None

    season_start = datetime(2024, 9, 4)
    season_end = datetime(2025, 1, 7)

    nfl_weeks = get_nfl_weeks(season_start, season_end)

    today_date = datetime.now()

    current_week = get_current_week(nfl_weeks, today_date)
    
    print(f"Successfully retrieved NFL week! It is week {current_week}")
    
    return current_week


def get_user_id(name, email):
    
    name = name
    email = email
    connection_string = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"

    try:
        engine = create_engine(connection_string)
    except Exception as e:
        print(f"Error creating engine: {e}")

    sql_query = f"""
    select users.id from users
    where users.name = '{name}'
    and users.email = '{email}';
    """

    user_id = pd.read_sql(sql_query, con=engine)

    if not user_id.empty:
        print("Getting user id...")
        print(user_id.iloc[0, 0])
        # putters.insert_blank_picks(get_game_ids(user_id.iloc[0, 0]))
        print(f"Successfully retrieved user with the id: {user_id.iloc[0, 0]}")
        return user_id.iloc[0, 0]
    else:
        print("User not found. Adding user...")
        user_id = putters.insert_user(name=name, email=email)
        if user_id:
            print(f"User added successfully with ID: {user_id}")
            putters.insert_blank_picks(get_game_ids(user_id))
            return user_id
        else:
            print("Failed to add user.")
            return None

    return

def get_game_ids(user_id):
    
    connection_string = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"

    try:
        engine = create_engine(connection_string)
    except Exception as e:
        print(f"Error creating engine: {e}")

    sql_query = """
    select odds.game_id from odds;
    """

    game_ids_df = pd.read_sql(sql_query, con=engine)
    game_ids_df['user_id'] = user_id
    
    return game_ids_df