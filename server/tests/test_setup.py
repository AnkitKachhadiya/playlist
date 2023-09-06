from setup import create_db_table, is_db_table_exist, insert_json_data_to_db


def test_create_db_table():
    assert create_db_table() is None, "Error while creating database table."


def test_is_db_table_exist():
    assert is_db_table_exist() is True, "Error database table does not exist."


def test_insert_json_data_to_db():
    assert (
        insert_json_data_to_db() is None
    ), "Error while inserting data to database table."
