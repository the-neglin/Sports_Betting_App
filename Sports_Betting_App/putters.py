from sqlalchemy import create_engine, insert, Table, MetaData, update
from sqlalchemy.exc import SQLAlchemyError
import os
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getters

load_dotenv()
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
            insert_query = insert(users_table).values(email=f"{email}", name=f"{name}")
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

def put_picks(picks_df):
    connection_string = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"

    try:
        engine = create_engine(connection_string)

        with engine.connect() as connection:  # noqa: F841
            Session = sessionmaker(bind=engine)
            session = Session()
            metadata = MetaData()
            picks_table = Table('picks', metadata, autoload_with=engine)

            for index, row in picks_df.iterrows():
                stmt = (
                    update(picks_table)
                    .where(
                        picks_table.c.user_id == row['user_id'], 
                        picks_table.c.game_id == row['game_id']
                    )
                    .values({
                        'choice_id': row['Spread Pick'],
                        'dd': row['Double Down?'],
                        'over_under_id': row['Over/Under Pick']
                    })
                )
                session.execute(stmt)

            session.commit()
            session.close()
            print("Picks saved successfully...")
            return
    except SQLAlchemyError as e:
        print(f"Error interacting with the database: {e}")
        return None
    
    return

def send_email(updated_df, name, email):
        GMAILPASS = os.getenv("GMAILPASS")
        columns = ['Time', 'Favorite', 'Spread', 'Underdog', 'Over/Under', 'Spread Pick', 'Double Down?', 'Over/Under Pick']
        df = updated_df[columns]

        # Convert the DataFrame to an HTML table
        df_html = df.to_html(index=False)

        # Set up the email
        sender = "nicksmassivepickem@gmail.com"
        recipient = email  # Replace with the selected user's email
        subject = f"Nick's Massive Pickem: Your Picks for Week {getters.get_week()}"
        body = f"""
            <html>
            <body>
                <p>🏈 Hey there {name}, Champion of the Gridiron! 🏆</p>
                <p>You’ve made your picks, and now the only thing standing between you and sports betting glory is...well, 
                a few teams playing football. No pressure, right? 😅</p>
                <p>Here’s a look at your picks. May the football gods be in your favor:</p>
                {df_html}
                <p>Remember, it's not just a game, it's a test of your predictive prowess! Good luck, and may your teams 
                always find the end zone. 🏟️</p>
                <p>Cheers to big wins and even bigger celebrations! 🍻</p>
            </body>
            </html>
            """

        msg = MIMEMultipart("alternative")
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject

        # Attach the HTML body to the email
        msg.attach(MIMEText(body, 'html'))

        # Gmail's SMTP server setup
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(sender, GMAILPASS)  # Use an app-specific password for security
        text = msg.as_string()
        server.sendmail(sender, recipient, text)
        server.quit()
        print(f"Email successfully sent to {email}")
        
        return