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

        self.background = QtWidgets.QLabel(self)
        self.background.setGeometry(QtCore.QRect(0,0,2000,1000))
        self.background.setText("")
        self.background.setObjectName("background")
        self.background.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 11, 25, 255)"
                                      ", stop:1 rgba(10, 2, 25, 255));\n""border-color: rgb(3, 10, 9z);\n""}")

        self.map_widget = QtWidgets.QLabel(self)
        self.map_widget.setGeometry(QtCore.QRect(500, 100, 600, 600))
        self.map_widget.setStyleSheet("background-color:rgba(30, 100, 190, 255);\n")
        self.map_widget.setText("")
        self.map_widget.setObjectName("mapwidget")
        self.chart = MapCanvas(self.map_widget)
        self.chart.resize(600, 600)

        self.ub = QtWidgets.QLabel(self)
        self.ub.setGeometry(QtCore.QRect(500, 100, 610, 72))
        self.ub.setText("")
        self.ub.setObjectName("lb")
        self.ub.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 25, 255)"
                                      ", stop:1 rgba(0, 0, 0, 255));\n""border-color: rgb(3, 0, 9z);\n""}")

        self.bb = QtWidgets.QLabel(self)
        self.bb.setGeometry(QtCore.QRect(500, 633, 610, 72))
        self.bb.setText("")
        self.bb.setObjectName("lb")
        self.bb.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(0, 0, 25, 255)"
            ", stop:1 rgba(0, 0, 0, 255));\n""border-color: rgb(0, 0, 0z);\n""}")

        self.lb = QtWidgets.QLabel(self)
        self.lb.setGeometry(QtCore.QRect(500, 100, 75, 600))
        self.lb.setText("")
        self.lb.setObjectName("lb")
        self.lb.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(0, 0, 25, 255)"
                                      ", stop:1 rgba(0, 0, 0, 255));\n""border-color: rgb(0, 0, 0z);\n""}")


        self.rb = QtWidgets.QLabel(self)
        self.rb.setGeometry(QtCore.QRect(1040, 100, 72, 600))
        self.rb.setText("")
        self.rb.setObjectName("lb")
        self.rb.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 rgba(0, 0, 0, 255)"
            ", stop:1 rgba(0, 0, 25, 255));\n""border-color: rgb(0, 0, 0z);\n""}")

        self.search_bar = QtWidgets.QLineEdit(self, placeholderText=" search city ... ")
        self.search_bar.setGeometry(QtCore.QRect(800, 10, 500, 90))
        completer = QtWidgets.QCompleter(['Nowy Jork', 'Sydney', 'Johanesburg', 'Rio de Janiero'])
        self.search_bar.setCompleter(completer)
        self.search_bar.setStyleSheet("background-color:rgb(0,0,25,150);"
                                      "font: 20pt \"Calibri\";\n"
                                      "color:rgb(255, 255, 255);")
        self.search_bar.setObjectName("lineEdit")


app = QtWidgets.QApplication(sys.argv)
gui = MainWindow()
gui.show()
sys.exit(app.exec_())