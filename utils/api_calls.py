"""
Module containing all functions related to API interactions
"""

import os
import requests

from dotenv import load_dotenv

from utils.config import (
    OMDB_BASE_URL,
    FLAG_BASE_URL
)

load_dotenv()

api_key = os.getenv("API_KEY")


def fetch_movie_data(title: str, plot="short", return_type="json"):
    """
    Fetches movie data from the OMDb API.
    :param: title: str: title of the movie.
    :param: plot: str: plot type of the movie (short or full).
    :param: return_type: str: type of the returned data (json or xml).
    :return:
        movie_data: dict: containing the movie data.
     """
    params = {
        "apikey": api_key,
        "t": title,
        "plot": plot,
        "r": return_type,
    }

    try:
        response = requests.get(OMDB_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        movie_data = response.json()

        return movie_data

    except requests.exceptions.RequestException as e:
        print(f"An error with the API occurred: {e}")

        return None


def get_country_flag(country_name: str) -> str | None:
    """
    Returns the url to the flag of the given country.
    :param country_name: str containing the country name.
    :return:
    """
    url = f"{FLAG_BASE_URL}{country_name}"
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        data = response.json()
        flag = data[0]["flags"]["png"]

        return flag

    return None
