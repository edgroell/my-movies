"""
Module that contains all the commands functions for the main menu.
"""

import os
import random

import matplotlib.pyplot as plt

from data.movie_storage_sql import (
    add_movie_to_db,
    delete_movie_from_db,
    update_movie_from_db
)
from users.user_management import get_user_id
from utils.api_calls import fetch_movie_data
from utils.helpers import (
    is_already_in_movie_database,
    get_movie_rating,
    get_ratings_list,
    get_average_rating,
    get_median_rating,
    get_best_movie,
    get_worst_movie,
    get_edit_distance
)
from utils.text_formatter import TextFormatter
from utils.user_prompts import (
    prompt_movie_name,
    prompt_movie_note,
    prompt_whether_movie_note,
    prompt_sorting_descending,
    prompt_min_rating,
    prompt_min_year,
    prompt_max_year
)
from utils.web_generator import (
    get_movies_cards,
    open_template,
    inject_website_content,
    build_html_page
)

title = TextFormatter.title
success = TextFormatter.success
error = TextFormatter.error

def list_movies(movies: list, current_user: str) -> None:
    """
    Prints the entire list of movies with corresponding info.
    :param movies: list of all movies.
    :param current_user: str containing the current username.
    :return: None
    """
    if len(movies) == 0:
        print(title(f"No Movies") + ":")
    elif len(movies) == 1:
        print(title(f"{len(movies)} Movie") + ":")
    else:
        print(title(f"{len(movies)} Movies") + ":")

    if len(movies) == 0:
        print(f"No movies in your collection, {current_user}!\n"
              "You should add your favorite movies...")
    else:
        for movie in movies:
            print(f">>> {movie["title"]} ({movie["details"]["year"]}): {movie["details"]["rating"]}")
            if not movie["details"]["note"] == "N/A":
                print(f" 📝 {movie['details']['note']}")
            else:
                print(" ❌ This movie has no attached note...")


def add_movie(movies: list, current_user: str) -> None:
    """
    Adds a movie with corresponding info to the movie database.
    :param movies: list of all movies.
    :param current_user: str containing the current username.
    :return: None
    """
    print(title("Add Movie") + ":")
    movie_name = prompt_movie_name()
    if is_already_in_movie_database(movies, movie_name):
        print("\n" + error(f"Sorry {current_user}, movie '{movie_name}' is already in your collection!"))

        return

    movie_data = fetch_movie_data(movie_name)
    if movie_data is None:

        return

    if movie_data["Response"] == "False":
        print("\n" + error(f"Sorry, {movie_data["Error"]}"))

        return

    if movie_data and movie_data["Response"] == "True":
        user_id = get_user_id(current_user)
        movie_name = movie_data["Title"]
        movie_year = movie_data["Year"]
        movie_rating = get_movie_rating(movie_data)
        movie_note = prompt_whether_movie_note()
        movie_poster = movie_data["Poster"]
        movie_country = movie_data["Country"]
        movie_imdbID = movie_data["imdbID"]
        if add_movie_to_db(user_id, movie_name, movie_year, movie_rating, movie_note, movie_poster, movie_country, movie_imdbID):
            print("\n" + success(f"Movie '{movie_name}' successfully added"))

            return

        print("Sorry, there was a problem adding the movie.")


def delete_movie(movies: list, current_user: str) -> None:
    """
    Deletes a movie with corresponding info from the database.
    :param movies: list of all movies.
    :param current_user: str containing the current username.
    :return: None
    """
    print(title("Delete Movie") + ":")
    movie_name = prompt_movie_name()
    if not is_already_in_movie_database(movies, movie_name):
        print("\n" + error(f"Sorry {current_user}, movie '{movie_name}' is not in the database!"))

        return

    user_id = get_user_id(current_user)
    if delete_movie_from_db(user_id, movie_name):
        print("\n" + success(f"Movie '{movie_name}' successfully deleted"))

        return

    print("Sorry, there was a problem deleting movie.")


def update_movie(movies: list, current_user: str) -> None:
    """
    Updates a movie rating in the database.
    :param movies: list of all movies.
    :param current_user: str containing the current username.
    :return: None
    """
    print(title("Update Movie") + ":")
    movie_name = prompt_movie_name()
    if not is_already_in_movie_database(movies, movie_name):
        print("\n" + error(f"Sorry {current_user}, movie '{movie_name}' is not in the database!"))

        return

    for movie in movies:
        if movie_name.strip().lower() == movie["title"].strip().lower():
            print(f"Current note: '{movie["details"]["note"]}'")

    user_id = get_user_id(current_user)
    movie_note = prompt_movie_note()
    if update_movie_from_db(user_id, movie_name, movie_note):
        print("\n" + success(f"Note successfully added to the movie '{movie_name}'"))

        return

    print("Sorry, there was a problem updating the movie.")


