"""
Module containing all the functions that interact with the db via SQL.
"""

import os

from sqlalchemy import create_engine, text

DB_PATH = os.path.join(os.path.dirname(__file__), "movies.db")
DB_URL = f"sqlite:///{DB_PATH}"

try:
    engine = create_engine(DB_URL, echo=False)
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
                note TEXT NOT NULL,
                poster TEXT UNIQUE NOT NULL,
                country TEXT NOT NULL,
                imdbID TEXT UNIQUE NOT NULL
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
            "year": 2001,
            "rating": 10,
            "note": "...",
            "poster": "https://..."
            "country" : "United States",
            "imdbID": "tt0268978"
          }
        },
        "..."
    ]
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, note, poster, country, imdbID FROM movies"))
        movies = result.fetchall()

    return [{
        "title": row[0],
        "details": {
            "year": row[1],
            "rating": row[2],
            "note": row[3],
            "poster": row[4],
            "country": row[5],
            "imdbID": row[6]
        }
    } for row in movies]


def add_movie_to_db(title: str, year: int, rating: float, note: str, poster: str, country: str, imdbID: str) -> bool:
    """
    Adds a movie to the database via SQL.
    :param title: str containing the title of the movie.
    :param year: int containing the year of the movie.
    :param rating: float containing the rating of the movie.
    :param note: str containing the note on the movie.
    :param poster: str containing the poster image URL of the movie.
    :param country: str containing the country(ies) of the movie.
    :param imdbID: str containing the IMDb ID of the movie.
    :return: bool:
        True: if movie successfully added to database.
        False: if an error occurred.
    """
    with engine.connect() as connection:
        try:
            connection.execute(text(
                "INSERT INTO movies (title, year, rating, note, poster, country, imdbID) "
                "VALUES (:title, :year, :rating, :note, :poster, :country, :imdbID)"),
                               {
                                   "title": title,
                                   "year": year,
                                   "rating": rating,
                                   "note": note,
                                   "poster": poster,
                                   "country": country,
                                   "imdbID": imdbID
                               })
            connection.commit()

            return True

        except Exception as e:
            print(f"An error occurred: {e}")

            return False


def delete_movie_from_db(title: str) -> bool:
    """
    Deletes a movie from the database via SQL.
    :param title: str containing the title of the movie.
    :return: bool:
        True: if movie successfully deleted from database.
        False: if an error occurred.
    """
    with engine.connect() as connection:
        try:
            connection.execute(text(
                "DELETE FROM movies "
                "WHERE title = :title"),
                {"title": title})
            connection.commit()

            return True

        except Exception as e:
            print(f"An error occurred: {e}")

            return False


def update_movie_from_db(title: str, note: str) -> bool:
    """
    Updates a movie from the database via SQL.
    :param title: str containing the title of the movie.
    :param note: str containing a personal note on the movie.
    :return: bool:
        True: if movie successfully updated in database.
        False: if an error occurred.
    """
    with engine.connect() as connection:
        try:
            connection.execute(text(
                "UPDATE movies "
                "SET note = :note "
                "WHERE title = :title"),
                {"title": title, "note": note})
            connection.commit()

            return True

        except Exception as e:
            print(f"An error occurred: {e}")

            return False
