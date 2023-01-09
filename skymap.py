import json
import os
import datetime as datetime
import numpy as np
import pytz
import skyfield.api
from geopy import Nominatim
from matplotlib.patches import Circle
from tzwhere import tzwhere
from pytz import timezone, utc
import matplotlib.pyplot as plt
from matplotlib import *
from skyfield.api import Star, load, wgs84, load_constellation_map, position_of_radec, load_constellation_names
from skyfield.data import hipparcos, stellarium
from skyfield.projections import build_stereographic_projection
import location
import pandas

eph = load('de421.bsp')

with load.open(hipparcos.URL) as f:
    stars = hipparcos.load_dataframe(f)

location.LocationApi.get_location()
with open(os.path.relpath("loc.json")) as loc_file:
    loc = json.load(loc_file)
    lat = loc["results"][1]['geometry']['location']['lat']
    lon = loc["results"][1]['geometry']['location']['lng']

utc_dt = datetime.datetime.now(tz=pytz.UTC)
t = load.timescale().utc(utc_dt)

observer = wgs84.latlon(latitude_degrees=lat, longitude_degrees=lon).at(t)
position = observer.from_altaz(alt_degrees=90, az_degrees=0)

ra, dec, distance = observer.radec()
center_object = Star(ra=ra, dec=dec)
earth = eph['earth']
sun = eph['sun']
mars = eph['mars']
uranus = eph['URANUS BARYCENTER']
moon = eph['moon']

center = earth.at(t).observe(center_object)
projection = build_stereographic_projection(center)
field_of_view_degrees = 180.0

mars_position = earth.at(t).observe(mars)
mars_x, mars_y = projection(mars_position)
uranus_position = earth.at(t).observe(uranus)
uranus_x, uranus_y = projection(uranus_position)
moon_position = earth.at(t).observe(moon)
moon_x, moon_y = projection(moon_position)
sun_position = earth.at(t).observe(sun)
sun_x, sun_y = projection(sun_position)

chart_size = 10
fig, ax = plt.subplots(figsize=(chart_size, chart_size))

star_positions = earth.at(t).observe(Star.from_dataframe(stars))
stars['x'], stars['y'] = projection(star_positions)

chart_size = 10
max_star_size = 50
limiting_magnitude = 10

bright_stars = (stars.magnitude <= limiting_magnitude)
magnitude = stars['magnitude'][bright_stars]

marker_size = max_star_size * 10 ** (magnitude / -2.5)

scatter = ax.scatter(stars['x'][bright_stars], stars['y'][bright_stars],
 s=marker_size, color='white', marker='.', linewidths=0,
 zorder=2)

border = plt.Circle((0, 0), 1, color='black', fill=True)
ax.add_patch(border)

ax.scatter(mars_x, mars_y,
           s=200, color='red', marker='.', linewidths=0,
           zorder=2)

ax.scatter(uranus_x, uranus_y,
           s=200, color='blue', marker='.', linewidths=0,
           zorder=2)

ax.scatter(moon_x, moon_y,
           s=250, color='grey', marker='o', linewidths=0,
           zorder=2)

ax.scatter(sun_x, sun_y,
           s=2000, color='yellow', marker='.', linewidths=0,
           zorder=2)


# sun_light = plt.Circle((sun_x, sun_y), 0.8, color='blue', fill=True)
# ax.add_patch(sun_light)


horizon = Circle((0, 0), radius=1, transform=ax.transData)
for col in ax.collections:
    col.set_clip_path(horizon)



# other settings
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
plt.axis('off')
plt.show()