# Import the Flask dependencies
import datetime as dt
import numpy as np
import pandas as pd

# Import SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask dependencies
from flask import Flask, jsonify

# Set Up the Database engine for the Flask application to allow access to the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the existing database into our classes (a new model)
Base = automap_base()

# Add the follwing code to reflect the schema from the tables to our code:
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
# Base.classes.keys()

# Create a variable for each of the classes so that we can reference the table later.
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database with the following code:
# Create our session (link) from Python to the DB
session = Session(engine)

# -----Set Up Flask Application-----

# Create a Flask application called "app."
app = Flask(__name__)

# Define the starting point, aka the root.
@app.route('/')

# Create welcome() function and return statement
def welcome():
    return(
# When creating routes, we follow the naming convention /api/v1.0/ followed by the name of the route.
# This convention signifies that this is version 1 of our application. 
    '''
    Welcome to the Climate Analysis API!<br><br>
    Available Routes:<br>
    /api/v1.0/precipitation<br>
    /api/v1.0/stations<br>
    /api/v1.0/tobs<br>
    /api/v1.0/temp/start/end
    ''')

# When creating a new route, make sure the code is aligned to the left in order to avoid errors.
# Create the precipitation analysis route
@app.route("/api/v1.0/precipitation")

# Create the precipitation() function that calculates the date one year ago from the most recent date in the database.
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # write a query to get the date and precipiation from the pervious year.
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    # Create a dictionary with the date as the key and the precipitation as the value.    
    precip = {date: prcp for date, prcp in precipitation}
    # To do this, we will "jsonify" our dictionary.
    # Jsonify() is a function that converts the dictionary to a JSON file.
    # When we are done modifying that data, we can push the data back to a web interface, like Flask.
    return jsonify(precip)

# Create the stations route
@app.route("/api/v1.0/stations")

# Create a new function called stations().
def stations():
    # create a query that will allow us to get all of the stations in our database.
    results = session.query(Station.station).all()
    # We want to start by unraveling our results into a one-dimensional array.
    # To do this, we want to use thefunction np.ravel(), with results as our parameter.
    # Next, we will convert our unraveled results into a list.
    # To convert the results to a list, use the list function, and then convert that array into a list.
    stations = list(np.ravel(results))
    # Then jsonify the list and return it as JSON.

    return jsonify(stations=stations)

# Create the temperature observations route
@app.route("/api/v1.0/tobs")

# Create a new function called temp_monthly()
def temp_monthly():
    # calculate the date one year ago from the last date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query the primary station for all the temperature observations from the previous year.
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    # unravel the results into a one-dimensional array and convert that array into a list.
    temps = list(np.ravel(results))
    # jsonify our temps list, and then return it.
    return jsonify(temps=temps)


# Create the temerature starts and end route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Create a new function called stats() and add parameters to the functions
def stats(start=None, end=None):
    # create a query to select the minimum, average, and maximum temperatures from our SQLite database
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    # Since we need to determine the starting and ending date, add an if-not statement to our code so we can queery our database using the list.
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)
    # Then, we'll unravel the results into a one-dimensional array and convert them to a list. 
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    # Jsonify our results and return them.
    return jsonify(temps=temps)








# ----- Set Up Flask Test and Notes-----

# Create a New Flash App Instance
# app = Flask(__name__)

# Define the starting point, aka the root.
# @app.route('/')

# Create a function, aka route
# def hello_world():
#     return 'Hello world'


# Notice the __name__ variable in this code.
# This is a special type of variable in Python.
# Its value depends on where and how the code is run.
# For example, if we wanted to import our app.py file into another Python file named example.py,
# the variable __name__ would be set to example. Here's an example of what that might look like:

# import app

# print("example __name__ = %s", __name__)

# if __name__ == "__main__":
#     print("example is being run directly.")
# else:
#     print("example is being imported")


# However, when we run the script with python app.py,
# the __name__ variable will be set to __main__.
# This indicates that we are not using any other file to run this code.