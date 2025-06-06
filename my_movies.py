from utils.text_formatter import TextFormatter
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
    create_ratings_histogram
)
from utils.user_prompts import (
    prompt_menu_choice,
    prompt_press_enter
)

title = TextFormatter.title
success = TextFormatter.success
error = TextFormatter.error


def display_header() -> None:
    """
    Prints the main header of the app.
    :return: None
    """
    print(f"\n***************************************")
    print(f"************   ", end="")
    print(success(f"My Movies"), end="")
    print(f"   ************")
    print(f"***************************************\n")


def load_data() -> list:
    movies = [
        {"The Shawshank Redemption": {"rating": 9.5, "year": 2014}},
        {"Pulp Fiction": {"rating": 8.8, "year": 2008}},
        {"The Room": {"rating": 3.6, "year": 2000}},
        {"The Godfather": {"rating": 9.2, "year": 2012}},
        {"The Godfather: Part II": {"rating": 9.0, "year": 2012}},
        {"The Dark Knight": {"rating": 9.0, "year": 2012}},
        {"12 Angry Men": {"rating": 8.9, "year": 2012}},
        {"Everything Everywhere All At Once": {"rating": 8.9, "year": 2012}},
        {"Forrest Gump": {"rating": 8.8, "year": 2012}},
        {"Star Wars: Episode V": {"rating": 8.7, "year": 2012}}
    ]

    return movies # TODO change data structure


def dispatch_menu(movies: list) -> None:

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
        10: ("10. Filter Movies", search_movie), # TODO update
        11: ("11. Create Ratings Histogram", create_ratings_histogram)
    }

    while True:
        print(title(f"Menu") + ":")
        for command in menu.values():
            print(command[0])

        menu_choice = prompt_menu_choice()

        if menu_choice == 0:
            print("Goodbye!")

            break

        command = menu.get(menu_choice)
        if command and command[1]:
            command[1](movies)

        prompt_press_enter()


def main():
    display_header()
    movies = load_data()
    dispatch_menu(movies)


if __name__ == "__main__":
    main()