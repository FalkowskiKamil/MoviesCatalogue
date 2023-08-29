# Flask Movie App with Docker Integration

This is a Flask application that fetch movie data from TMDB (The Movie Database) API. The application provides various functionalities related to movies, including fetching popular movies, searching for movies, retrieving movie details, displaying movie posters, and more.

## Overview
[You can have an overview of the functionality of the app on Replit](https://replit.com/@KamilFalkowski/TMDBFlask)


## Technology Stack

TMDB is built using the following technologies:

- Framework: Flask
- Handling forms and form validation: Flask WTF
- Database: TMDB
- Testing: Pytest, Selenium
- Deployment and Management: Docker, Kubernetes

## Installation

Option 1:
   1. Clone the repository.
   2. Install the necessary dependencies using the command 'pip install -r requirements.txt.'
   3. Start the application by running the command 'flask run' in the application folder.
   4. Open your browser and go to [http://localhost:5000/](http://localhost:5000/)
   
Option 2:
   1. Clone the Docker image using the command: 'docker pull falkowskikamil/tmdb_flask:tmdb' Make sure Docker is installed.
   2. Run container, using host Ports "5000"
   3. Open your browser and go to [http://localhost:5000/](http://localhost:5000/)

## Contribution

Contributions to TMDB_flask are welcome! If you have any ideas or improvements, feel free to submit a pull request.
