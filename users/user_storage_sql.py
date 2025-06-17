"""
Module containing all the functions that interact with the user db via SQL.
"""

import os

from sqlalchemy import create_engine, text

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")
USER_DB_URL = f"sqlite:///{DB_PATH}"

try:
    engine = create_engine(USER_DB_URL, echo=False)
except Exception as e:
    print(f"Failed to create engine: {e}")
    raise

try:
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """))
        connection.commit()
except Exception as e:
    print(f"Failed to create table: {e}")

def get_users_from_db() -> list:
    """
    Loads the information from the user database via SQL and returns the users data.
    :return: users: list of dictionaries containing the users' data.
        Data structure is as follows:
        [
            {
                "id": 1,
                "name": "Ed"
            },
            "..."
        ]
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id, name FROM users"))
        users = result.fetchall()

    return [{"id": row[0], "name": row[1]} for row in users]


def add_user_to_db(user_name: str) -> bool:
    """
    Adds a user to the user database via SQL.
    :param user_name: str containing the name of the user.
    :return: bool:
        True: if user successfully added to database,
        False: if an error occurred.
    """
    try:
        with engine.connect() as connection:
            connection.execute(
                text("INSERT INTO users (name) VALUES (:name)"),
                {"name": user_name}
            )
            connection.commit()

        return True

    except Exception as e:
        print(f"An error occurred while adding user: {e}")

        return False


def delete_user_from_db(user_name: str) -> bool:
    """
    Deletes a user from the user database via SQL.
    :param user_name: str containing the name of the user.
    :return: bool:
        True: if user successfully deleted from database.
        False: if an error occurred.
    """
    try:
        with engine.connect() as connection:
            connection.execute(
                text("DELETE FROM users WHERE name = :name"),
                {"name": user_name}
            )
            connection.commit()

        return True

    except Exception as e:
        print(f"An error occurred while deleting user: {e}")

        return False


def update_user_from_db(new_user_name: str, user_name: str) -> bool:
    """
    Updates a user's name in the user database via SQL.
    :param new_user_name: str containing the new name of the user.
    :param user_name: str containing the old name of the user.
    :return: bool:
        True: if user successfully updated in database.
        False: if an error occurred.
    """
    with engine.connect() as connection:
        try:
            connection.execute(
                text("UPDATE users SET name = :new_user_name WHERE name = :user_name"),
                {"new_user_name": new_user_name, "user_name": user_name}
            )
            connection.commit()

            return True

        except Exception as e:
            print(f"An error occurred: {e}")

            return False
