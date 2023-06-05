# CSGOSkins
Web application displaying information about CSGO skins, using Python, Flask, and PostgreSQL

## Requirements:
Run the code below to install the necessary modules.

>$ pip install -r requirements.txt

## Database init
1. set the database in __init__.py file.
2. run schema.sql, schema_ins.sql, schema_upd.sql, schema_upd_2.sql in your database.

## Running flask
### The python way

$ python3 run.py

### The flask way.

$ export FLASK_APP=run.py

$ export FLASK_DEBUG=1           (Replaces export FLASK_ENV=development)

$ export FLASK_RUN_PORT=5004     (Optional if you want to change port numbe4. Default port is port 5000.)

$ flask run

For Windows you may have to use the SET command instead of EXPORT. Ex set FLASK_APP=run.py; set FLASK_DEBUG=1; flask run. This worked for me. Also remeber to add the path to your postgres bin-directory in order to run (SQL interpreter) and other postgres programs in any shell.