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
        Available Routes:<br/>
        <br/>
        Precipitation data for last year of data:<br/>
        /api/v1.0/precipitation<br/>
        <br/>
        List of stations:<br/>
        /api/v1.0/stations<br/>
        <br/>
        Last year of temperature data from station USC00519281:<br/>
        /api/v1.0/tobs<br/>
        <br/>
        Return minimum, average, and maximum tempuratures for the input date(s):<br/>
        /api/v1.0/STARTDATE<br/>
        /api/v1.0/STARTDATE/ENDDATE
        """
        # f"Available Routes:<br/>"
        # f"/api/v1.0/precipitation<br/>"
        # f"/api/v1.0/stations<br/>"
        # f"/api/v1.0/tobs<br/>"
        # f"/api/v1.0/<start><br/>"
        # f"/api/v1.0/<start>/<end>"
    )

# Precipitation; return last year of precipitation data as a dictionary by JSON
# Ask TAs whether this should be all precipitation data or just last year
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create session link
    session = Session(engine)

    # Get last date, find first date by subtracting a year
    # not sure why the "u" is required now for the strptime func
    last_date = str(session.query(Measurement.date).order_by(Measurement.date.desc()).first())
    first_date = dt.datetime.strptime(last_date, "(u'%Y-%m-%d',)") - dt.timedelta(days=366)

    # Query last year of precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= first_date).\
        order_by(Measurement.date.asc()).all()


if __name__ == '__main__':
    app.run(debug=True)
