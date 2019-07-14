#import database
#import create_map
import sqlalchemy
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template


app = Flask(__name__)

# Connects to the SQL database.


connection_string = 'sqlite:///cz_2010.sqlite'
engine = create_engine(connection_string)
Base = automap_base()
Base.prepare(engine, reflect=True)
cz_2010 = Base.classes.cz_2010_usc
session = Session(engine)

# Serves up the HTML page in the `templates` folder.


@app.route('/')
def index():

    return render_template('index.html')


# Serves up the map.html page.


@app.route('/map')
def map():

    return render_template('map.html')


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

# Returns a JSON of all of the data from a single station between any two months.


@app.route('/api/v1.0/<station>/<start_date>/<end_date>')
def station_start_end(station, start_date, end_date):

    TEMP = session.query(
        cz_2010.STATION_NBR,
        cz_2010.READ_DT_MON,
        cz_2010.READ_DT_DAY,
        cz_2010.READ_DT_YEAR,
        cz_2010.TEMP_F_0000,
        cz_2010.TEMP_F_0100,
        cz_2010.TEMP_F_0200,
        cz_2010.TEMP_F_0300,
        cz_2010.TEMP_F_0400,
        cz_2010.TEMP_F_0500,
        cz_2010.TEMP_F_0600,
        cz_2010.TEMP_F_0700,
        cz_2010.TEMP_F_0800,
        cz_2010.TEMP_F_0900,
        cz_2010.TEMP_F_1000,
        cz_2010.TEMP_F_1100,
        cz_2010.TEMP_F_1200,
        cz_2010.TEMP_F_1300,
        cz_2010.TEMP_F_1400,
        cz_2010.TEMP_F_1500,
        cz_2010.TEMP_F_1600,
        cz_2010.TEMP_F_1700,
        cz_2010.TEMP_F_1800,
        cz_2010.TEMP_F_1900,
        cz_2010.TEMP_F_2000,
        cz_2010.TEMP_F_2100,
        cz_2010.TEMP_F_2200,
        cz_2010.TEMP_F_2300,
    ).filter((cz_2010.STATION_NBR == station) &
             (cz_2010.READ_DT_MON >= start_date) &
             (cz_2010.READ_DT_MON <= end_date)).all()

    TEMP_DF = pd.DataFrame(TEMP).to_dict()

    return jsonify(TEMP_DF)


if __name__ == "__main__":
    app.run(debug=True)
