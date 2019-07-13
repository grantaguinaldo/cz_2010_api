import numpy as np
import sqlalchemy
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

app = Flask(__name__)

#Connects to the SQL database.
connection_string = 'sqlite:///cz_2010.sqlite'
engine = create_engine(connection_string)
Base = automap_base()
Base.prepare(engine, reflect=True)
cz_2010 = Base.classes.cz_2010_usc
session = Session(engine)


# Checks if the app is running on the server.
@app.route('/is_alive')
def hello_world():
    return 'Yes, I am alive!!!'

# Returns JSON of all station numbers in the database.
@app.route('/api/v1.0/station')
def stations():

    return jsonify(session.query(cz_2010.STATION_NBR).distinct().all())

# Returns JSON of all station names in the database.
@app.route('/api/v1.0/station_names')
def station_names():

    return jsonify(session.query(cz_2010.STATION).distinct().all())


if __name__ == "__main__":
    app.run(debug=True)
