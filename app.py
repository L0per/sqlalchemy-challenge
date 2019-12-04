# Import dependencies

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

# Database setup
engine = create_engine("sqlite:///Data/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

# Save references to tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask setup
app = Flask(__name__)

###########################
# Flask Routes
###########################

# Homepage
@app.route("/")
def homepage():
    return (
        """
        <h1>Available Routes:</h1>
        Precipitation data for last year of data:<br/>
        <a href="http://127.0.0.1:5000/api/v1.0/precipitation">/api/v1.0/precipitation</a><br/>
        <br/>
        List of stations:<br/>
        <a href="http://127.0.0.1:5000/api/v1.0/stations">/api/v1.0/stations</a><br/>
        <br/>
        Last year of temperature data from station USC00519281:<br/>
        <a href="http://127.0.0.1:5000/api/v1.0/tobs">/api/v1.0/tobs</a><br/>
        <br/>
        Return minimum, average, and maximum tempuratures for the input date(s):<br/>
        /api/v1.0/STARTDATE<br/>
        /api/v1.0/STARTDATE/ENDDATE
        """
    )

# Precipitation; return last year of precipitation data as a dictionary by JSON
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create session link
    session = Session(engine)

    # Get last date, find first date by subtracting a year
    last_date = str(session.query(Measurement.date).order_by(Measurement.date.desc()).first())
    first_date = dt.datetime.strptime(last_date, "('%Y-%m-%d',)") - dt.timedelta(days=366)

    # Query last year of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= first_date).\
        order_by(Measurement.date.asc()).all()

    # Close session link
    session.close()

    # Create dictionary containing date as key and prcp as value
    date_prec_dict = {}
    for date, prcp in results:
        date_prec_dict[date] = prcp

    return jsonify(date_prec_dict)

if __name__ == '__main__':
    app.run(debug=True)
