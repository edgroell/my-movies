"""
Module that consolidates all the user prompting functions.
"""

from datetime import datetime

from utils.helpers import is_already_in_user_database
from utils.text_formatter import TextFormatter

prompt = TextFormatter.prompt
error = TextFormatter.error


def prompt_user_menu_choice() -> int:
    """
    Prompts the user to enter a user menu choice.
    :return: user_menu_choice: int containing the selected command.
    """
    while True:
        print("\n****************************************")
        user_menu_choice = input(prompt("Enter choice (0-4): ")).strip()
        print("****************************************\n")

        if user_menu_choice.isdigit() and 0 <= int(user_menu_choice) <= 4:

            return int(user_menu_choice)

        print(error("Please enter a number between 0 and 4!"))


def prompt_user_name():
    """
    Prompts the user to enter a username.
    :return: user_name: string containing the selected username.
    """
    while True:
        user_name = input(prompt("Enter a Username: ")).strip()

        if user_name:

            return user_name

        print(error("Please enter a username!"))


def prompt_new_user_name(users: list):
    """
    Prompts the user to enter a new username.
    :param users: list of all the users.
    :return: new_user_name: string containing the selected username.
    """
    while True:
        new_user_name = input(prompt("Enter NEW Username: ")).strip()

        if is_already_in_user_database(users, new_user_name):
            print(error(f"Sorry, the user '{new_user_name}' already exists!"))

        else:
            if new_user_name:

                return new_user_name


def prompt_main_menu_choice() -> int:
    """
    Prompts the user to enter a main menu choice.
    :return: main_menu_choice: int containing the selected command.
    """
    while True:
        print("\n****************************************")
        main_menu_choice = input(prompt("Enter choice (0-13): ")).strip()
        print("****************************************\n")

        if main_menu_choice.isdigit() and 0 <= int(main_menu_choice) <= 13:

            return int(main_menu_choice)

        print(error("Please enter a number between 0 and 12!"))


def prompt_press_enter() -> None:
    """
    Prompts the user to press enter before continuing.
    :return: None
    """
    print("\n****************************************")
    input(prompt("Press Enter ⏎ to continue... "))
    print("****************************************\n")


def prompt_movie_name() -> str:
    """
    Prompts the user to enter a movie title.
    :return: movie_name: str containing the movie title given by the user.
    """
    while True:
        movie_name = input(prompt("Enter movie name: ")).strip()

        if movie_name:

            return movie_name

        print("\n" + error("Please enter a movie name!\n"))


def prompt_movie_note() -> str:
    """
    Prompts the user to enter a new note on the given movie.
    :return: new_note: str containing the movie note.
    """
    movie_note = input(prompt("Enter movie note: ")).strip()

    return movie_note


def prompt_whether_movie_note() -> str:
    """
    Prompts whether the user wants to add a note for the added movie.
    :return: movie_note: str containing the movie note.
    """
    while True:
        note_choice = input(prompt("Do you want to add a note (y/n): ")).strip().lower()

        if note_choice == "y":
            movie_note = prompt_movie_note()

            return movie_note

        if note_choice == "n":

            return "N/A"

        print(error("Please enter a valid answer (y/n)!"))


# def prompt_movie_rating() -> float:
#     """
#     Prompts the user to enter a movie rating.
#     :return: movie_rating: float containing the movie rating given by the user.
#     """
#     while True:
#         try:
#             movie_rating = input(prompt("Enter movie rating (0-10): ")).strip()
#             if "," in movie_rating:
#                 movie_rating = movie_rating.replace(",", ".")
#
#             if 0 <= float(movie_rating) <= 10:
#                 return float(movie_rating)
#
#             print(error("\nPlease enter a valid number between 0 and 10!\n"))
#
#         except ValueError:
#             print(error("\nPlease enter a valid number!\n"))


# def prompt_movie_year() -> int:
#     """
#     Prompts the user to enter a movie year of release.
#     :return: movie_year: int containing the movie year of release given by the user.
#     """
#     while True:
#         movie_year = input(prompt("Enter movie year of release: ")).strip()
#         if (movie_year.isdigit() and
#                 len(movie_year) == 4 and
#                 (movie_year.startswith("1") or
#                  movie_year.startswith("2"))):
#
#             return int(movie_year)
#
#         print(error("\nPlease enter a valid year!\n"))


def prompt_sorting_descending() -> bool:
    """
    Prompts the user to decide whether the sorting is descending or ascending.
    :return: bool:
        True if sorting is descending,
        False otherwise.
    """
    while True:
        sorting_choice = input(prompt(
            "Do you want the latest movies first? (y/n): ")).strip().lower()

        if sorting_choice == "y":

            return True

        if sorting_choice == "n":

            return False

        print(error("Please enter a valid answer (y/n)!"))


def prompt_min_rating() -> int | float:
    """
    Prompts the user to enter a minimum rating.
    :return:
        0: int indicating there is no minimum rating.
        min_rating_float: float containing the minimum rating given by the user.
    """
    while True:
        min_rating = input(prompt("Enter minimum rating (leave blank for no min rating): ")).strip()

        if not min_rating:

            return 0

        try:
            if "," in min_rating:
                min_rating = min_rating.replace(",", ".")

            min_rating_float = float(min_rating)

            if 0 <= min_rating_float <= 100:

                return min_rating_float

            print("\n" + error("Please enter a valid number between 0 and 100!\n"))

        except ValueError:
            print("\n" + error("Please enter a valid rating!\n"))


def prompt_min_year() -> int:
    """
    Prompts the user to enter a minimum year of release.
    :return:
        0: int indicating there is no minimum year of release.
        min_year: int containing the minimum year of release given by the user.
    """
    while True:
        min_year = input(prompt("Enter start year (leave blank for no start year): ")).strip()

        if not min_year:

            return 0

        if (min_year.isdigit() and
                len(min_year) == 4 and
                (min_year.startswith("1") or
                 min_year.startswith("2"))):

            return int(min_year)

        print("\n" + error("Please enter a valid year!\n"))


def prompt_max_year() -> int:
    """
    Prompts the user to enter a maximum year of release.
    :return:
        current_year: int indicating there is no maximum year of release.
        max_year: int containing the maximum year of release given by the user.
    """
    while True:
        try:
            max_year = input(prompt("Enter end year (leave blank for no end year): ")).strip()
            current_year = datetime.now().year

            if not max_year:

                return current_year

            if (int(max_year) <= current_year and
                    len(max_year) == 4 and
                    (max_year.startswith("1") or
                     max_year.startswith("2"))):

                return int(max_year)

            print("\n" + error("Please enter a valid year, not in the future!\n"))

        except ValueError:
            print("\n" + error("Please enter a year!\n"))


__all__ = [
    "prompt_user_menu_choice",
    "prompt_user_name",
    "prompt_new_user_name",
    "prompt_main_menu_choice",
    "prompt_press_enter",
    "prompt_movie_name",
    "prompt_movie_note",
    "prompt_whether_movie_note",
    "prompt_sorting_descending",
    "prompt_min_rating",
    "prompt_min_year",
    "prompt_max_year"
]
