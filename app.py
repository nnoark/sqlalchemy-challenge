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
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
Base = automap_base()
Base.prepare(engine,reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station

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
    session = Session(engine)
   
    #Create a query
    prcp_query = session.query(measurement.date,measurement.prcp).all()
    #Create a dictionary to convert to JSON
    session.close()
    prcp_dict = {}
    for date,prcp in prcp_query:
        prcp_dict[date] = prcp
    return jsonify(prcp_dict)
    
@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    station_query = session.query(station.station,station.name).all()
    station_list = []
    session.close()
    for each in station_query:
        station_dict = {}
        station_dict['station'] = each[0]
        station_dict['name'] = each[1]
        station_list.append(station_dict)
    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    ##From previous analysis, we know the lastest date and most active station
    session = Session(engine)
    data = session.query(measurement.date,measurement.tobs).\
    filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= '2016-08-24').\
        filter(measurement.date <= '2017-08-24').all()
    session.close()
    tobs_list = []
    for i in data:
        tobs_dict = {}
        tobs_dict['date'] = i[0]
        tobs_dict['tobs'] = i[1]
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

    
@app.route('/api/v1.0/<start>')
def start(start):
    session = Session(engine)
    query_result = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).\
       filter(measurement.date >= start).all()
    session.close()
    tobs_list = []
    for min,avg,max in query_result:
        tobs_dict = {}
        tobs_dict['Min'] = min
        tobs_dict['Average'] = avg
        tobs_dict['Max'] = max
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

@app.route('/api/v1.0/<start>/<end>')
def start_end(start,end):
    session = Session(engine)
    query_result = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).\
       filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()
    tobs_list = []
    for min,avg,max in query_result:
        tobs_dict = {}
        tobs_dict['Min'] = min
        tobs_dict['Average'] = avg
        tobs_dict['Max'] = max
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)



if __name__ == '__main__':
    app.run(debug=True)





