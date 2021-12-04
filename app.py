import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")

def home():
    return(f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-m-d<br/>"
        f"/api/v1.0/yyyy-m-d/yyyy-m-d")

@app.route("/api/v1.0/precipitation")

def precipitation():
    session = Session(engine)  
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > dt.date(2016,8,23)).all()
    session.close()

    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")

def stations():
    session = Session(engine)  
    results = session.query(Station.station).all()
    session.close()

    station_list = list(np.ravel(results))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")

def tobs():
    session = Session(engine)  
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > dt.date(2016,8,23)).filter(Measurement.station == 'USC00519281').all()
    session.close()

    tobs_list = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["temperature"] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")

def date1(start):

    startAdj = dt.datetime.strptime(start, "%Y-%m-%d").date()

    session = Session(engine)  
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= startAdj).all()
    session.close()

    start_list = []
    for a, b, c in results:
        start_dict = {}
        start_dict["TMIN"] = a
        start_dict["TAVG"] = c
        start_dict["TMAX"] = b
        start_list.append(start_dict)

    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")

def date2(start,end):

    startAdj = dt.datetime.strptime(start, "%Y-%m-%d").date()
    endAdj = dt.datetime.strptime(end, "%Y-%m-%d").date()

    session = Session(engine)  
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= startAdj).filter(Measurement.date <= endAdj).all()
    session.close()

    end_list = []
    for a, b, c in results:
        end_dict = {}
        end_dict["TMIN"] = a
        end_dict["TAVG"] = c
        end_dict["TMAX"] = b
        end_list.append(end_dict)

    return jsonify(end_list)

if __name__ == "__main__":
    app.run(debug = True)