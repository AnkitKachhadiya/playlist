from db import get_db_connection, close_db_connection


def test_db_connection():
    connection = get_db_connection()
    assert connection is not None, "Error while connecting database."
    close_db_connection(connection)
