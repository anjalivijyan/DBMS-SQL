# **DBMS - SQL : PORTFOLIO TRACKER**

The Portfolio Tracker is an SQL based financial web application designed to help users manage their stock investments more efficiently. The platform enables users to buy and sell global market indices, track their holdings, manage a watchlist, and gain insights into market performance through analytics.

The platform uses MySQL as the core database system, storing structured data such as user profiles, transaction logs, holdings, watchlists, and historical price data for 8 global indices. The backend is developed using Python (Flask), which processes user requests and handles all the logic, such as handling routes, processing input, and applying trading procedures. The frontend is built with HTML and CSS, providing a user interface for signing up, buying and selling stocks, viewing holdings, and monitoring the market dashboard.

# **Set up instructions for the website :**
This guide will help you set up and run the Portfolio Tracker using Flask and MySQL.

1. Clone or Download the Project Download the project folder containing the following files: • app.py (Flask application code) • connection.py (MySQL connection code) • dbms.env (environment variables) • templates/ (folder for HTML templates) • static/ (folder for CSS)

2. Set Up the MySQL Database in MySQL Workbench 2.1 Create a New Database

* Open MySQL Workbench and log in.
* In the query area, run: CREATE DATABASE portfolio_tracker;
* Click the lightning bolt to execute.

2.2 Run the SQL Files

* Open each file in MySQL Workbench and run them in the following order:
* schema/entities.sql — creates all tables
* schema/seed.sql — inserts sample data for 8 global indices
* schema/triggers.sql — creates the holdings update trigger
* schema/procedures.sql — creates stored procedures for buy, sell, and watchlist

3. Create a dbms.env File

* In the project folder App, create a file named dbms.env and paste the following (replace the placeholder with your actual MySQL password):
* DB_HOST=localhost
* DB_NAME=portfolio_tracker
* DB_USER=root
* DB_PASSWORD=YourPasswordHere
* Make sure to use the correct password for your local MySQL server in DB_PASSWORD.

4. Run the Flask App

4.1 Install Dependencies

* In the terminal, run:
* pip install flask mysql-connector-python python-dotenv bcrypt

4.2 Start the Flask App

* In the terminal, run:
* cd [your project directory]
* Once you are in the correct directory, execute the following command:
* python3 app/app.py

4.3 Visit the Flask App in Your Browser

* Open a browser and visit:
* Homepage: http://127.0.0.1:5000/ — Shows the welcome page with signup and login.
* Signup: http://127.0.0.1:5000/signup — Create a new account.
* Login: http://127.0.0.1:5000/login — Log into your account.
* Dashboard: http://127.0.0.1:5000/dashboard — View market analytics.

# **Troubleshooting**

* MySQL Connection: If there are issues connecting to the database, check if the username, password, and database name in the dbms.env file are correct.
* MySQL Workbench: Make sure you have run all SQL files in the correct order and the tables appear in your database.
* Flask App Not Running: Ensure Flask is installed and there are no errors when starting the app with python3 app/app.py.
