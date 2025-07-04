"""
Module that serves as Data Access Layer
"""

from ..services.omdb_service import OMDBService
from .data_models import db, User, Movie
from sqlalchemy.exc import IntegrityError

omdb_service = OMDBService()

class DataManager:
    @staticmethod
    def get_users():
        """Fetches all users. Returns an empty list if none found."""
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        """Fetches a user by ID. Returns None if not found."""
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_username(username):
        """Fetches a user by username. Returns None if not found."""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def create_user(username):
        """
        Creates a new user.
        Raises IntegrityError if username already exists (due to unique constraint).
        Returns the new User object on success.
        """
        try:
            new_user = User(username=username)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except IntegrityError:
            db.session.rollback()
            raise ValueError(
                f"Username '{username}' already exists, pick another!")
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(
                f"Failed to create user due to a database hiccup: {e}")

    def update_user(self, user_id, new_username=None):
        """
        Updates a user's attributes.
        Returns the updated User object, or None if user not found.
        Raises IntegrityError if new_username already exists.
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        if new_username is not None and new_username != user.username:
            existing_user_with_new_name = self.get_user_by_username(new_username)
            if existing_user_with_new_name and existing_user_with_new_name.id != user_id:
                raise ValueError(f"Cannot update: Username '{new_username}' is already taken.")

            user.username = new_username

        try:
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Failed to update user {user_id}: {e}")


    def delete_user(self, user_id):
        """
        Deletes a user by ID.
        Returns True on success, False if user not found.
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return False

        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Failed to delete user {user_id}: {e}")


    @staticmethod
    def get_movies(user_id):
        """Fetches all movies for a given user. Returns an empty list if none found."""
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, user_id, movie):
        """
        Adds a new movie by fetching all data from the OMDb API.
        Returns the new Movie object on success.
        """
        try:
            if not self.get_user_by_id(user_id):
                raise ValueError(f"User with ID {user_id} does not exist. No movie for ghosts!")

            new_movie_data = omdb_service.get_movie_details(movie)
            if new_movie_data:
                new_movie = Movie(
                    user_id=user_id,
                    title=new_movie_data['Title'],
                    year=new_movie_data['Year'],
                    rating=new_movie_data['imdbRating'],
                    country=new_movie_data['Country'],
                    poster_url=new_movie_data['Poster'],
                    imdb_id=new_movie_data['imdbID'],
                    note='N/A')
                db.session.add(new_movie)
                db.session.commit()
                return new_movie
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Failed to add movie: {e}")


    @staticmethod
    def update_movie(movie_id, **kwargs):
        """
        Updates a movie's attributes.
        Returns the updated Movie object, or None if movie not found.
        """
        movie = Movie.query.get(movie_id)
        if not movie:
            return None

        for key, value in kwargs.items():
            if hasattr(movie, key):
                setattr(movie, key, value)
            else:
                print(f"Warning: Attempted to update non-existent attribute '{key}' for Movie ID {movie_id}")

        try:
            db.session.commit()
            return movie
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Failed to update movie {movie_id}: {e}")

    @staticmethod
    def delete_movie(movie_id):
        """
        Deletes a movie by ID.
        Returns True on success, False if movie not found.
        """
        movie = Movie.query.get(movie_id)
        if not movie:
            return False

        try:
            db.session.delete(movie)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Failed to delete movie {movie_id}: {e}")
