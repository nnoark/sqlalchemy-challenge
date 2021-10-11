from flask import Flask, jsonify
from flask.wrappers import Request
import numpy as np
import datetime as dt


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from sqlalchemy import create_engine, func
from config import username,password

###Setup of the database
engine = create_engine(f'postgresql://{username}:{password}@localhost:5432/hawaii')
Base = automap_base()
Base.prepare(engine,reflect=True)
measurement = Base.classes.measurements
station = Base.classes.stations
session = Session(engine)

###Setup of Flask
app = Flask(__name__)

###Flask routes
@app.route('/')
def home():
    return (
        f'Welcome to my Weather API<br/>'
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end>'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    #Create a session
   
    #Create a query
    prcp_query = session.query(measurement.date,measurement.prcp).all()
    #Create a dictionary to convert to JSON
    prcp_dict = {}
    for date,prcp in prcp_query:
        prcp_dict[date] = prcp
    return jsonify(prcp_dict)
    session.close()
@app.route('/api/v1.0/stations')
def stations():
    station_query = session.query(station.station,station.name).all()
    station_list = []
    for each in station_query:
        station_dict = {}
        station_dict['station'] = each[0]
        station_dict['name'] = each[1]
        station_list.append(station_dict)
    return jsonify(station_list)
@app.route('/api/v1.0/tobs')
def tobs():
    ##From previous analysis, we know the lastest date and most active station
    data = session.query(measurement.date,measurement.tobs).\
    filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= '2016-08-24').\
        filter(measurement.date <= '2017-08-24').all()
    tobs_list = []
    for i in data:
        tobs_dict = {}
        tobs_dict['date'] = i[0]
        tobs_dict['tobs'] = i[1]
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)
##Create a calc_temps function
def calc_temps(start_date, end_date):
  
    session = Session(engine)

    return (
        session.query(
            func.min(measurement.tobs),
            func.avg(measurement.tobs),
            func.max(measurement.tobs),
        )
        .filter(measurement.date >= start_date)
        .filter(measurement.date <= end_date)
        .all()
    )
@app.route('/api/v1.0/<start>')
def start(start):
    temps = calc_temps(start,'2017-08-24')
    temp_list = []
    date_dict = {start,'2017-08-24'}
    temp_list.append(date_dict)
    temp_list.append(temps[0][0])
    temp_list.append(temps[0][1])
    temp_list.append(temps[0][2])
    return jsonify(temp_list)
    
@app.route('/api/v1.0/<start>/<end>')
def start_end():
    start = Request.args.get("Start Date")
    end = Request.args.get("End Date")
    temps = calc_temps(start,end)
    temp_list = []
    date_dict = {start,'2017-08-24'}
    temp_list.append(date_dict)
    temp_list.append(temps[0][0])
    temp_list.append(temps[0][1])
    temp_list.append(temps[0][2])
    return jsonify(temp_list)




if __name__ == '__main__':
    app.run(debug=True)
session.close()




