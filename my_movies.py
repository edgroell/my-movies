# @Author: VU Anh Tuan
# @Date:   2024-03-22 06:17:07
# @Last Modified by:   VU Anh Tuan
# @Last Modified time: 2024-10-09 17:40:31


"""
This program
"""


import statistics
import random
import Levenshtein
import matplotlib.pyplot


def display_menu(formatting):

    # Function that prints all options and redirects to the corresponding function
    print()
    print(
        f"{formatting['bold']}{formatting['underline']}Menu{formatting['reset']}:\n"
        '1. List movies\n'
        '2. Add movie\n'
        '3. Delete movie\n'
        '4. Update movie\n'
        '5. Stats\n'
        '6. Random movie\n'
        '7. Search movie\n'
        '8. Movies sorted by rating\n'
        '9. Create Rating Histogram\n'
    )


def list_movies(movies: dict, formatting):

    # Function that prints the list of all movies currently available in the dictionary
    print(f"{formatting['bold']}{formatting['underline']}{len(movies.keys())} movies in total{formatting['reset']}:")

    for movie, rating in movies.items():
        print(f"{movie}: {rating}")

    print()


def add_movie(movies: dict, formatting):

    # Function that prompts the user to add a new movie and its rating into the dictionary
    new_movie_name = input(f"{formatting['bold']}{formatting['blue']}Enter new movie name: {formatting['reset']}")

    # Checking if the movie is already in the dictionary
    for movie in movies.keys():

        if new_movie_name.lower() == movie.lower():
            print(f"{formatting['bold']}{formatting['red']}Sorry, this movie is already in the database!{formatting['reset']}")
            print()

            # For UX purpose, prompting the user if they simply want to update the rating of the movie they entered
            prompt_rating_update = input(f"{formatting['bold']}{formatting['blue']}Do you wish to update the rating of the movie {movie}? (Y/N) {formatting['reset']}")

            if prompt_rating_update.lower() == 'y':
                new_rating = input(f"{formatting['bold']}{formatting['blue']}Enter new movie rating (0-10): {formatting['reset']}")

                # In case the user has a European keyboard and prints a comma instead of a point
                if ',' in new_rating:
                    corrected_new_rating = new_rating.replace(',', '.')
                    movies[movie] = float(corrected_new_rating)
                    print()
                    print(f"{formatting['bold']}{formatting['green']}Movie {formatting['underline']}{movie}{formatting['reset']} {formatting['bold']}{formatting['green']}successfully updated{formatting['reset']}")
                    print()
                    return

                movies[new_movie_name] = float(new_rating)
                print()
                print(f"{formatting['bold']}{formatting['green']}Movie {formatting['underline']}{movie}{formatting['reset']} {formatting['bold']}{formatting['green']}successfully updated{formatting['reset']}")
                print()
                return

            elif prompt_rating_update.lower() == 'n':
                print(f"{formatting['bold']}{formatting['green']}Let's get you back to the main menu!{formatting['reset']}")
                print()
                return

            print(f"{formatting['bold']}{formatting['red']}Sorry, this choice is not valid -- Let's get you back to the main menu!{formatting['reset']}")
            print()
            return

    new_movie_rating = input(f"{formatting['bold']}{formatting['blue']}Enter new movie rating (0-10): {formatting['reset']}")

    # In case the user has a European keyboard and prints a comma instead of a point
    if ',' in new_movie_rating:
        corrected_new_movie_rating = new_movie_rating.replace(',', '.')
        movies[new_movie_name] = float(corrected_new_movie_rating)

    else:
        movies[new_movie_name] = float(new_movie_rating)

    print()
    print(f"{formatting['bold']}{formatting['green']}Movie {formatting['underline']}{new_movie_name}{formatting['reset']} {formatting['bold']}{formatting['green']}successfully added{formatting['reset']}")
    print()


def delete_movie(movies, formatting):

    # Function that will delete the movie entered by user
    movie_to_delete = input(f"{formatting['bold']}{formatting['blue']}Enter movie name to delete: {formatting['reset']}")
    print()

    # Checks if the movie actually is in the dictionary
    for _ in movies.keys():

        if movie_to_delete in movies.keys():
            del movies[movie_to_delete]
            print(f"{formatting['bold']}{formatting['green']}Movie {formatting['underline']}{movie_to_delete}{formatting['reset']} {formatting['bold']}{formatting['green']}successfully deleted{formatting['reset']}")
            break

        print(f"{formatting['bold']}{formatting['red']}Movie {formatting['underline']}{movie_to_delete}{formatting['reset']} {formatting['bold']}{formatting['red']}doesn't exist!{formatting['reset']}")
        break

    print()


