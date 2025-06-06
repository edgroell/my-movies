import os
import json
# TODO PEP 8

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


def save_movies_to_db(movies: list):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    try:
        with open("data.json", "w", encoding="utf-8") as handle:
            json.dump(movies, handle, ensure_ascii=False, indent=4)
        return True
    except FileNotFoundError:
        return False


def add_movie_to_db(movie_name, movie_rating, movie_year):
    """
    Adds a movie to the database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies_from_db()
    movies.append({"title": movie_name, "details": {"rating": movie_rating, "year": movie_year}})
    save_movies_to_db(movies)


def delete_movie_from_db(movie_name):
    """
    Deletes a movie from the database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies_from_db()
    for movie in movies:
        if movie["title"].lower() == movie_name.lower():
            movies.remove(movie)
    save_movies_to_db(movies)


def update_movie_from_db(movie_name, movie_rating):
    """
    Updates a movie from the database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies_from_db()
    for movie in movies:
        if movie["title"].lower() == movie_name.lower():
            movie["details"]["rating"] = movie_rating
    save_movies_to_db(movies)
