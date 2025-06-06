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
        movie_title = next(iter(movie))
        movie_details = movie[movie_title]
        if movie_title.lower() == movie_name.lower().strip():

            return True

    return False


def get_ratings_list(movies: list) -> list:
    """
    Collects all ratings from each movie in the database.
    :param movies: list of movies (aka database).
    :return: ratings_list: list containing all ratings.
    """
    ratings_list = []
    for movie in movies:
        movie_title = next(iter(movie))
        movie_details = movie[movie_title]
        ratings_list.append(movie_details["rating"])

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
        movie_title = next(iter(movie))
        movie_details = movie[movie_title]
        if movie_details["rating"] == max(ratings_list):
            best_movies[movie_title] = movie_details["rating"]

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
        movie_title = next(iter(movie))
        movie_details = movie[movie_title]
        if movie_details["rating"] == min(ratings_list):
            worst_movies[movie_title] = movie_details["rating"]

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
