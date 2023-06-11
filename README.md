## CSGOSkins
Web application displaying information about CSGO skins, using Python, Flask, and PostgreSQL

## Requirements:
Run the code below to install the necessary modules.

>$ pip install -r requirements.txt

## Database init
1. set the database in __init__.py file.
2. run schema.sql in your database.

## Running the web-app

$ export FLASK_APP=app.py
OR
$ set FLASK_APP=app.py

$ export FLASK_DEBUG=1           (Replaces export FLASK_ENV=development)
OR
$ set FLASK_DEBUG=1

$ export FLASK_RUN_PORT=5432     (Optional if you want to change port numbe4. Default port is port 5000.)
OR
$ set FLASK_RUN_PORT=5432

$ flask run

Remeber to add the path to your postgres bin-directory in order to run (SQL interpreter) and other postgres programs in any shell.

## The Web-App
The interface is pretty straight-forward. You can login or sign-up to view the market (Customer user ID's are between 1 and 999, while employee user ID's are between 1000 and 1999). Employees can add funds to any account that is registered in the database (customers and employees), while customers cannot add funds. The market tab displays all items in the database with their price and quality. The home tab displays 10 random items, the account tab displays information about the user currently logged in, the inventory tab displays items in a certain inventory (currently not able to add items to inventories - except manually), and lastly, the about page displays the authors' names.