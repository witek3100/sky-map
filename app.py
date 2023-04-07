import base64
from flask import Flask, render_template, request
import map
import datetime
from skyfield.api import utc
app = Flask(__name__)


@app.route('/')
def hello_world():
    longtitude = request.args.get('longtitude')
    latitude = request.args.get('latitude')
    date = request.args.get('date')
    time = request.args.get('time')
    if longtitude == None or latitude == None:
        return render_template('main.html', welcome=True)

    try:
        lon = float(longtitude)
        lat = float(latitude)
    except ValueError:
        lon = 0
        lat = 0

    try:
        split_date = date.split('-')
        split_time = time.split(':')
        utc_dt = datetime.datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]), hour=int(split_time[0]), minute=int(split_time[1]), tzinfo=utc)
    except ValueError:
        utc_dt = datetime.datetime.now(tz=utc)

    map_ = map.create_map(lon, lat, utc_dt)
    map_data = base64.b64encode(map_.getbuffer()).decode("ascii")
    time = str(utc_dt.time())
    return render_template('main.html', map=map_data, longtitude=lon, latitude=lat, date=utc_dt.date(), time=time[:5])

if __name__ == '__main__':
    app.run(debug=True)