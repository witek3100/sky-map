from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import json
import datetime as datetime
import pytz
from matplotlib.patches import Circle
import matplotlib.pyplot as plt
from matplotlib import *
from skyfield.api import Star, load, wgs84, load_constellation_map, position_of_radec, load_constellation_names
from skyfield.data import hipparcos, stellarium
from skyfield.projections import build_stereographic_projection
import location


class MapCanvas(FigureCanvas):
    def __init__(self, parent, lat, lon):
        fig, self.ax = plt.subplots(figsize=(5,4), dpi=200)
        super().__init__(fig)
        self.setParent(parent)

        utc_dt = datetime.datetime.now(tz=pytz.UTC)
        self.time = load.timescale().utc(utc_dt)

        self.observer = wgs84.latlon(latitude_degrees=lat, longitude_degrees=lon).at(self.time)
        self.position = self.observer.from_altaz(alt_degrees=90, az_degrees=0)

        ra, dec, distance = self.observer.radec()
        center_object = Star(ra=ra, dec=dec)

        eph = load('de421.bsp')
        with load.open(hipparcos.URL) as f:
            stars = hipparcos.load_dataframe(f)

        earth = eph['earth']
        center = earth.at(self.time).observe(center_object)
        projection = build_stereographic_projection(center)
        field_of_view_degrees = 180.0

        star_positions = earth.at(self.time).observe(Star.from_dataframe(stars))
        stars['x'], stars['y'] = projection(star_positions)
        chart_size = 10

        max_star_size = 50
        limiting_magnitude = 10

        bright_stars = (stars.magnitude <= limiting_magnitude)
        magnitude = stars['magnitude'][bright_stars]

        marker_size = max_star_size * 10 ** (magnitude / -2.5)

        scatter = self.ax.scatter(stars['x'][bright_stars], stars['y'][bright_stars],
                             s=marker_size, color='white', marker='.', linewidths=0,
                             zorder=2)

        bckg = plt.Circle((0, 0), 4, color='black', fill=True)
        self.ax.add_patch(bckg)
        border = plt.Circle((0, 0), 1, color='grey', fill=False)
        self.ax.add_patch(border)

        horizon = Circle((0, 0), radius=1, transform=self.ax.transData)
        for col in self.ax.collections:
            col.set_clip_path(horizon)

        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)
        plt.axis('off')
