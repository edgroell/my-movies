"""
Module containing all the functions that interact with the movie db via SQL.
"""

import os

from sqlalchemy import create_engine, text

DB_PATH = os.path.join(os.path.dirname(__file__), "movies.db")
MOVIE_DB_URL = f"sqlite:///{DB_PATH}"

try:
    engine = create_engine(MOVIE_DB_URL, echo=False)
except Exception as e:
    print(f"Failed to create engine: {e}")

try:
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                note TEXT NOT NULL,
                poster TEXT NOT NULL,
                country TEXT NOT NULL,
                imdb_id TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(user_id, imdb_id)
            )
        """))
        connection.commit()
except Exception as e:
    print(f"Failed to create table: {e}")


def get_movies_from_db(user_id: int) -> list:
    """
    Loads the information from the movie database via SQL
    and returns the movies data for a specific user.
    :param user_id: The ID of the user whose movies are to be retrieved.
    :return: A list of dictionaries containing the movies data.
        Data structure is as follows:
        [
            {
                "title": "A Beautiful Mind",
                "details": {
                    "year": 2001,
                    "rating": 10,
                    "note": "Best Ever!",
                    "poster": "https://...",
                    "country": "United States",
                    "imdb_id": "tt0268978"
                }
            },
            "..."
        ]
    """
    with engine.connect() as connection:
        result = connection.execute(text("""
            SELECT
                movies.title, movies.year, movies.rating, movies.note,
                movies.poster, movies.country, movies.imdb_id
            FROM movies
            WHERE movies.user_id = :user_id
        """), {"user_id": user_id})

        movies = result.fetchall()

    return [{
        "title": row[0],
        "details": {
            "year": row[1],
            "rating": row[2],
            "note": row[3],
            "poster": row[4],
            "country": row[5],
            "imdb_id": row[6]
        }
    } for row in movies]


def add_movie_to_db(
    user_id: int, title: str, year: int, rating: float,
    note: str, poster: str, country: str, imdb_id: str) -> bool:
    """
    Adds a movie to the database via SQL.
    :param user_id: int containing the user ID associated with the transaction.
    :param title: str containing the title of the movie.
    :param year: int containing the year of the movie.
    :param rating: float containing the rating of the movie.
    :param note: str containing the note on the movie.
    :param poster: str containing the poster image URL of the movie.
    :param country: str containing the country(ies) of the movie.
    :param imdb_id: str containing the IMDb ID of the movie.
    :return: bool: True if movie successfully added to database, False otherwise.
    """
    with engine.connect() as connection:
        try:
            connection.execute(
                text(
                    "INSERT INTO movies ("
                    "user_id, title, year, rating, note, poster, country, imdb_id) "
                    "VALUES ("
                    ":user_id, :title, :year, :rating, :note, :poster, :country, :imdb_id)"
                ),
                {
                    "user_id": user_id,
                    "title": title,
                    "year": year,
                    "rating": rating,
                    "note": note,
                    "poster": poster,
                    "country": country,
                    "imdb_id": imdb_id,
                },
            )
            connection.commit()

            return True

        except Exception as e:
            print(f"An error occurred: {e}")

            return False



def delete_movie_from_db(user_id: int, title: str) -> bool:
    """
    Deletes a movie from the database via SQL.
    :param user_id: int containing the user ID associated with the transaction.
    :param title: str containing the title of the movie.
    :return: bool:
        True if movie successfully deleted from database,
        False otherwise.
    """
    with engine.connect() as connection:
        try:
            connection.execute(
                text("DELETE FROM movies "
                     "WHERE user_id = :user_id AND title = :title"),
                {"user_id": user_id, "title": title},
            )
            connection.commit()

            return True

        except Exception as e:
            print(f"An error occurred: {e}")

            return False


def update_movie_from_db(user_id: int, title: str, note: str) -> bool:
    """
    Updates a movie's note in the database via SQL.
    :param user_id: int containing the user ID associated with the transaction.
    :param title: str containing the title of the movie.
    :param note: str containing a personal note on the movie.
    :return: bool:
        True if movie successfully updated in database,
        False otherwise.
    """
    with engine.connect() as connection:
        try:
            connection.execute(
                text(
                    "UPDATE movies SET note = :note "
                    "WHERE user_id = :user_id AND title = :title"
                ),
                {"user_id": user_id, "title": title, "note": note},
            )
            connection.commit()

            return True

        except Exception as e:
            print(f"An error occurred: {e}")

            return False
