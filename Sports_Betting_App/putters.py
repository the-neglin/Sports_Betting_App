from sqlalchemy import create_engine, insert, Table, MetaData
from sqlalchemy.exc import SQLAlchemyError
import os

DATABASE_TYPE = os.getenv("DATABASE_TYPE")
DBAPI = os.getenv("DBAPI")
ENDPOINT = os.getenv("ENDPOINT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWD")
PORT = os.getenv("PORT")
DATABASE = os.getenv("DATABASE")



def insert_user(name, email):
    connection_string = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"

    try:
        engine = create_engine(connection_string)

        with engine.connect() as connection:
            metadata = MetaData()

            users_table = Table('users', metadata, autoload_with=engine)
            insert_query = insert(users_table).values(email=f"'{email}'", name=f"'{name}'")
            compiled = insert_query.compile()  # noqa: F841
            result = connection.execute(insert_query)
            connection.commit()
            
            user_id = result.inserted_primary_key[0]
            return user_id

    except SQLAlchemyError as e:
        print(f"Error interacting with the database: {e}")
        return None
    
def insert_blank_picks(game_df):
    connection_string = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"

    try:
        engine = create_engine(connection_string)

        with engine.connect() as connection:
            metadata = MetaData()
            picks_table = Table('picks', metadata, autoload_with=engine)
            
            data_to_insert = game_df.to_dict(orient='records')

            insert_query = picks_table.insert().values(data_to_insert)
            result = connection.execute(insert_query)
            connection.commit()

            print(f"Loaded {result.rowcount} blank picks")
            return

    except SQLAlchemyError as e:
        print(f"Error interacting with the database: {e}")
        return None

    return