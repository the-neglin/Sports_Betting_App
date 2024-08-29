import pandas as pd
from sqlalchemy import create_engine, insert, Table, MetaData
from sqlalchemy.exc import SQLAlchemyError
import os
import getters


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
            # Create an insert query
            metadata = MetaData()

            users_table = Table('users', metadata, autoload_with=engine)
            insert_query = insert(users_table).values(email=f"'{email}'", name=f"'{name}'")
            compiled = insert_query.compile()
            result = connection.execute(insert_query)
            connection.commit()
            
            return

    except SQLAlchemyError as e:
        print(f"Error interacting with the database: {e}")
        return None