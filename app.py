"""
My Movies app
by Ed Groell
Latest: 04-JUL-2025
"""

import os

from flask import Flask, render_template
from data.data_manager import DataManager
from data.data_models import db, Movie

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'my_movies.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

data_manager = DataManager()


@app.route('/')
def index():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])

@app.route('/users/<int:user_id>/movies', methods=['GET', 'POST'])

@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])

if __name__ == '__main__':
  with app.app_context():
    db.create_all()

  app.run()
