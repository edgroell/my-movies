"""
My Movies app
by Ed Groell
Latest: 04-JUL-2025
"""

import os

from flask import Flask, render_template, request, redirect, url_for, flash
from data.data_manager import DataManager
from data.data_models import db, User, Movie

app = Flask(__name__)

# TODO: Replace this with a strong, random key in production!
app.secret_key = 'a_very_secret_key'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data', 'my_movies.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()


@app.route('/')
def home():
    """
    Fetches all users from the database and renders the index.html template.
    This serves as the main user list page.
    """
    users = data_manager.get_users()

    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    """
    Handles the POST request from the 'Add New User' form.
    Creates a new user, flashes messages, and redirects back to the user list.
    """
    username = request.form.get('username')

    if not username:
        flash('Username cannot be empty!', 'error')
        return redirect(url_for('home'))

    try:
        data_manager.create_user(username)
        flash(f"User '{username}' added successfully!", 'success')
    except ValueError as e:
        flash(f"Error: {e}", 'error')
    except RuntimeError as e:
        flash(f"An unexpected database error occurred: {e}", 'error')
    except Exception as e:
        flash(f"An unknown error occurred: {e}", 'error')

    return redirect(url_for('home'))


@app.route('/users/<int:user_id>/update', methods=['POST'])
def update_user_details(user_id):
    """
    Handles updating a user's username.
    """
    user = data_manager.get_user_by_id(user_id)
    username = user.username
    if not user:
        flash(f"User with ID {user_id} not found!", 'error')
        return redirect(url_for('home'))

    new_username = request.form.get('new_username')
    if not new_username:
        flash('New username cannot be empty!', 'error')
        return redirect(url_for('home'))

    try:
        updated_user = data_manager.update_user(user_id, new_username)
        if updated_user:
            flash(f"User '{username}' updated to '{updated_user.username}' successfully!", 'success')
        else:
            flash(f"Could not update user with ID {user_id}.", 'error')
    except ValueError as e:
        flash(f"Error: {e}", 'error')
    except RuntimeError as e:
        flash(f"An error occurred while updating user: {e}", 'error')
    except Exception as e:
        flash(f"An unknown error occurred: {e}", 'error')

    return redirect(url_for('home'))


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """
    Handles deleting a specific user.
    """
    user = data_manager.get_user_by_id(user_id)
    username = user.username
    try:
        success = data_manager.delete_user(user_id)
        if success:
            flash(f"User {username} deleted successfully!", 'success')
        else:
            flash(f"User with ID {user_id} not found or could not be deleted.", 'error')
    except RuntimeError as e:
        flash(f"An error occurred while deleting user: {e}", 'error')
    except Exception as e:
        flash(f"An unknown error occurred: {e}", 'error')

    return redirect(url_for('home'))


@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])
def user_movies(user_id):
    """
    Handles listing movies for a specific user (GET) and adding a new movie (POST).
    """
    user = data_manager.get_user_by_id(user_id)
    if not user:
        flash(f"User with ID {user_id} not found!", 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        movie_title = request.form.get('movie_title')
        if not movie_title:
            flash('Movie title cannot be empty!', 'error')
            return redirect(url_for('user_movies', user_id=user_id))

        try:
            new_movie = data_manager.add_movie(user_id, movie_title)
            if new_movie:
                flash(f"Movie '{new_movie.title}' added successfully for {user.username}!", 'success')
            else:
                flash(f"Could not find movie '{movie_title}' on OMDb or failed to add.", 'error')
        except ValueError as e:
            flash(f"Error: {e}", 'error')
        except RuntimeError as e:
            flash(f"An unexpected error occurred while adding movie: {e}", 'error')
        except Exception as e:
            flash(f"An unknown error occurred: {e}", 'error')

        return redirect(url_for('user_movies', user_id=user_id))
    else:
        movies = data_manager.get_movies(user_id)
        return render_template('user_movies.html', user=user, movies=movies)


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    """
    Handles updating a specific movie for a user.
    """
    user = data_manager.get_user_by_id(user_id)
    if not user:
        flash(f"User with ID {user_id} not found!", 'error')
        return redirect(url_for('home'))

    # Get updated data from the form (e.g., new_title, new_note)
    new_title = request.form.get('new_title')
    new_note = request.form.get('new_note')

    update_kwargs = {}
    if new_title:
        update_kwargs['title'] = new_title
    if new_note:
        update_kwargs['note'] = new_note

    if not update_kwargs:
        flash("No update data provided!", 'info')
        return redirect(url_for('user_movies', user_id=user_id))

    try:
        updated_movie = data_manager.update_movie(movie_id, **update_kwargs)
        if updated_movie:
            flash(f"Movie '{updated_movie.title}' updated successfully!", 'success')
        else:
            flash(f"Movie with ID {movie_id} not found or could not be updated.", 'error')
    except RuntimeError as e:
        flash(f"An error occurred while updating movie: {e}", 'error')
    except Exception as e:
        flash(f"An unknown error occurred: {e}", 'error')

    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """
    Handles deleting a specific movie for a user.
    """
    user = data_manager.get_user_by_id(user_id)
    if not user:
        flash(f"User with ID {user_id} not found!", 'error')
        return redirect(url_for('home'))

    movie = data_manager.get_movie_by_id(movie_id)
    try:
        success = data_manager.delete_movie(movie_id)
        if success:
            flash(f"Movie {movie.title} deleted successfully!", 'success')
        else:
            flash(f"Movie with ID {movie_id} not found or could not be deleted.", 'error')
    except RuntimeError as e:
        flash(f"An error occurred while deleting movie: {e}", 'error')
    except Exception as e:
        flash(f"An unknown error occurred: {e}", 'error')

    return redirect(url_for('user_movies', user_id=user_id))


# -----------------------------------------------------
# Error Handlers
# -----------------------------------------------------


@app.errorhandler(404)
def page_not_found(e):
    """
    Handles 404 errors (Page Not Found).
    Renders a custom 404 page and returns the 404 status code.
    The 'e' parameter is the error object, which is required by Flask.
    """
    # Note: We are explicitly returning the 404 status code.
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """
    Handles 500 errors (Internal Server Error).
    This is triggered by unhandled exceptions in your code.
    Renders a custom 500 page and returns the 500 status code.
    """
    # It's a good practice to also log the actual error to your console or a file
    # for debugging purposes.
    print(f"An internal server error occurred: {e}")
    return render_template('500.html'), 500


if __name__ == '__main__':
  with app.app_context():
    db.create_all()

  app.run(debug=True) # TODO: Replace this with False once in production!
