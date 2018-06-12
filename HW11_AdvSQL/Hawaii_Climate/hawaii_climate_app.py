# Use FLASK to create your routes

# Routes

# /api/v1.0/precipitation
# Query for the dates and temperature observations from the last year.
# Convert the query results to a Dictionary using date as the key and tobs as the value.
# Return the json representation of your dictionary.

# /api/v1.0/stations
# Return a json list of stations from the dataset.

# /api/v1.0/tobs
# Return a json list of Temperature Observations (tobs) for the previous year

# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

import datetime as dt
import numpy as np

# import sqlalchemy
import sqlalchemy

# Imports the method used for connecting to DBs
from sqlalchemy import create_engine

# Imports the methods needed to abstract classes into tables
from sqlalchemy.ext.declarative import declarative_base

# Allow us to declare column types
from sqlalchemy import Column, Integer, String, Float, Date


from sqlalchemy.ext.automap import automap_base

from sqlalchemy.orm import Session

from sqlalchemy import create_engine, inspect

from sqlalchemy import func

from flask import Flask, jsonify

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Assign the measurement class to a variable called `Measurement`
Measurement = Base.classes.measurement

# Assign the station class to a variable called `Station`
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Weather !<br/><br/>"
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation - Return the station dates and temperature observations for previous year as json<br/><br/>"
        f"/api/v1.0/stations - Return the list of stations as json<br/><br/>"
        f"/api/v1.0/tobs - Return the Temperature Observations (tobs) for the previous year as json<br/><br/>"
        f"/api/v1.0/calculated_values/start=&ltstart_date&gt&end=&ltend_date&gt - Start and End Date should be YYYY-MM-DD Format \
        Returns minimum temperature, average temperature and max temperature for a given start or start-end range. \
        If no date passed, default to current date <br/><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the station dates and temperature observations for previous year as json"""
    
    # Obtain the current year from the date and using that date determine the previous year appending 01-01 and 12-31
    
    compare_date = dt.date.today()
    start_date = f"{compare_date.year - 1}-01-01"
    end_date = f"{compare_date.year - 1}-12-31"
    precipitation_result = session.query(Measurement).filter((Measurement.date >= start_date) & (Measurement.date <= end_date)
                                      ).order_by(Measurement.date).all()
    
    precipitation = []
    
    for row in precipitation_result:
        precipitation_dict = {}
        precipitation_dict["date"] = row.date
        precipitation_dict["tobs"] = row.tobs
        precipitation.append(precipitation_dict)
       
    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    """Return the list of stations as json"""
    
    station_result = session.query(Station.station).all()
    stations = []
    # Convert list of tuples into normal list
    stations = list(np.ravel(station_result))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return the Temperature Observations (tobs) for the previous year as json"""
    
    # Obtain the current year from the date and using that date determine the previous year appending 01-01 and 12-31
    compare_date = dt.date.today()
    start_date = f"{compare_date.year - 1}-01-01"
    end_date = f"{compare_date.year - 1}-12-31"
    
    tobs_result = session.query(Measurement.tobs).filter((Measurement.date >= start_date) & (Measurement.date <= end_date)
                                      ).order_by(Measurement.date).all()
    
    tobs = []
    tobs = list(np.ravel(tobs_result))
    return jsonify(tobs)


@app.route("/api/v1.0/calculated_values/")
@app.route("/api/v1.0/calculated_values/start=<start_date>")
@app.route("/api/v1.0/calculated_values/start=<start_date>&end=<end_date>")

#deafult value for start and end date = current date

def start_end_date(start_date=dt.date.today().strftime('%Y-%m-%d'),end_date = dt.date.today().strftime('%Y-%m-%d')):
    """Return a json list of minimum temperature, average temperature and max temperature for a given start or start-end range"""

    sel =[func.min(Measurement.tobs),
             func.avg(Measurement.tobs),
             func.max(Measurement.tobs)
             ]
    
    result = session.query(*sel).filter((Measurement.date >= start_date) & (Measurement.date <= end_date)).all()
    
    temperature_values = {}
    calculated_values = []
    
    temperature_values["min_temp"] = result[0][0]
    temperature_values["avg_temp"] = result[0][1]
    temperature_values["max_temp"] = result[0][2]
    calculated_values.append(temperature_values)
           
    return jsonify(calculated_values)

if __name__ == "__main__":
    app.run(debug=True)
