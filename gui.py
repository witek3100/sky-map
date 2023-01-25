import sys
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import json
import os
import datetime as datetime
import numpy as np
import pytz
from matplotlib.colors import LinearSegmentedColormap
import skyfield.api
from geopy import Nominatim
from matplotlib.patches import Circle
from tzwhere import tzwhere
import matplotlib.image as mpimg
import matplotlib as mpl
from pytz import timezone, utc
import matplotlib.pyplot as plt
from matplotlib import *
from skyfield.api import Star, load, wgs84, load_constellation_map, position_of_radec, load_constellation_names
from skyfield.data import hipparcos, stellarium
from skyfield.projections import build_stereographic_projection
import location
from PIL import Image
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
import constelations
import pandas
from skymap import MapCanvas

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1600, 800)

        self.map_widget = QtWidgets.QLabel(self)
        self.map_widget.setGeometry(QtCore.QRect(400, 100, 600, 600))
        self.map_widget.setText("")
        self.map_widget.setObjectName("mapwidget")
        self.chart = MapCanvas(self.map_widget)
        self.chart.resize(600, 600)


app = QtWidgets.QApplication(sys.argv)
gui = MainWindow()
gui.show()
sys.exit(app.exec_())