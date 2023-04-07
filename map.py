import datetime
import math
from matplotlib.figure import Figure
from skyfield.api import Star, load, wgs84
from skyfield.data import hipparcos
from skyfield.api import utc
from skyfield.projections import build_stereographic_projection
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO


def create_map(lon, lat, time):

    lon = lon
    lat = lat
    time = load.timescale().utc(time)


    ''' configuring plot '''
    fig = Figure(figsize=(10,10), dpi=100, frameon=False)
    ax = fig.subplots(subplot_kw={'projection': 'polar'})
    ax.set_xticks([0, 0.25*math.pi, 0.5*math.pi, 0.75*math.pi, math.pi, 1.25*math.pi, 1.5*math.pi, 1.75*math.pi], ['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE'])
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1], ['','','','',''])
    ax.tick_params(axis='x', colors='white')
    ax.spines['polar'].set_color('white')
    ax.yaxis.grid(False)
    ax.xaxis.grid(False)
    fig.set_facecolor((0,0,0))


    ''' loading astronomical data '''
    eph = load('de421.bsp')
    with load.open('hip_main.dat') as f:
        stars = hipparcos.load_dataframe(f)


    ''' setting observer and objects projection '''
    observer = wgs84.latlon(latitude_degrees=lat, longitude_degrees=lon).at(time)
    ra, dec, distance = observer.radec()
    center_object = Star(ra=ra, dec=dec)
    earth = eph['earth']
    center = earth.at(time).observe(center_object)
    projection = build_stereographic_projection(center)
    cartesian_to_polar =  lambda x, y : (np.arctan2(y, x), np.sqrt(x**2 + y**2))


    ''' stars positions and sizes '''
    star_positions = earth.at(time).observe(Star.from_dataframe(stars))
    stars['x'], stars['y'] = projection(star_positions)
    stars['theta'], stars['radius'] = cartesian_to_polar(stars['x'], stars['y'])
    max_star_size = 30
    limiting_magnitude = 10
    bright_stars = (stars.magnitude <= limiting_magnitude)
    magnitude = stars['magnitude'][bright_stars]
    marker_size = max_star_size * 10 ** (magnitude / -3.5)
    ''' ploting stars '''
    ax.scatter(stars['theta'][bright_stars], stars['radius'][bright_stars], s=marker_size, color='white', marker='.', linewidths=0, zorder=2)


    ''' calculating positions and ploting other astronomical objects '''
    sun = eph['sun']
    sun_position = earth.at(time).observe(sun)
    sun_theta, sun_radius = cartesian_to_polar(projection(sun_position)[0], projection(sun_position)[1])
    ax.scatter(sun_theta, sun_radius, s=500, color='yellow', marker='.', linewidths=0, zorder=2)

    mercury = eph['MERCURY BARYCENTER']
    mercury_position = earth.at(time).observe(mercury)
    mercury_theta, mercury_radius = cartesian_to_polar(projection(mercury_position)[0], projection(mercury_position)[1])
    ax.scatter(mercury_theta, mercury_radius, s=70, color='brown', marker='.', linewidths=0, zorder=2)

    venus = eph['VENUS BARYCENTER']
    venus_position = earth.at(time).observe(venus)
    venus_theta, venus_radius = cartesian_to_polar(projection(venus_position)[0], projection(venus_position)[1])
    ax.scatter(venus_theta, venus_radius, s=70, color=(200/255,120/255,30/255), marker='.', linewidths=0, zorder=2)

    mars = eph['MARS BARYCENTER']
    mars_position = earth.at(time).observe(mars)
    mars_theta, mars_radius = cartesian_to_polar(projection(mars_position)[0], projection(mars_position)[1])
    ax.scatter(mars_theta, mars_radius, s=70, color=(220/255,60/255,30/255), marker='.', linewidths=0, zorder=2)

    jupiter = eph['JUPITER BARYCENTER']
    jupiter_position = earth.at(time).observe(jupiter)
    jupiter_theta, jupiter_radius = cartesian_to_polar(projection(jupiter_position)[0], projection(jupiter_position)[1])
    ax.scatter(jupiter_theta, jupiter_radius, s=70, color=(145/255,100/255,30/255), marker='.', linewidths=0, zorder=2)

    saturn = eph['SATURN BARYCENTER']
    saturn_position = earth.at(time).observe(saturn)
    saturn_theta, saturn_radius = cartesian_to_polar(projection(saturn_position)[0], projection(saturn_position)[1])
    ax.scatter(saturn_theta, saturn_radius, s=70, color=(190/255,150/255,50/255), marker='.', linewidths=0, zorder=2)

    uranus = eph['URANUS BARYCENTER']
    uranus_position = earth.at(time).observe(uranus)
    uranus_theta, uranus_radius = cartesian_to_polar(projection(uranus_position)[0], projection(uranus_position)[1])
    ax.scatter(uranus_theta, uranus_radius, s=70, color=(60/255,220/255,200/255), marker='.', linewidths=0, zorder=2)

    neptune = eph['NEPTUNE BARYCENTER']
    neptune_position = earth.at(time).observe(neptune)
    neptune_theta, neptune_radius = cartesian_to_polar(projection(neptune_position)[0], projection(neptune_position)[1])
    ax.scatter(neptune_theta, neptune_radius, s=70, color=(35/255,70/255,220/255), marker='.', linewidths=0, zorder=2)

    moon = eph['moon']
    moon_position = earth.at(time).observe(moon)
    moon_theta, moon_radius = cartesian_to_polar(projection(moon_position)[0], projection(moon_position)[1])
    ax.scatter(moon_theta, moon_radius, s=70, color=(75/255,75/255,75/255), marker='.', linewidths=0, zorder=2)

    ax.set_rmax(1)
    ax.set_rmin(0)

    bckg = plt.Circle((0, 0), 4, color='black', fill=True)
    ax.add_patch(bckg)

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    return tmpfile
