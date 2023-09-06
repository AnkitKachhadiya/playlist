from os import getenv
from dotenv import load_dotenv
import psycopg2

load_dotenv()


def get_db_connection():
    try:
        connection = psycopg2.connect(
            database=getenv("DB_NAME"),
            user=getenv("DB_USER"),
            password=getenv("DB_PASSWORD"),
            host=getenv("DB_HOST"),
            port=getenv("DB_PORT"),
        )

        connection.autocommit = True

        return connection

    except Exception as e:
        print("Db connection failed.")
        print(e)


def close_db_connection(connection):
    if connection:
        connection.close()
