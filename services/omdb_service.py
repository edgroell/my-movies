"""
Module containing all functions related to OMDb API interactions
"""

import os
import requests

from dotenv import load_dotenv

load_dotenv()

class OMDBService:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OMDB_API_KEY")
        if not self.api_key:
            raise ValueError("OMDB_API_KEY not found.")
        self.base_url = "http://www.omdbapi.com/"

    def get_movie_details(self, title=None):
        """ Fetches details for a single movie by title """
        params = {'apikey': self.api_key}
        if title:
            params['t'] = title
        else:
            raise ValueError("Must provide a title to fetch movie details.")

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        movie_data = response.json()
        if movie_data.get("Response") == "True":
            return movie_data
        return None
