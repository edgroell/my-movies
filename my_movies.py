"""
# My Movies
# by Ed Groell
# last update: 17-JUN-2025
"""

from core.features import (
    list_movies,
    add_movie,
    delete_movie,
    update_movie,
    list_stats,
    get_random_movie,
    search_movie,
    list_movies_sorted_by_rating,
    list_movies_sorted_by_year,
    filter_movies,
    generate_website,
    create_ratings_histogram
)
from data.movie_storage_sql import get_movies_from_db
from users.user_management import (
    list_users,
    validate_user,
    add_user,
    delete_user,
    update_user,
    get_user_id
)
from users.user_storage_sql import get_users_from_db
from utils.text_formatter import TextFormatter
from utils.user_prompts import (
    prompt_user_menu_choice,
    prompt_main_menu_choice,
    prompt_press_enter
)

main_title = TextFormatter.main_title
title = TextFormatter.title

def display_header() -> None:
    """
    Prints the main header of the app.
    :return: None
    """
    print("\n****************************************")
    print("********* ", end="")
    print(main_title("My Movies"), end="")
    print(" *********")
    print("****************************************\n")
    print("          Welcome to My Movies")
    print("\n****************************************\n")


def select_user() -> str | bool | None:
    """ Coordinates the different commands available around user management """
    user_menu = {
        0: ("0. Exit", None),
        1: ("1. Select User", validate_user),
        2: ("2. Add User", add_user),
        3: ("3. Delete User", delete_user),
        4: ("4. Update User", update_user)
    }

    while True:
        users = get_users_from_db()
        list_users(users)
        print("\n" + title("User Menu") + ":")
        for command in user_menu.values():
            print(command[0])

        user_choice = prompt_user_menu_choice()

        if user_choice == 0:

            return False

        command = user_menu.get(user_choice)
        if user_choice == 1:
            current_user = command[1](users)
            if current_user is None:
                continue

            if current_user:

                return current_user

        if command and command[1]:
            result = command[1](users)
            if result is not None:

                return result


def dispatch_menu(current_user: str) -> bool | None:
    """ Coordinates the different commands available from the CLI for the current user """
    main_menu = {
        0: ("0. Exit", None),
        1: ("1. List Movies", list_movies),
        2: ("2. Add Movie", add_movie),
        3: ("3. Delete Movie", delete_movie),
        4: ("4. Update Movie", update_movie),
        5: ("5. List Stats", list_stats),
        6: ("6. Random Movie", get_random_movie),
        7: ("7. Search Movie", search_movie),
        8: ("8. Movies Sorted by Rating", list_movies_sorted_by_rating),
        9: ("9. Movies Sorted by Year", list_movies_sorted_by_year),
        10: ("10. Filter Movies", filter_movies),
        11: ("11. Generate Website", generate_website),
        12: ("12. Create Ratings Histogram", create_ratings_histogram),
        13: ("13. Switch User", None)
    }

    while True:
        print(f"Hey {current_user} 👋 What can I do for you today?!")
        print("\n" + title("Main Menu") + ":")
        for key, command in main_menu.items():
            print(command[0])

        menu_choice = prompt_main_menu_choice()

        if menu_choice == 0:

            return False

        if menu_choice == 13:
            new_user = select_user()
            if new_user:
                current_user = new_user
                continue

        user_id = get_user_id(current_user)
        movies = get_movies_from_db(user_id)
        command = main_menu.get(menu_choice)
        if command and command[1]:
            command[1](movies, current_user)

        prompt_press_enter()


def main():
    """ Initiates the My Movies app """
    display_header()
    current_user = select_user()

    while current_user:
        if not dispatch_menu(current_user):

            break

        current_user = select_user()

    print("Bye for now & have a great day! 🚀")


if __name__ == "__main__":
    main()
