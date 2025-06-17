"""
Module that contains all the helper functions.
"""

import statistics
import Levenshtein

def is_already_in_database(movies: list, movie_name: str) -> bool:
    """
    Performs a check whether the given movie is already in the database.
    :param movies: list of movies (aka database).
    :param movie_name: str containing the movie title to be checked.
    :return: bool:
        True if the movie is already in the database.
        False otherwise.
    """
    for movie in movies:
        if movie["title"].lower() == movie_name.lower().strip():

            return True

    return False


def normalize_all_ratings(ratings_list: list) -> list:
    """
    Takes all ratings from API data set and normalizes them.
    :param ratings_list: list: contains all ratings from API data.
    :return: normalized_ratings_list: list: contains normalized
        (only floats) ratings from API data.
    """
    normalized_ratings_list = []
    for rating in ratings_list:
        if rating[-3:] == "/10":
            new_rating = float(rating[:-3]) * 10
            normalized_ratings_list.append(new_rating)
        elif rating[-4:] == "/100":
            new_rating = float(rating[:-4])
            normalized_ratings_list.append(new_rating)
        elif rating[-1:] == "%":
            new_rating = float(rating[:-1])
            normalized_ratings_list.append(new_rating)

    return normalized_ratings_list


def get_average_normalized_ratings(normalized_ratings_list: list) -> float:
    """
    Takes all normalized ratings and returns the rounded average.
    :param normalized_ratings_list: contains normalized
        (only floats) ratings from API data.
    :return: movie_rating: float: returns rounded average of normalized ratings.
    """
    movie_rating = round(statistics.mean(normalized_ratings_list), 2)

    return movie_rating


def get_movie_rating(movie_data: dict) -> float:
    """
    Extracts all ratings from the API into a list of strings.
    :param movie_data: dict: containing all movie data from the API.
    :return: movie_rating: float: returns rounded average of normalized ratings.
    """
    ratings_list = []
    ratings = movie_data["Ratings"]
    for rating in ratings:
        ratings_list.append(rating["Value"])

    if ratings_list:
        normalized_ratings_list = normalize_all_ratings(ratings_list)
        movie_rating = get_average_normalized_ratings(normalized_ratings_list)
    else:
        movie_rating = "N/A"

    return movie_rating


def get_movie_countries(movie: dict) -> list:
    """
    Extracts all countries from the dictionary and returns a list of countries.
    :param movie: dict: containing all movie data from the API.
    :return: movie_countries: list: contains all countries of the movie.
    """
    movie_countries = movie["details"]["country"].split(", ")

    return movie_countries


def get_ratings_list(movies: list) -> list:
    """
    Collects all ratings from each movie in the database.
    :param movies: list of movies (aka database).
    :return: ratings_list: list containing all ratings.
    """
    ratings_list = []
    for movie in movies:
        try:
            ratings_list.append(int(movie["details"]["rating"]))
        except ValueError:
            pass

    return ratings_list


def get_average_rating(movies: list) -> float:
    """
    Calculates the average rating of all movies from the database.
    :param movies: list of movies (aka database).
    :return: average_rating: float containing the average rating of all movies.
    """
    ratings_list = get_ratings_list(movies)
    average_rating = round(statistics.mean(ratings_list), 2)

    return average_rating


def get_median_rating(movies: list) -> float:
    """
    Calculates the median rating of all movies from the database.
    :param movies: list of movies (aka database).
    :return: median_rating: float containing the median rating of all movies.
    """
    ratings_list = get_ratings_list(movies)
    median_rating = round(statistics.median(ratings_list), 2)

    return median_rating


def get_best_movie(movies: list) -> dict:
    """
    Collects which movie(s) has/have the best rating.
    :param movies: list of movies (aka database).
    :return: best_movies: dict containing the best-rated movie(s).
    """
    ratings_list = get_ratings_list(movies)
    best_movies = {}
    for movie in movies:
        if movie["details"]["rating"] == max(ratings_list):
            best_movies[movie["title"]] = movie["details"]["rating"]

    return best_movies


def get_worst_movie(movies: list) -> dict:
    """
    Collects which movie(s) has/have the worst rating.
    :param movies: list of movies (aka database).
    :return: worst_movies: dict containing the worst-rated movie(s).
    """
    ratings_list = get_ratings_list(movies)
    worst_movies = {}
    for movie in movies:
        if movie["details"]["rating"] == min(ratings_list):
            worst_movies[movie["title"]] = movie["details"]["rating"]

    return worst_movies


def get_edit_distance(movie: str, movie_name: str) -> int:
    """
    Calculates the edit distance between the movie from the database and the movie searched.
    :param movie: movie from the database.
    :param movie_name: movie searched by user.
    :return: edit_distance: int containing the edit distance between the 2 movie names.
    """
    edit_distance = Levenshtein.distance(movie, movie_name)

    return edit_distance
