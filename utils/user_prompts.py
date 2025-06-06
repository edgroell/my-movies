from utils.text_formatter import TextFormatter


prompt = TextFormatter.prompt
error = TextFormatter.error


def prompt_menu_choice() -> int:
    """
    Prompts the user to enter a menu choice.
    :return: menu_choice: int containing the command to forward to.
    """
    while True:
        print(f"\n***************************************")
        menu_choice = input(prompt(f"Enter choice (0-11): "))
        print(f"***************************************\n")
        if menu_choice.isdigit() and 0 <= int(menu_choice) <= 11:

            return int(menu_choice)

        print(error(f"Please enter a number between 0 and 11!"))


def prompt_press_enter() -> None:
    """
    Prompts the user to press enter before continuing.
    :return: None
    """
    print(f"\n***************************************")
    input(prompt(f"Press enter to continue "))
    print(f"***************************************\n")


def prompt_movie_name() -> str:
    """
    Prompts the user to enter a movie title.
    :return: movie_name: str containing the movie title given by the user.
    """
    movie_name = input(prompt("Enter movie name: ")).strip()

    return movie_name


def prompt_movie_rating() -> float:
    """
    Prompts the user to enter a movie rating.
    :return: movie_rating: float containing the movie rating given by the user.
    """
    while True:
        try:
            movie_rating = input(prompt("Enter movie rating (0-10): ")).strip()
            if "," in movie_rating:
                movie_rating = movie_rating.replace(",", ".")

            if 0 <= float(movie_rating) <= 10:
                return float(movie_rating)

            print(error("\nPlease enter a valid number between 0 and 10!\n"))

        except ValueError:
            print(error("\nPlease enter a valid number!\n"))


def prompt_movie_year() -> int:
    """
    Prompts the user to enter a movie year of release.
    :return: movie_year: int containing the movie year of release given by the user.
    """
    while True:
        movie_year = input(prompt("Enter movie year of release: ")).strip()
        if (movie_year.isdigit() and
                len(movie_year) == 4 and
                (movie_year.startswith("1") or
                 movie_year.startswith("2"))):

            return int(movie_year)

        print(error("\nPlease enter a valid year.\n"))


def prompt_sorting_descending() -> bool:
    """
    Prompts the user to decide whether the sorting is descending or ascending.
    :return: bool:
        True if sorting is descending,
        False otherwise.
    """
    while True:
        sorting_choice = input(prompt("Do you want the latest movies first? (y/n) ")).strip().lower()
        if sorting_choice == "y":

            return True

        if sorting_choice == "n":

            return False

        print(error(f"\nPlease enter a valid answer (y/n)!\n"))


__all__ = [
    "prompt_menu_choice",
    "prompt_press_enter",
    "prompt_movie_name",
    "prompt_movie_rating",
    "prompt_movie_year",
    "prompt_sorting_descending",
]
