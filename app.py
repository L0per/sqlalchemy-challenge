###########################
# Dependencies
###########################

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

###########################
# Database and Flask Setup
###########################

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
        List of stations, associated station id, and their number of datapoints:<br/>
        <a href="http://127.0.0.1:5000/api/v1.0/stations">/api/v1.0/stations</a><br/>
        <br/>
        Last year of temperature data from Waihee station USC00519281:<br/>
        <a href="http://127.0.0.1:5000/api/v1.0/tobs">/api/v1.0/tobs</a><br/>
        <br/>
        Return minimum, average, and maximum tempuratures for the input date(s):<br/>
        /api/v1.0/YYYY-MM-DD<br/>
        /api/v1.0/YYYY-MM-DD(start)/YYYY-MM-DD(end)
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


# Return list of stations by station name, id, and activity
@app.route("/api/v1.0/stations")
def stations():

    # Create session link
    session = Session(engine)

    # Query stations and their activity
    results = session.query(Station.name, Measurement.station, func.count(Measurement.station)).\
        filter(Station.station == Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()

    # Close session link
    session.close()

    return jsonify(results)


# Return list of temp observations from station USC00519281
@app.route('/api/v1.0/tobs')
def tobs():

    # Create session link
    session = Session(engine)

    # Get last date, find first date by subtracting a year
    last_date = str(session.query(Measurement.date).order_by(Measurement.date.desc()).first())
    first_date = dt.datetime.strptime(last_date, "('%Y-%m-%d',)") - dt.timedelta(days=366)

    # Create query for last 12 months of temperature data for station USC00519281
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= first_date).\
        filter_by(station='USC00519281').all()

    # Close session link
    session.close()

    return jsonify(results)


# Return temperature min, max, and avg based on inputed start date
@app.route("/api/v1.0/<start>")
def start(start):

    # Create session link
    session = Session(engine)

    # Convert start input date with datetime and subtract 1 day (>= not working correctly?)
    query_date = dt.datetime.strptime(start, "%Y-%m-%d") - dt.timedelta(days=1)

    # Query minimum, average, and maximum temperature for data between input start date and most recent date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= query_date).all()

    # Close session link
    session.close()

    # Create dictionary containing description of results
    tobs_list = ['Temperature']
    tobs_stats = {}
    for min, avg, max in results:
        tobs_stats['Minimum'] = min
        tobs_stats['Average'] = avg
        tobs_stats['Maximum'] = max
        tobs_list.append(tobs_stats)

    return jsonify(tobs_list)


# Return temperature min, max, and avg based on inputed start and end dates
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):

    # Create session link
    session = Session(engine)

    # Convert start input date with datetime and subtract 1 day (>= not working correctly?)
    start_date = dt.datetime.strptime(start, "%Y-%m-%d") - dt.timedelta(days=1)
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")

    # Query minimum, average, and maximum temperature for data between input start date and most recent date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()

    # Close session link
    session.close()

    # Create dictionary containing description of results
    tobs_list = ['Temperature']
    tobs_stats = {}
    for min, avg, max in results:
        tobs_stats['Minimum'] = min
        tobs_stats['Average'] = avg
        tobs_stats['Maximum'] = max
        tobs_list.append(tobs_stats)

    return jsonify(tobs_list)


if __name__ == '__main__':
    app.run(debug=True)
