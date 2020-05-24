from flask import Flask, request, g, jsonify
import sqlite3 as lite
import pandas as pd

DATABASE = 'SystemTemp.db'

from system_temp_monitor import getLightData


app = Flask(__name__)
app.config["DEBUG"] == True

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = lite.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET'])
def base(): # Base route - "have it return something"
    return '''<p>Welcome to Facebook</p>'''

@app.route('/light', methods=['GET'])
def light(): # Route for fetching data from light sensor
    light = getLightData()
    return '{}'.format(light)

@app.route('/api', methods=['GET', 'POST'])
def api():
    start = request.args.get('start')
    end = request.args.get('end')

    data = {}
    with app.app_context():
        conn = get_db()
        c = conn.cursor()

        data = pd.read_sql_query('''
            SELECT *
            FROM atable
        ''', conn)

    return jsonify(data)

# create_table()
app.run(port=3000) #address for local server
