import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# print(Base.classes.keys())
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitaion():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    
    measurements = []
    for date, prcp in results:
        measurements.append({date : prcp})

    return jsonify(measurements)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-22').all()

    session.close()

    temp = []
    for date, tobs in results:
        temp.append({date : tobs})

    return jsonify(temp)

@app.route("/api/v1.0/<start>")
def temperature_analysis_by_start_date(start):
    session = Session(engine)
    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date>=start).all()
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date>=start).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date>=start).all()

    session.close()

    temp_min = np.round(min_temp[0], 0)
    temp_max = np.round(max_temp[0], 0)
    temp_avg = np.round(avg_temp[0], 0)
            
    return jsonify(f"Minimum temperature is {temp_min}."
                   f"Maximum temperature is {temp_max}."
                   f"Average temperature is {temp_avg}.")

@app.route("/api/v1.0/<start>/<end>")
def temperature_analysis_by_start_end_date(start,end):
    session = Session(engine)
    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<=end).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<=end).all()

    session.close()

    temp_min = np.round(min_temp[0], 0)
    temp_max = np.round(max_temp[0], 0)
    temp_avg = np.round(avg_temp[0], 0)
            
    return jsonify(f"Minimum temperature is {temp_min}."
                   f"Maximum temperature is {temp_max}."
                   f"Average temperature is {temp_avg}.")

if __name__ == '__main__':
    app.run(debug=True)