def update_movie(movies, formatting):

    # Function that allows user to update the rating of the movie they enter
    movie_to_update = input(f"{formatting['bold']}{formatting['blue']}Enter movie name: {formatting['reset']}")
    print()

    # Checks if the movie actually is in the dictionary
    for _ in movies.items():

        if movie_to_update not in movies.keys():
            print(f"{formatting['bold']}{formatting['red']}Movie {formatting['underline']}{movie_to_update}{formatting['reset']} {formatting['bold']}{formatting['red']}doesn't exist!{formatting['reset']}")
            break

        new_rating = input(f"{formatting['bold']}{formatting['blue']}Enter new movie rating (0-10): {formatting['reset']}")

        # In case the user has a European keyboard and prints a comma instead of a point
        if ',' in new_rating:
            corrected_new_rating = new_rating.replace(',', '.')
            movies[movie_to_update] = float(corrected_new_rating)
            print()
            print(f"{formatting['bold']}{formatting['green']}Movie {formatting['underline']}{movie_to_update}{formatting['reset']} {formatting['bold']}{formatting['green']}successfully updated{formatting['reset']}")
            break

        movies[movie_to_update] = float(new_rating)
        print()
        print(f"{formatting['bold']}{formatting['green']}Movie {formatting['underline']}{movie_to_update}{formatting['reset']} {formatting['bold']}{formatting['green']}successfully updated{formatting['reset']}")
        break

    print()


def get_best_movie(movies):

    # Function that extracts the most highly-rated movie in the dictionary
    best_movie = max(movies.values())
    best_movies = {}

    for movie, rating in movies.items():

        if movies[movie] == best_movie:
            best_movies[movie] = rating

    for movie, rating in best_movies.items():
        print(f"{movie}, {rating}", end='    ')


def get_worst_movie(movies):

    # Function that extracts the least highly-rated movie in the dictionary
    worst_movie = min(movies.values())
    worst_movies = {}

    for movie, rating in movies.items():

        if movies[movie] == worst_movie:
            worst_movies[movie] = rating

    for movie, rating in worst_movies.items():
        print(f"{movie}, {rating}", end='    ')


def list_stats(movies):

    # Function that displays some key statisctics about the movies from the dictionary
    average_rating = round(statistics.mean(movies.values()), 2)
    median_rating = round(statistics.median(movies.values()), 2)
    print('Average rating:', average_rating)
    print('Median rating:', median_rating)
    print(f"Best movie: ", end='')
    get_best_movie(movies)
    print()
    print(f"Worst movie: ", end='')
    get_worst_movie(movies)
    print()
    print()


def get_random_movie(movies):

    # Function that allows the user to randomly select a movie from the dictionary
    movie, rating = random.choice(list(movies.items()))
    print(f"Your movie for tonight: {movie}, it's rated {rating}")
    print()


def search_edit_distance(movie_to_search, movie):
    # Function that looks for potential typos via edit distance
    edit_distance = Levenshtein.distance(movie_to_search, movie)
    return edit_distance


def search_movies_iterations(search_matching: dict, movies: dict):
    # Function that looks for potential movie prequels or sequels (called 'iterations')
    iterations_matching = {}
    for corrected_movie in search_matching.keys():
        for movie, rating in movies.items():
            if corrected_movie.lower() in movie.lower():
                iterations_matching[movie] = rating
    return iterations_matching


def search_movie(movies, formatting):

    # Search engine that searches against the dictionary
    movie_to_search = input(f"{formatting['bold']}{formatting['blue']}Enter part of the movie name: {formatting['reset']}")
    # New dictionary to store potential search results
    search_matching = {}
    print()

    for movie, rating in movies.items():

        # Prints the movie if we have a direct match
        if movie_to_search.lower() == movie.lower():
            print(f"{movie}: {rating}")
            print()
            return_to_menu()

        # Searches for approximate matches
        elif movie_to_search.lower() in movie.lower():
            search_matching[movie] = rating

        else:
            # Calls the Edit Distance function to look for potential typos
            distance = search_edit_distance(movie_to_search.lower(), movie.lower())
            if distance <= 3:
                search_matching[movie] = rating

    if not search_matching:
        # If typo not found, will print a 'no match' message
        print(f"{formatting['bold']}{formatting['red']}Sorry, we can't find any match for {formatting['underline']}{movie_to_search}{formatting['reset']}{formatting['bold']}{formatting['red']}!{formatting['reset']}")

    else:
        # Calls the Movie Iterations function to look for potential movie prequels or sequels (called 'iterations')
        all_iterations = {}
        for corrected_movie, rating in search_matching.items():
            iterations = search_movies_iterations(search_matching, movies)
            all_iterations.update(iterations)

        # Update and print search results
        search_matching.update(all_iterations)

        print(f"{formatting['bold']}{formatting['red']}Movie {formatting['underline']}{movie_to_search}{formatting['reset']} {formatting['bold']}{formatting['red']}doesn't exist!{formatting['reset']} Did you mean:")
        for movie, rating in search_matching.items():
            print(f"{movie}: {rating}")

    print()


