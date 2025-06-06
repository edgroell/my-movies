import os
import random
import matplotlib.pyplot as plt

from utils.text_formatter import TextFormatter
from utils.helpers import (
    is_already_in_database,
    get_ratings_list,
    get_average_rating,
    get_median_rating,
    get_best_movie,
    get_worst_movie,
    get_edit_distance
)
from utils.user_prompts import (
    prompt_movie_name,
    prompt_movie_rating,
    prompt_movie_year,
    prompt_sorting_descending
)


title = TextFormatter.title
success = TextFormatter.success
error = TextFormatter.error


def list_movies(movies: list) -> None:
    """
    Prints the entire list of movies with corresponding info.
    :param movies: list of movies (aka database).
    :return: None
    """
    print(title(f"{len(movies)} movies in total") + ":")
    for movie in movies:
        print(f">>> {movie['title']} ({movie['year']}): {movie['rating']}")


def add_movie(movies: list) -> None:
    """
    Adds a movie with corresponding info to the database.
    :param movies: list of movies (aka database).
    :return: None
    """
    movie_name = prompt_movie_name()
    if is_already_in_database(movies, movie_name):
        print(error(f"\nSorry, the movie '{movie_name}' is already in the database!\n"))

        return

    movie_rating = prompt_movie_rating()
    movie_year = prompt_movie_year()
    movies.append({"title": movie_name, "rating": movie_rating, "year": movie_year})
    print(success(f"\nMovie {movie_name} successfully added"))


def delete_movie(movies: list) -> None:
    """
    Deletes a movie with corresponding info from the database.
    :param movies: list of movies (aka database).
    :return: None
    """
    movie_name = prompt_movie_name()
    if not is_already_in_database(movies, movie_name):
        print(error(f"\nSorry, the movie '{movie_name}' is not in the database!"))

        return

    for movie in movies:
        if movie["title"].lower() == movie_name.lower():
            movies.remove(movie)
            print(success(f"\nMovie '{movie_name}' successfully deleted"))


def update_movie(movies: list) -> None:
    """
    Updates a movie rating in the database.
    :param movies: list of movies (aka database).
    :return: None
    """
    movie_name = prompt_movie_name()
    if not is_already_in_database(movies, movie_name):
        print(error(f"\nSorry, the movie '{movie_name}' is not in the database!"))

        return

    new_rating = prompt_movie_rating()
    for movie in movies:
        if movie["title"].lower() == movie_name.lower():
            movie["rating"] = new_rating
    print(success(f"\nRating of movie '{movie_name}' updated to {new_rating}"))


def list_stats(movies: list) -> None:
    """
    Prints some key statistics from the database data.
    :param movies: list of movies (aka database).
    :return: None
    """
    print(title(f"KPIs") + ":")
    print("Average rating: ", get_average_rating(movies))
    print("Median rating: ", get_median_rating(movies))
    print("Best movie(s): ", end="")
    best_movies = get_best_movie(movies)
    for movie, rating in best_movies.items():
        print(f"{movie}: {rating}", end="    ")
    print("\nWorst movie(s): ", end="")
    worst_movies = get_worst_movie(movies)
    for movie, rating in worst_movies.items():
        print(f"{movie}: {rating}", end="    ")
    print()


def get_random_movie(movies: list) -> None:
    """
    Selects and prints a random movie from the database.
    :param movies: list of movies (aka database).
    :return: None
    """
    random_movie = random.choice(movies)
    print(title(f"Your movie for tonight") + ": ", end="")
    print(f"{random_movie['title']}, it's rated {random_movie['rating']}")


def search_movie(movies: list) -> None:
    """
    Searches for a movie in the database.
    :param movies: list of movies (aka database).
    :return: None
    """
    movie_name = prompt_movie_name()
    search_matching = {}
    for movie in movies:
        if movie_name.lower() in movie["title"].lower():
            search_matching[movie["title"]] = movie["rating"]
        else:
            distance = get_edit_distance(movie["title"].lower(), movie_name.lower())
            if distance <= 4:
                search_matching[movie["title"]] = movie["rating"]

    if not search_matching:
        print(error(f"\nSorry, we can't find any match for '{movie_name}' in the database!"))

        return

    print(title(f"\nSearch results for '{movie_name}'") + ":")
    for movie, rating in search_matching.items():
        print(f"{movie}: {rating}")


def list_movies_sorted_by_rating(movies: list) -> None:
    """
    Sorts and prints the movies by descending rating.
    :param movies: list of movies (aka database).
    :return: None
    """
    print(title(f"Movies sorted by rating") + ":")
    movies_sorted_by_rating = sorted(movies, key=lambda item: item["rating"], reverse=True)
    for movie in movies_sorted_by_rating:
        print(f"{movie['title']}: {movie['rating']}")


def list_movies_sorted_by_year(movies: list) -> None:
    """
    Sorts and prints the movies by year.
    Whether ascending or descending is up to the user.
    :param movies: list of movies (aka database).
    :return: None
    """
    sorting_choice = prompt_sorting_descending()
    movies_sorted_by_year_descending = sorted(movies, key=lambda item: item["rating"], reverse=True)
    movies_sorted_by_year_ascending = sorted(movies, key=lambda item: item["rating"], reverse=False)
    print(title(f"\nMovies sorted by rating") + ":")
    if sorting_choice:
        for movie in movies_sorted_by_year_descending:
            print(f"{movie['title']} ({movie["year"]}): {movie['rating']}")

    else:
        for movie in movies_sorted_by_year_ascending:
            print(f"{movie['title']} ({movie["year"]}): {movie['rating']}")


def create_ratings_histogram(movies: list) -> None:
    """
    Creates, saves, and displays a histogram of all ratings of movies.
    :param movies: list of movies (aka database).
    :return: None
    """
    data = get_ratings_list(movies)
    plt.hist(data, bins=5, edgecolor="black", color="green", alpha=0.7)
    plt.title("My Movies' Ratings Histogram")
    plt.xlabel("Ratings")
    plt.ylabel("Frequency")
    output_dir = os.path.join(os.getcwd(), "..", "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = os.path.join(output_dir, "ratings_histogram.png")
    plt.savefig(file_path)
    plt.show()
    print(success(f"\nMovies' Ratings Histogram saved to {file_path}"))
