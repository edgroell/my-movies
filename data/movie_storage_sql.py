"""
Module containing all the functions that interact with the db via SQL.
"""

import os

from sqlalchemy import create_engine, text

DB_PATH = os.path.join(os.path.dirname(__file__), "movies.db")
DB_URL = f"sqlite:///{DB_PATH}"

try:
    engine = create_engine(DB_URL, echo=False) # TODO set echo to False
except Exception as e:
    print(f"Failed to create engine: {e}")

try:
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL, 
                poster TEXT UNIQUE NOT NULL
            )
        """))
        connection.commit()
except Exception as e:
    print(f"Failed to create table: {e}")

def get_movies_from_db() -> list:
    """
    Loads the information from the db via SQL and returns the data.
    :return: movies: list of dictionaries that contains the movies database.
        Data structure is as follows:
    [
        {
          "title": "A Beautiful Mind",
          "details": {
            "rating": 10,
            "year": 2001,
            "poster": "https://..."
          }
        },
        "..."
    ]
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster FROM movies"))
        movies = result.fetchall()

    return [{"title": row[0], "details": {"year": row[1], "rating": row[2]}, "poster": row[3]} for row in movies]


def add_movie_to_db(title: str, year: int, rating: float, poster: str) -> None:
    """
    Adds a movie to the database via SQL.
    :param title: str containing the title of the movie.
    :param year: int containing the year of the movie.
    :param rating: float containing the rating of the movie.
    :param poster: str containing the poster image URL of the movie.
    :return: None
    """
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating, poster) VALUES (:title, :year, :rating, :poster)"),
                               {"title": title, "year": year, "rating": rating, "poster": poster})
            connection.commit()

        except Exception as e:
            print(f"An error occurred: {e}")


def delete_movie_from_db(title: str) -> None:
    """
    Deletes a movie from the database via SQL.
    :param title: str containing the title of the movie.
    :return: None
    """
    with engine.connect() as connection:
        try:
            connection.execute(text("DELETE FROM movies WHERE title = :title"), {"title": title})
            connection.commit()

        except Exception as e:
            print(f"An error occurred: {e}")


def update_movie_from_db(title: str, rating: float) -> None:
    """
    Updates a movie from the database via SQL.
    :param title: str containing the title of the movie.
    :param rating: float containing the rating of the movie.
    :return: None
    """
    with engine.connect() as connection:
        try:
            connection.execute(text("UPDATE movies SET rating = :rating WHERE title = :title"), {"title": title, "rating": rating})
            connection.commit()

        except Exception as e:
            print(f"Error: {e}")