def list_stats(movies: list, current_user: str) -> None:
    """
    Prints some key statistics from the database data.
    :param movies: list of all movies.
    :param current_user: str containing the current username.
    :return: None
    """
    print(title("KPIs") + ":")
    print(">>> Average Rating: ", get_average_rating(movies))
    print(">>> Median Rating: ", get_median_rating(movies))
    print(f">>> {current_user}'s Best Movie(s): ", end="")
    best_movies = get_best_movie(movies)
    for movie, rating in best_movies.items():
        print(f"{movie}: {rating}", end="    ")
    print(f"\n>>> {current_user}'s Worst Movie(s): ", end="")
    worst_movies = get_worst_movie(movies)
    for movie, rating in worst_movies.items():
        print(f"{movie}: {rating}", end="    ")
    print()


def get_random_movie(movies: list, current_user: str) -> None:
    """
    Selects and prints a random movie from the database.
    :param movies: list of all movies.
    :param current_user: str containing the current username.
    :return: None
    """
    random_movie = random.choice(movies)
    print(title(f"{current_user}'s Random Movie") + ": ")
    print(f">>> {random_movie["title"]}, it's rated {random_movie["details"]["rating"]}")


def search_movie(movies: list,current_user: str) -> None:
    """
    Searches for a movie in the database.
    :param movies: list of all movies.
    :param current_user: str containing the current username.
    :return: None
    """
    print(title("Search Movie") + ":")
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
        print("\n" + error(f"Sorry {current_user}, no match for '{movie_name}'!"))

        return

    print("\n" + title(f"{current_user}'s Search Results for '{movie_name}'") + ":")
    for movie, rating in search_matching.items():
        print(f">>> {movie}: {rating}")


def list_movies_sorted_by_rating(movies: list, current_user: str) -> None:
    """
    Sorts and prints the movies by descending rating.
    :param movies: list of all movies.
    :param current_user: str containing the current username.
    :return: None
    """
    movies_sorted_by_rating = sorted(
        movies,
        key=lambda item: (-item["details"]["rating"], item["title"]),
        reverse=False
    )
    print(title(f"{current_user}'s Movies Sorted by Rating") + ":")
    for movie in movies_sorted_by_rating:
        print(f">>> {movie["title"]}: {movie["details"]["rating"]}")


def list_movies_sorted_by_year(movies: list, current_user: str) -> None:
    """
    Sorts and prints the movies by year.
    Whether ascending or descending is up to the user.
    :param movies: list of all movies.
    :param current_user: str containing the current username.
    :return: None
    """
    print(title("Sorting by Year") + ":")
    sorting_choice = prompt_sorting_descending()
    movies_sorted_by_year_descending = sorted(
        movies,
        key=lambda item: (-item["details"]["year"], item["title"]),
        reverse=False
    )
    movies_sorted_by_year_ascending = sorted(
        movies,
        key=lambda item: (item["details"]["year"], item["title"]),
        reverse=False
    )
    print(title("\n" + f"{current_user}'s Movies Sorted by Year") + ":")
    if sorting_choice:
        for movie in movies_sorted_by_year_descending:
            print(f">>> {movie["title"]} ({movie["details"]["year"]}): "
                  f"{movie["details"]["rating"]}")

    else:
        for movie in movies_sorted_by_year_ascending:
            print(f">>> {movie["title"]} ({movie["details"]["year"]}): "
                  f"{movie["details"]["rating"]}")


def filter_movies(movies: list, current_user: str) -> None:
    """
    Filters out movies as per parameters given by user and prints the result.
    :param movies: list of all movies.
    :param current_user: str containing the current username.
    :return: None
    """
    print(title("Filter Movies") + ":")
    min_rating = prompt_min_rating()
    min_year = prompt_min_year()
    max_year = prompt_max_year()
    print(title("\n" + f"{current_user}'s Filtered Movies") + ":")
    for movie in movies:
        if (movie["details"]["rating"] >= min_rating and
                min_year <= movie["details"]["year"] <= max_year):
            print(f">>> {movie["title"]} ({movie["details"]["year"]}): "
                  f"{movie["details"]["rating"]}")


def generate_website(movies: list, current_user: str) -> None:
    """
    Coordinates the generation of the HTML frontend for the current user.
    :param current_user: str containing the current username.
    :param movies: list of all movies.
    :return: None
    """
    movies_cards = get_movies_cards(movies)
    template_path = os.path.join("static", "index_template.html")
    page_template = open_template(template_path)
    final_page = inject_website_content(page_template, movies_cards)
    build_html_page(final_page, current_user)

    print(success(f"{current_user}'s Website successfully generated"))


def create_ratings_histogram(movies: list, current_user: str) -> None:
    """
    Creates, saves, and displays a histogram of all ratings of movies.
    :param movies: list of all movies.
    :param current_user: str containing the current username.
    :return: None
    """
    data = get_ratings_list(movies)
    plt.hist(data, bins=5, edgecolor="black", color="green", alpha=0.7)
    plt.title("My Movies' Ratings Histogram")
    plt.xlabel("Ratings")
    plt.ylabel("Frequency")
    if not os.path.exists("output"):
        os.makedirs("output")

    file_path = os.path.join("output", f"{current_user}_ratings_histogram.png")
    plt.savefig(file_path)
    plt.show()
    print(success(f"{current_user}'s Movies Ratings Histogram successfully generated"))
