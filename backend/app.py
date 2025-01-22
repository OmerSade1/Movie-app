import os
import logging
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pymysql
from prometheus_flask_exporter import PrometheusMetrics  # Import PrometheusMetrics

app = Flask(__name__)
CORS(app)

# Initialize Prometheus metrics exporter
metrics = PrometheusMetrics(app)

db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Set the URI for SQLAlchemy to connect to MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://omer:{db_password}@db-mysql.cha4akq0c089.us-east-1.rds.amazonaws.com/{db_name}"
db = SQLAlchemy(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Ensure the database and table are created
def create_database_and_table():
    connection = pymysql.connect(
        host='db-mysql.cha4akq0c089.us-east-1.rds.amazonaws.com',
        user='omer',
        password=db_password 
   )
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
            cursor.execute(f"USE {db_name};")
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS movie (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                poster VARCHAR(255) NOT NULL
            );
            ''')
            connection.commit()
            app.logger.info(f"Database {db_name} and table 'movie' created (if they didn't exist).")
    finally:
        connection.close()

# Call the function to create the database and table
create_database_and_table()

# Define Movie model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    poster = db.Column(db.String(255), nullable=False)

# Fetch movies
@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    app.logger.info('Fetched movies: %s', movies)
    return jsonify([{'id': movie.id, 'name': movie.name, 'poster': movie.poster} for movie in movies])

# Add new movie
@app.route('/movies', methods=['POST'])
def add_movie():
    data = request.get_json()
    new_movie = Movie(name=data['name'], poster=data['poster'])
    db.session.add(new_movie)
    try:
        db.session.commit()
        app.logger.info('Added new movie: %s', new_movie)
        return '', 201
    except Exception as e:
        return str(e), 500

# Delete a movie by ID
@app.route('/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.query.get(id)
    if movie is None:
        return '', 404
    db.session.delete(movie)
    db.session.commit()
    app.logger.info('Deleted movie: %s', movie)
    return '', 204

# Edit a movie by ID
@app.route('/movies/<int:id>', methods=['PUT'])
def edit_movie(id):
    movie = Movie.query.get(id)
    if movie is None:
        return '', 404

    data = request.get_json()
    movie.name = data['name']
    movie.poster = data['poster']
    try:
        db.session.commit()
        app.logger.info('Updated movie: %s', movie)
        return '', 200
    except Exception as e:
        return str(e), 500

# Prometheus Metrics will be available at /metrics
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



