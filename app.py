
#import dependencies
import datetime as dt
import numpy as np
import pandas as pd

# Import SQLAlchemy dependencies to access data in SQLite database 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# Import dependency needed for Flask
from flask import Flask, jsonify

# Set up engine to access and query SQLite Database file
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect database into classes 
Base = automap_base()
# use PythonFlask fcn to reflect the tables 
Base.prepare(engine, reflect=True)
# save references to each table and create variable for each of classes to reference later 
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create session link from Python to our database
session = Session(engine)

# Set up Flask 
# define Flask app and call it 'app'
app = Flask(__name__)
# define the welcome route 
@app.route("/")

# Create fcn welcome() with a return statement
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!<br/>
    Available Routes:<br/>
    /api/v1.0/precipitation<br/>
    /api/v1.0/stations<br/>
    /api/v1.0/tobs<br/>
    /api/v1.0/temp/start/end<br/>
    ''')

# Build route for precipitation analysis
@app.route("/api/v1.0/precipitation")

# Create precipitation function 
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Build route for precipitation analysis 
@app.route("/api/v1.0/stations")

# Create stations function 
def stations():
    results = session.query(Station.station).all()
    stations =list(np.ravel(results))
    return jsonify(stations=stations)

# Build route for temperature observations 
@app.route("/api/v1.0/tobs")

# Create temp. observation function
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.date >= prev_year).\
        filter(Measurement.station == 'USC00519281').all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Build route for summary statistics (min,max,avg temp)
# need start date and ending date routes
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Create summary statistics function
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end: 
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)