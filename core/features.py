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
    prompt_sorting_descending,
    prompt_min_rating,
    prompt_min_year,
    prompt_max_year
)
from data.movie_storage import (
    add_movie_to_db,
    delete_movie_from_db,
    update_movie_from_db,
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
        print(f">>> {movie["title"]} ({movie["details"]['year']}): {movie["details"]['rating']}")


def add_movie(movies: list) -> None:
    """
    Adds a movie with corresponding info to the database.
    :param movies: list of movies (aka database).
    :return: None
    """
    print(title(f"Add Movie") + ":")
    movie_name = prompt_movie_name()
    if is_already_in_database(movies, movie_name):
        print(error(f"\nSorry, the movie '{movie_name}' is already in the database!"))

        return

    movie_rating = prompt_movie_rating()
    movie_year = prompt_movie_year()
    add_movie_to_db(movie_name, movie_rating, movie_year)
    print(success(f"\nMovie '{movie_name}' successfully added"))


def delete_movie(movies: list) -> None:
    """
    Deletes a movie with corresponding info from the database.
    :param movies: list of movies (aka database).
    :return: None
    """
    print(title(f"Delete Movie") + ":")
    movie_name = prompt_movie_name()
    if not is_already_in_database(movies, movie_name):
        print(error(f"\nSorry, the movie '{movie_name}' is not in the database!"))

        return

    delete_movie_from_db(movie_name)
    print(success(f"\nMovie '{movie_name}' successfully deleted"))


def update_movie(movies: list) -> None:
    """
    Updates a movie rating in the database.
    :param movies: list of movies (aka database).
    :return: None
    """
    print(title(f"Update Movie") + ":")
    movie_name = prompt_movie_name()
    if not is_already_in_database(movies, movie_name):
        print(error(f"\nSorry, the movie '{movie_name}' is not in the database!"))

        return

    new_rating = prompt_movie_rating()
    update_movie_from_db(movie_name, new_rating)
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
    print(title(f"Your movie for tonight") + ": ")
    print(f"{random_movie["title"]}, it's rated {random_movie["details"]["rating"]}")


def search_movie(movies: list) -> None:
    """
    Searches for a movie in the database.
    :param movies: list of movies (aka database).
    :return: None
    """
    print(title(f"Search Movie") + ":")
    movie_name = prompt_movie_name()
    search_matching = {}
    for movie in movies:
        if movie_name.lower() in movie["title"].lower():
            search_matching[movie["title"]] = movie["details"]["rating"]
        else:
            distance = get_edit_distance(movie["title"].lower(), movie_name.lower())
            if distance <= 4:
                search_matching[movie["title"]] = movie["details"]["rating"]

    if not search_matching:
        print(error(f"\nSorry, there's no match for '{movie_name}' in the database!"))

        return

    print(title(f"\nSearch Results for '{movie_name}'") + ":")
    for movie, rating in search_matching.items():
        print(f"{movie}: {rating}")


def list_movies_sorted_by_rating(movies: list) -> None:
    """
    Sorts and prints the movies by descending rating.
    :param movies: list of movies (aka database).
    :return: None
    """
    movies_sorted_by_rating = sorted(movies, key=lambda item: item["details"]["rating"], reverse=True)
    print(title(f"Movies Sorted by Rating") + ":")
    for movie in movies_sorted_by_rating:
        print(f">>> {movie["title"]}: {movie["details"]["rating"]}")


def list_movies_sorted_by_year(movies: list) -> None:
    """
    Sorts and prints the movies by year.
    Whether ascending or descending is up to the user.
    :param movies: list of movies (aka database).
    :return: None
    """
    sorting_choice = prompt_sorting_descending()
    movies_sorted_by_year_descending = sorted(movies, key=lambda item: item["details"]["year"], reverse=True)
    movies_sorted_by_year_ascending = sorted(movies, key=lambda item: item["details"]["year"], reverse=False)
    print(title(f"\nMovies Sorted by Year") + ":")
    if sorting_choice:
        for movie in movies_sorted_by_year_descending:
            print(f">>> {movie["title"]} ({movie["details"]["year"]}): {movie["details"]["rating"]}")

    else:
        for movie in movies_sorted_by_year_ascending:
            print(f">>> {movie["title"]} ({movie["details"]["year"]}): {movie["details"]["rating"]}")


def filter_movies(movies: list) -> None:
    """
    Filters out movies as per parameters given by user and prints the result.
    :param movies: list of movies (aka database).
    :return: None
    """
    print(title(f"Filter Movies") + ":")
    min_rating = prompt_min_rating()
    min_year = prompt_min_year()
    max_year = prompt_max_year()
    print(title(f"\nFiltered Movies") + ":")
    for movie in movies:
        if movie["details"]["rating"] >= min_rating and min_year <= movie["details"]["year"] <= max_year:
            print(f">>> {movie['title']} ({movie["details"]['year']}): {movie['details']['rating']}")


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
    if not os.path.exists("output"):
        os.makedirs("output")

    file_path = os.path.join("output", "ratings_histogram.png")
    plt.savefig(file_path)
    plt.show()
    print(success(f"Movies' Ratings Histogram saved to ..."))
    print(success(f"  'current directory + {file_path}'"))
