"""
Module containing all the functions that interact with the db via SQL.
"""

from sqlalchemy import create_engine, text

from utils.config import DB_URL

engine = create_engine(DB_URL, echo=False) # TODO set echo to False

with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL
        )
    """))
    connection.commit()


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
            "year": 2001
          }
        },
        "..."
    ]
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating FROM movies"))
        movies = result.fetchall()

    return [{"title": row[0], "details": {"year": row[1], "rating": row[2]}} for row in movies]


def add_movie_to_db(title: str, year: int, rating: float) -> None:
    """
    Adds a movie to the database via SQL.
    :param title: str containing the title of the movie.
    :param year: int containing the year of the movie.
    :param rating: float containing the rating of the movie.
    :return: None
    """
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating) VALUES (:title, :year, :rating)"),
                               {"title": title, "year": year, "rating": rating})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


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
            print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")


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
            print(f"Movie '{title}' updated successfully.")
        except Exception as e:
            print(f"Error: {e}")