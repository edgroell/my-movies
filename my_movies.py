"""
# My Movies
# by Ed Groell
# last update: 16-JUN-2025
"""

from data.movie_storage_sql import get_movies_from_db
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
from utils.text_formatter import TextFormatter
from utils.user_prompts import (
    prompt_menu_choice,
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


def dispatch_menu() -> None:
    """ Coordinates the different commands available from the CLI """
    menu = {
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
        12: ("12. Create Ratings Histogram", create_ratings_histogram)
    }

    while True:
        print(title("Menu"))
        for command in menu.values():
            print(command[0])

        menu_choice = prompt_menu_choice()

        if menu_choice == 0:
            print("Bye for now & have a nice day!")

            break

        movies = get_movies_from_db()
        command = menu.get(menu_choice)
        if command and command[1]:
            command[1](movies)

        prompt_press_enter()


def main():
    """ Initiates the my-movies program """
    display_header()
    # Displays and handles the CLI interface
    dispatch_menu()


if __name__ == "__main__":
    main()
