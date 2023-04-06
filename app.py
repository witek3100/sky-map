import base64
from flask import Flask, render_template, request
import map

app = Flask(__name__)


@app.route('/')
def hello_world():
    longtitude = request.args.get('longtitude')
    latitude = request.args.get('latitude')
    map_ = map.create_map(longtitude, latitude)
    map_data = base64.b64encode(map_.getbuffer()).decode("ascii")
    return render_template('main.html', map=map_data)

if __name__ == '__main__':
    app.run(debug=True)