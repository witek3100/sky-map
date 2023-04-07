from matplotlib.patches import Circle
import matplotlib.pyplot as plt
from skyfield.api import Star, load, wgs84, load_constellation_map, position_of_radec, load_constellation_names, utc
from skyfield.data import hipparcos, stellarium
from skyfield.projections import build_stereographic_projection
from io import BytesIO
from matplotlib.figure import Figure




def create_map(longtitude, latitude, utc_dt):

    time = load.timescale().utc(utc_dt)
    lon = longtitude
    lat = latitude

    fig = Figure(figsize=(10,10), dpi=100, frameon=False)
    fig.set_facecolor((1,1,1))
    ax = fig.subplots()
    observer = wgs84.latlon(latitude_degrees=lat, longitude_degrees=lon).at(time)
    position = observer.from_altaz(alt_degrees=90, az_degrees=0)

    ra, dec, distance = observer.radec()
    center_object = Star(ra=ra, dec=dec)

    eph = load('de421.bsp')
    with load.open('hip_main.dat') as f:
        stars = hipparcos.load_dataframe(f)

    earth = eph['earth']
    center = earth.at(time).observe(center_object)
    projection = build_stereographic_projection(center)
    field_of_view_degrees = 180.0

    star_positions = earth.at(time).observe(Star.from_dataframe(stars))
    stars['x'], stars['y'] = projection(star_positions)
    chart_size = 10
    max_star_size = 30
    limiting_magnitude = 10
    bright_stars = (stars.magnitude <= limiting_magnitude)
    magnitude = stars['magnitude'][bright_stars]
    marker_size = max_star_size * 10 ** (magnitude / -3.5)
    scatter = ax.scatter(stars['x'][bright_stars], stars['y'][bright_stars],
                                 s=marker_size, color='white', marker='.', linewidths=0,
                                 zorder=2)

    sun = eph['sun']
    mercury = eph['MERCURY BARYCENTER']
    venus = eph['VENUS BARYCENTER']
    mars = eph['MARS BARYCENTER']
    jupiter = eph['JUPITER BARYCENTER']
    saturn = eph['SATURN BARYCENTER']
    uranus = eph['URANUS BARYCENTER']
    neptune = eph['NEPTUNE BARYCENTER']
    moon = eph['moon']

    mercury_position = earth.at(time).observe(mercury)
    mercury_x, mercury_y = projection(mercury_position)

    venus_position = earth.at(time).observe(venus)
    venus_x, venus_y = projection(venus_position)

    mars_position = earth.at(time).observe(mars)
    mars_x, mars_y = projection(mars_position)

    jupiter_position = earth.at(time).observe(jupiter)
    jupiter_x, jupiter_y = projection(jupiter_position)

    saturn_position = earth.at(time).observe(saturn)
    saturn_x, saturn_y = projection(saturn_position)

    uranus_position = earth.at(time).observe(uranus)
    uranus_x, uranus_y = projection(uranus_position)

    neptune_position = earth.at(time).observe(neptune)
    neptune_x, neptune_y = projection(neptune_position)

    moon_position = earth.at(time).observe(moon)
    moon_x, moon_y = projection(moon_position)

    sun_position = earth.at(time).observe(sun)
    sun_x, sun_y = projection(sun_position)

    ax.scatter(mercury_x, mercury_y,
                            s=70, color='brown', marker='.', linewidths=0,
                            zorder=2)

    ax.scatter(venus_x, venus_y,
                            s=90, color='orange', marker='.', linewidths=0,
                            zorder=2)

    ax.scatter(mars_x, mars_y,
                       s=100, color='red', marker='.', linewidths=0,
                       zorder=2)

    ax.scatter(jupiter_x, jupiter_y,
                            s=120, color='peru', marker='.', linewidths=0,
                            zorder=2)

    ax.scatter(saturn_x, saturn_y,
                            s=110, color='grey', marker='.', linewidths=0,
                            zorder=2)

    ax.scatter(uranus_x, uranus_y,
                       s=100, color='cyan', marker='.', linewidths=0,
                       zorder=2)

    ax.scatter(neptune_x, neptune_y,
                            s=100, color='blue', marker='.', linewidths=0,
                            zorder=2)

    ax.scatter(moon_x, moon_y,
                       s=150, color='grey', marker='o', linewidths=0,
                       zorder=2)

    sun = ax.scatter(sun_x, sun_y,
                             s=500, color='yellow', marker='.', linewidths=0,
                             zorder=2)

    bckg = plt.Circle((0, 0), 4, color='black', fill=True)
    ax.add_patch(bckg)
    border = plt.Circle((0, 0), 0.99, color='grey', fill=False, linewidth=0.8)
    ax.add_patch(border)
    horizon = Circle((0, 0), radius=1, transform=ax.transData)
    for col in ax.collections:
        col.set_clip_path(horizon)

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.axis('off')
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')

    return tmpfile
