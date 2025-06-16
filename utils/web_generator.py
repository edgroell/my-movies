"""
Module that contains all the functions to generate the HTML frontend.
"""

import os

def serialize_movie(movie: dict) -> str:
    """
    Builds the entire string in HTML format for the given movie.

    :param movie: dict containing all data from the given movie.
    :return: str containing all info of the given movie in HTML format.
    """
    title = movie.get("title", "Name not found")
    year = movie["details"].get("year", "Year not found")
    if movie["details"].get("poster") == "N/A":
        poster = None
    else:
        poster = movie["details"].get("poster", "Image not found")

    movie_card = f"""
    <li class="movie">
        <div class="movie-poster" style="background-image: url('{poster}');"></div>
        <div class="movie-title">{title}</div>
        <div class="movie-year">{year}</div>
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


def build_html_page(final_page: str) -> None:
    """
    Builds the final html page containing the movies cards.
    :param final_page: str containing the final page in html format.
    :return: None
    """
    if not os.path.exists("output"):
        os.mkdir("output")

    file_path = os.path.join("output", "index.html")

    with open(file_path, "w", encoding="utf-8") as handle:
        handle.write(final_page)