def list_movies_sorted_by_rating(movies):

    # Function that sorts the dictionary by values in descending order
    movies_sorted_by_rating = dict(sorted(movies.items(), key=lambda item: item[1], reverse=True))

    for movie, rating in movies_sorted_by_rating.items():
        print(f"{movie}: {rating}")

    print()


def create_rating_histogram(movies, formatting):

    # Function that creates a rating histogram of all movies currently available in the dictionary
    initial_rating = list(movies.values())
    converted_rating = []

    for rating in initial_rating:
        converted_rating.append(float(rating))

    data = converted_rating

    plt = matplotlib.pyplot
    plt.hist(data, bins=5, edgecolor='black', color='green', alpha=0.7)
    plt.title('Movies Rating Histogram')
    plt.xlabel('Rating')
    plt.ylabel('Frequency')

    # Asks the user where to save and then saves the movies rating histogram file
    file_path = input("Where do you want to save the histogram? (e.g., /home/codio/workspace): ")
    plt.savefig(file_path)

    plt.show()
    print(f"{formatting['bold']}{formatting['green']}The Movies Rating Histogram has been successfully saved at {formatting['underline']}{file_path}{formatting['reset']}")
    print()


def main():

    # Dictionary that store the movies and the corresponding rating
    movies = {
        "The Shawshank Redemption": 9.5,
        "Pulp Fiction": 8.8,
        "The Room": 3.6,
        "The Godfather": 9.2,
        "The Godfather: Part II": 9.0,
        "The Dark Knight": 9.0,
        "12 Angry Men": 8.9,
        "Everything Everywhere All At Once": 8.9,
        "Forrest Gump": 8.8,
        "Star Wars: Episode V": 8.7
    }

    # Formatting options for the text
    formatting = {
        "bold": "\033[1m",
        "underline": "\033[4m",
        "white": "\033[37m",
        "red": "\033[31m",
        "green": "\033[32m",
        "blue": "\033[34m",
        "reset": "\033[0m"
    }

    print(f"{formatting['bold']}{formatting['white']}********** {formatting['green']}My Movies Database {formatting['white']}**********{formatting['reset']}")

    while True:
        display_menu(formatting)

        # Menu choice input is not an int in order to allow for Error Message to be displayed
        menu_choice = input(f"{formatting['bold']}{formatting['blue']}Enter choice (1-9): {formatting['reset']}")
        print()

        # Secret command to exit the program (not displayed on the menu!)
        if menu_choice.strip() == 'x':
            print('Goodbye!')
            break

        elif menu_choice.strip() == '1':
            list_movies(movies, formatting)
        elif menu_choice.strip() == '2':
            add_movie(movies, formatting)
        elif menu_choice.strip() == '3':
            delete_movie(movies, formatting)
        elif menu_choice.strip() == '4':
            update_movie(movies, formatting)
        elif menu_choice.strip() == '5':
            list_stats(movies)
        elif menu_choice.strip() == '6':
            get_random_movie(movies)
        elif menu_choice.strip() == '7':
            search_movie(movies, formatting)
        elif menu_choice.strip() == '8':
            list_movies_sorted_by_rating(movies)
        elif menu_choice.strip() == '9':
            create_rating_histogram(movies, formatting)
        else:
            # In case the user types a menu item that is not within range or any other string - not valid!
            print(f"{formatting['bold']}{formatting['red']}Sorry, this choice is not valid -- Please choose between 1 and 9!{formatting['reset']}")
            print()

        # Function that allows always flowing back to the main menu, yet awaits for the user to press Enter
        input(f"{formatting['bold']}{formatting['blue']}Press enter to continue {formatting['reset']}")


if __name__ == "__main__":
    main()