"""
Module that contains all the functions to generate the HTML frontend.
"""

import os

from utils.api_calls import get_country_flag
from utils.helpers import get_movie_countries
from utils.config import IMDB_BASE_URL

def serialize_movie(movie: dict) -> str:
    """
    Builds the entire string in HTML format for the given movie.

    :param movie: dict containing all data from the given movie.
    :return: str containing all info of the given movie in HTML format.
    """
    title = movie.get("title", "Name not found")
    year = movie["details"].get("year", "Year not found")
    rating = movie["details"].get("rating", "Rating not found")
    movie_countries = get_movie_countries(movie)
    if movie_countries[0] == "United States":
        flag = get_country_flag("United States of America")
    else:
        flag = get_country_flag(movie_countries[0])

    if movie["details"].get("imdbID") == "N/A":
        link = None
    else:
        link = f"{IMDB_BASE_URL}{movie["details"].get("imdbID")}"

    if movie["details"].get("poster") == "N/A":
        poster = None
    else:
        poster = movie["details"].get("poster")

    if movie["details"].get("note") == "N/A":
        movie_card = f"""
        <li class="movie">
            <a href="{link}" target="_blank" style="text-decoration: none; color: inherit;">
                <div class="movie-poster" style="background-image: url('{poster}');"></div>
                <div class="movie-title">{title}</div>
                <div class="movie-year">{year}</div>
                <div class="movie-rating">{rating}</div>
                <img src="{flag}" alt="Country Flag" class="movie-flag">
            </a>
        </li>
        """
    else:
        note = movie["details"].get("note")
        movie_card = f"""
        <li class="movie">
            <a href="{link}" target="_blank" style="text-decoration: none; color: inherit;">
                <div class="movie-poster" style="background-image: url('{poster}');"></div>
                <div class="movie-title">{title}</div>
                <div class="movie-year">{year}</div>
                <div class="movie-rating">{rating}</div>
                <div class="movie-note">{note}</div>
                <img src="{flag}" alt="Country Flag" class="movie-flag">
            </a>
        </li>
        """

    return movie_card


def get_movies_cards(movies: list) -> str:
    """
    Builds the entire string in html format for all movies.
    :param movies: list containing all info from movies.
    :return: movies_cards: str containing all info of all movies in html format.
    """
    movies_cards = ""

    for movie in movies:
        movies_cards += serialize_movie(movie)

    return movies_cards


def open_template(file_path: str) -> str:
    """
    Reads the content of the html template file.
    :param file_path: str indicating the path to the html template file.
    :return: page_template: str containing all info from the html template file.
    """
    with open(file_path, "r", encoding="utf-8") as handle:
        page_template = handle.read()

        return page_template


def inject_website_content(page_template: str, movies_cards: str) -> str:
    """
    Replaces the placeholder from the html template with data extracted from the database.
    :param page_template: str containing all info from the html template file.
    :param movies_cards: str containing all info from all selected animals in html format.
    :return: final_page: str containing the final page in html format.
    """
    final_page = page_template.replace("__TEMPLATE_MOVIE_GRID__", movies_cards)

    return final_page


def build_html_page(final_page: str, current_user: str) -> None:
    """
    Builds the final html page containing the movies cards.
    :param final_page: str containing the final page in html format.
    :param current_user: str containing the current username.
    :return: None
    """
    if not os.path.exists("output"):
        os.mkdir("output")

    file_path = os.path.join("output", f"{current_user}_website.html")

    with open(file_path, "w", encoding="utf-8") as handle:
        handle.write(final_page)
