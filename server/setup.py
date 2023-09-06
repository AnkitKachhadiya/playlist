from db import get_db_connection, close_db_connection
from pathlib import Path
from json import load
from psycopg2.extras import execute_values


def create_db_table():
    connection = get_db_connection()

    if not connection:
        return

    try:
        cursor = connection.cursor()

        SQL_FILE_NAME = "db.setup.sql"
        file_path = get_file_path(SQL_FILE_NAME)

        with open(file_path, "r") as sql_file:
            sql_commands = sql_file.read()

        cursor.execute(sql_commands)
        cursor.close()

    except Exception as e:
        print("Db table creation failed")
        print(e)
    finally:
        close_db_connection(connection)


def get_file_path(filename):
    return Path(filename).resolve()


def is_db_table_exist():
    DB_TABLE = "songs"

    connection = get_db_connection()

    if not connection:
        return

    try:
        cursor = connection.cursor()

        query = f"""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = '{DB_TABLE}'
        );
        """
        cursor.execute(query)
        status = cursor.fetchone()[0]
        cursor.close()

        return status

    except Exception as e:
        print(e)
    finally:
        close_db_connection(connection)


def get_json_data():
    JSON_FILE_NAME = "playlist.json"

    file_path = get_file_path(JSON_FILE_NAME)
    with open(file_path, "r") as json_file:
        return load(json_file)


def insert_json_data_to_db():
    if not is_db_table_exist():
        return

    connection = get_db_connection()

    if not connection:
        return

    try:
        cursor = connection.cursor()

        json_data = get_json_data()
        normalized_data = get_normalized_json_data(json_data)

        values_to_insert = []

        for value in normalized_data.values():
            tuple = (
                value["id"],
                value["title"],
                value["danceability"],
                value["energy"],
                value["key"],
                value["loudness"],
                value["mode"],
                value["acousticness"],
                value["instrumentalness"],
                value["liveness"],
                value["valence"],
                value["tempo"],
                value["duration_ms"],
                value["time_signature"],
                value["num_bars"],
                value["num_sections"],
                value["num_segments"],
                value["class"],
            )

            values_to_insert.append(tuple)

        insert_query = """
        INSERT INTO songs VALUES %s
        """

        execute_values(cursor, insert_query, values_to_insert)
        cursor.close()

    except Exception as e:
        print("Db data insertion failed")
        print(e)
    finally:
        close_db_connection(connection)


def get_normalized_json_data(json_data):
    normalized_data = {}

    for key, values in json_data.items():
        for index, value in values.items():
            if index not in normalized_data:
                normalized_data[index] = {}
            normalized_data[index][key] = value

    return normalized_data


def init():
    create_db_table()
    insert_json_data_to_db()


init()
