from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# 1. import Flask
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables

Base.prepare(engine, reflect=True)
session = Session(engine)

Measurement = Base.classes.measurement

Station = Base.classes.station

a_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= a_year_ago).all()

station_data = session.query(Station.station).all()

tobs_data = session.query(Measurement.station, Measurement.tobs)\
                .filter(Measurement.station == "USC00519281")\
                .filter(Measurement.date >= a_year_ago).all()


# Save references to each table


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# 3. Define what to do when a user hits the index route
@app.route("/")
def welcome():
    return (f"/api/v1.0/precipitation <br/>"
            f"/api/v1.0/stations <br/>"
            f"/api/v1.0/tobs <br/>"
            f"/api/v1.0/start <br/>"
            f"/api/v1.0/start/end")

@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def station():
    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def temp():
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def temp1(start):
    begin_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                            .filter(Measurement.date >= start).all()
    return jsonify(begin_temp)
@app.route("/api/v1.0/<start>/<end>")
def temp2(start, end):

    begin_end_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                                .filter(Measurement.date >= start)\
                                .filter(Measurement.date <= end).all()
    return jsonify(begin_end_temp)

if __name__ == '__main__':
    app.run(debug=True)
