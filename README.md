# MyLib: A home library cataloging web app
#### Video Demo: <url here>
#### App URL: (mylibrarycatalog.herokuapp.com)

MyLib is a home library cataloging web app that can be used to find information about books and create a catalog of books in your home library collection. The app was created using HTML, CSS, and JavaScript for the front end. The back end was created using the Flask framework in Python. Data is stored and retrieved via a PostgreSQL database using FlaskSQLAlchemy.

# App structure
The app is structured as a python package and has been structures to help separate different app functions into different files for convenience and ease of use.

The root directory contains configuration files for Heroku, PIPEnv, and other services. The directory mylib contains the majority of the app files.

Within the root directory two files are of import (create.py and run.py). Create.py is a small script used to easily initialize a database and create the needed tables. Run.py is the driver file which is used to start the application.

The mylib directory acts as a module within the package and contains the majority of the project files.
__init__.py contains codes that initializes the main components of this web app such as the Flask application, database connection, FlaskLogin login manager. This file also sets 	the app into DEV_MODE. Also within this file the app routes from routes.py are imported and the user model needed by Flask_Login. Routes.py is where the app's routes are created. This file creates various routes which serve web pages based on user requests and interact with the database via the database connection created in __init__.py. This file also contains errorhandler routes which handle two specific HTTP errors (404 and 500). Models.py is where the database models are created for the database connection. These models includes a user model, title model, author and publisher models, and a catalog model. These models are used to store, retrieve, update, and delete information from the connected database. Helpers.py contains several helper functions that assist with interfacing with the [Google Books API](https://developers.google.com/books/).

The templates directory contains the HTML templates utilized by the Flask rendering engine. Layout.html is the base template for the web app. Each other template extends layout.html.

The static directory contains three directories: assets, css, and js. Assets contains a few images needed across the web. CSS contains all the CSS files needed across the web app. JS contains all the JavaScript files needed across the web app.

# App logic and design
This app draws from a couple Flask extensions that help streamline the back end functions. [FlaskLogin](https://flasklogin.readthedocs.io/en/latest/) is used to handle user sessions, login in and log out users, and restrict access to logged in views. [FlaskSQLAlchemy](https://flasksqlalchemy.palletsprojects.com/en/2.x/) is used to streamline interactions with the database.

MyLib users are able to register for an account and then sign into their account to view their catalog. The app home page either displays a user's catalog or a message if their catalog is empty. Within the navbar, there is a search bar which allows users to search and retrieve information from Google Books. Within the search results, users can view and read information about books, pick a book format that they own, and add the information as a record to their catalog. Users can also remove records from their catalog on the app home page.

Users are also able to update and view their account information via the account settings page. From this page users can change their username, email, and password. Users can also delete their accounts if they so wish.
