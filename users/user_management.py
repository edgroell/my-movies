"""
Module that contains all the commands functions for the user menu.
"""

from users.user_storage_sql import (
    add_user_to_db,
    delete_user_from_db,
    update_user_from_db, get_users_from_db
)
from utils.helpers import is_already_in_user_database
from utils.text_formatter import TextFormatter
from utils.user_prompts import (
    prompt_user_name,
    prompt_new_user_name
)

title = TextFormatter.title
success = TextFormatter.success
error = TextFormatter.error


def list_users(users: list) -> None:
    """
    Prints the entire list of users.
    :param users: list of all users.
    :return: None
    """
    if len(users) == 0:
        print(title("No User") + ":")

    elif len(users) == 1:
        print(title(f"{len(users)} User") + ":")

    else:
        print(title(f"{len(users)} Users") + ":")

    if len(users) == 0:
        print("It's empty here - Start by adding a user!\n")

    else:
        for user in users:
            print(f">>> {user["name"]}")


def validate_user(users: list) -> str | None:
    """
    Validates the selection of an active user.
    :param users: list of all users.
    :return: user_name: str containing the username.
    """
    print(title("Select User") + ":")
    while True:
        user_name = prompt_user_name()

        if user_name.lower() == "exit":
            print("\n****************************************\n")

            return None

        if is_already_in_user_database(users, user_name):
            print("\n****************************************\n")

            return user_name

        print(error(f"Sorry, user '{user_name}' doesn't exist! Type 'exit' to quit!"))


def add_user(users: list) -> None:
    """
    Adds a user to the user database.
    :param users: list of all users.
    :return: None
    """
    print(title("Add User") + ":")
    user_name = prompt_user_name()

    if is_already_in_user_database(users, user_name):
        print("\n" + error(f"Sorry, the user '{user_name}' already exists!"))
        print("\n****************************************\n")

        return

    if add_user_to_db(user_name):
        print("\n" + success(f"User '{user_name}' successfully added"))
        print("\n****************************************\n")

        return

    print("Sorry, there was a problem adding the user.")
    print("\n****************************************\n")


def delete_user(users: list) -> None:
    """
    Deletes a user from the user database.
    :param users: list of all movies.
    :return: None
    """
    print(title("Delete User") + ":")
    user_name = prompt_user_name()

    if not is_already_in_user_database(users, user_name):
        print("\n" + error(f"Sorry, the user '{user_name}' doesn't exist!"))
        print("\n****************************************\n")

        return

    if delete_user_from_db(user_name):
        print("\n" + success(f"User '{user_name}' successfully deleted"))
        print("\n****************************************\n")

        return

    print("Sorry, there was a problem deleting user.")
    print("\n****************************************\n")


def update_user(users: list) -> None:
    """
    Updates a username in the user database.
    :param users: list of all users.
    :return: None
    """
    print(title("Update User") + ":")
    user_name = prompt_user_name()

    if not is_already_in_user_database(users, user_name):
        print("\n" + error(f"Sorry, the user '{user_name}' doesn't exist!"))
        print("\n****************************************\n")

        return

    new_user_name = prompt_new_user_name(users)

    if update_user_from_db(new_user_name, user_name):
        print("\n" + success(f"User successfully updated to '{new_user_name}'"))
        print("\n****************************************\n")

        return

    print("Sorry, there was a problem updating the user.")
    print("\n****************************************\n")


def get_user_id(current_user: str) -> int | None:
    """
    Gets the user id for a given user.
    :param current_user: str containing the current username.
    :return: user_id: int containing the user id.
    """
    users = get_users_from_db()

    for user in users:
        if user["name"] == current_user:
            user_id = user["id"]
            if user_id:

                return user_id

    return None
