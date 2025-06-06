import os
import json


def get_movies_from_db() -> list:
    """
    Loads the information from the JSON file and returns the data.
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
    filename = os.path.join(os.getcwd(), "data", "data.json")
    with open(filename, "r", encoding="utf-8") as handle:
        movies = json.load(handle)

        return movies


def save_movies_to_db(movies: list) -> None:
    """
    Gets all the movies as an argument and saves them to the JSON file.
    :param movies: list of dictionaries that contains the movies database.
    :return: None
    """
    with open("data.json", "w", encoding="utf-8") as handle:
        json.dump(movies, handle, ensure_ascii=False, indent=4)


def add_movie_to_db(movie_name: str, movie_rating: float, movie_year: int) -> None:
    """
    Adds a movie to the database by:
    (1) loading the JSON file
    (2) updating the database
    (3) saving the movies to the database (aka JSON file)..
    :param movie_name: str containing the name of the movie.
    :param movie_rating: float containing the rating of the movie.
    :param movie_year: int containing the year of release of the movie.
    :return: None
    """
    movies = get_movies_from_db()
    movies.append({"title": movie_name, "details": {"rating": movie_rating, "year": movie_year}})
    save_movies_to_db(movies)


def delete_movie_from_db(movie_name: str) -> None:
    """
    Deletes a movie from the database by:
    (1) loading the JSON file
    (2) updating the database
    (3) saving the movies to the database (aka JSON file).
    :param movie_name: str containing the name of the movie.
    :return: None
    """
    movies = get_movies_from_db()
    for movie in movies:
        if movie["title"].lower() == movie_name.lower():
            movies.remove(movie)

    save_movies_to_db(movies)


def update_movie_from_db(movie_name: str, movie_rating: float) -> None:
    """
    Updates a movie from the database by:
    (1) loading the JSON file
    (2) updating the rating of the given movie
    (3) saving the movies to the database (aka JSON file).
    :param movie_name: str containing the name of the movie.
    :param movie_rating: float containing the rating of the given movie.
    :return: None
    """
    movies = get_movies_from_db()
    for movie in movies:
        if movie["title"].lower() == movie_name.lower():
            movie["details"]["rating"] = movie_rating

    save_movies_to_db(movies)
