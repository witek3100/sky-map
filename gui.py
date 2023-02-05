import sys
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import re

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
        self.resize(1090, 680)

        self.cities = {'Baku' : [40.29, 49.56],
                       'Warsaw' : [52.13, 21],
                       'Buenos Aires' : [-36.3, -60],
                       'Canberra' : [-35.15, 149.08],
                       'Brasilia' : [-15.47, -47.55],
                       'Beijing' : [39.55, 116.2],
                       'Addis Ababa' : [9.02, 38.42],
                       'Tromso' : [69.65, 18.96],
                       'Reykiavik' : [60.15, -21.90],
                       'Nuuk' : [64.18, -51.75],
                       'New York' : [40.73, -73.94],
                       'Seattle' : [47.6, -122.36],
                       'Los Angeles' : [34.05, -118.24],
                       'Houston' : [29.75, -95.35],
                       'Mexico City' : [19.43, -99.13],
                       'Bogota' : [4.62, -74.06],
                       'Barcelona' : [41.39, 2.15],
                       'Lisbon' : [38.74, -9.14],
                       'Berlin' : [52.52, 13.4],
                       'Kair' : [30, 31],
                       'Accra' : [5.35, 0],
                       'New Delhi' : [28.37, 77.13],
                       'Manila' : [14.4, 121.03],
                       'Tokio' : [35.65, 139.83]}

        self.location = location.LocationApi.get_location()
        with open(os.path.relpath("loc.json")) as loc_file:
            observer_loc = json.load(loc_file)
            self.lat = observer_loc["results"][1]['geometry']['location']['lat']
            self.lon = observer_loc["results"][1]['geometry']['location']['lng']
        utc_dt = datetime.datetime.now(tz=pytz.UTC)
        self.time = load.timescale().utc(utc_dt)

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
        self.chart = MapCanvas(self.map_widget, self.lat, self.lon, self.time)
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
            "background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:1, stop:0 rgba(0, 0, 0, 255)"
            ""
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

        self.upperbar = QtWidgets.QLabel(self)
        self.upperbar.setGeometry(QtCore.QRect(0, 0, 1600, 120))
        self.upperbar.setText("")
        self.upperbar.setObjectName("upperbar")
        self.upperbar.setStyleSheet("background-color:rgb(20,20,80,150);")

        self.locationlabel = QtWidgets.QLabel(self)
        self.locationlabel.setGeometry(QtCore.QRect(70, 170, 300, 40))
        self.locationlabel.setText("LOCATION")
        self.locationlabel.setStyleSheet("background-color:rgb(0,0,0,0);"
                                  "font: 16pt \"Calibri\";\n"
                                  "color:rgb(255, 255, 255);")

        self.search_bar = QtWidgets.QLineEdit(self, placeholderText=" search city ... ")
        self.search_bar.setGeometry(QtCore.QRect(120, 220, 220, 45))
        completer = QtWidgets.QCompleter(self.cities)
        self.search_bar.setCompleter(completer)
        self.search_bar.setStyleSheet("background-color:rgb(20,20,60,150);"
                                      "font: 20pt \"Calibri\";\n"
                                      "color:rgb(255, 255, 255);"
                                      "border : 1px solid black;"
                                      "border-radius : 50px;")
        self.search_bar.setObjectName("lineEdit")

        self.get_location_button = QtWidgets.QPushButton(self, clicked= lambda : self.getLocation())
        self.get_location_button.setGeometry(QtCore.QRect(160, 290, 120, 40))
        self.get_location_button.setStyleSheet("background-color:rgb(50,50,50);"
                                               "color:rgb(255,255,255);")
        self.get_location_button.setObjectName("showbutton")
        self.get_location_button.setText("Get your location")

        self.datelabel = QtWidgets.QLabel(self)
        self.datelabel.setGeometry(QtCore.QRect(70, 330, 300, 40))
        self.datelabel.setText("DATE")
        self.datelabel.setStyleSheet("background-color:rgb(0,0,0,0);"
                                         "font: 16pt \"Calibri\";\n"
                                         "color:rgb(255, 255, 255);")

        self.datehourin = QtWidgets.QDateTimeEdit(self)
        self.datehourin.setGeometry(QtCore.QRect(100, 380, 250, 50))
        self.datehourin.setStyleSheet("background-color:rgb(50,50,50);"
                                  "color:rgb(255,255,255);")
        self.datehourin.setDateTime(QtCore.QDateTime.currentDateTime())

        self.setcurrenttimebutton = QtWidgets.QPushButton(self, clicked= lambda : self.datehourin.setDateTime(QtCore.QDateTime.currentDateTime()))
        self.setcurrenttimebutton.setGeometry(160, 440, 120, 40)
        self.setcurrenttimebutton.setStyleSheet("background-color:rgb(50,50,50);"
                                      "color:rgb(255,255,255);")
        self.setcurrenttimebutton.setText("set current")

        self.show_button = QtWidgets.QPushButton(self, clicked= lambda : self.showMap())
        self.show_button.setGeometry(QtCore.QRect(145, 540, 150, 50))
        self.show_button.setStyleSheet("background-color:rgb(50,50,50);"
                                       "color:rgb(255,255,255);")
        self.show_button.setObjectName("showbutton")
        self.show_button.setText("Show")

        self.skymap = QtWidgets.QLabel(self)
        self.skymap.setGeometry(QtCore.QRect(450, 20, 300, 40))
        self.skymap.setStyleSheet("background-color:rgb(0,0,0,0);"
                                  "font: 30pt \"Calibri\";\n"
                                  "color:rgb(255, 255, 255);")
        self.skymap.setObjectName("skymap")
        self.skymap.setText("SKYMAP")

        self.citydate = QtWidgets.QLabel(self)
        self.citydate.setGeometry(QtCore.QRect(110, 70, 900, 40))
        self.citydate.setStyleSheet("background-color:rgb(0,0,0,0);"
                                  "font: 20pt \"Calibri\";\n"
                                  "color:rgb(255, 255, 255);"
                                    "border-radius: 10px;")
        self.citydate.setObjectName("citydate")
        self.citydate.setAlignment(QtCore.Qt.AlignCenter)
        self.setCitydateText()

    def setCitydateText(self):
        f = lambda x: "0{}".format(x) if x < 10 else x
        self.citydate.setText("{} {} - {}.{}.{}  {}:{}".format(round(self.lat,3), round(self.lon,3),
                                                                 f(self.time.utc[2]), f(self.time.utc[1]),
                                                                 self.time.utc[0], f(self.time.utc[3]), f(self.time.utc[4])))

    def getLocation(self):
        self.location = location.LocationApi.get_location()
        with open(os.path.relpath("loc.json")) as loc_file:
            observer_loc = json.load(loc_file)
            self.lat = observer_loc["results"][1]['geometry']['location']['lat']
            self.lon = observer_loc["results"][1]['geometry']['location']['lng']
        self.search_bar.setText("{} {}".format(round(self.lat, 3), round(self.lon, 3)))

    def showMap(self):
        loc = self.search_bar.text()
        if loc in self.cities:
            self.lat, self.lon = self.cities[loc]
        elif not re.search("^[0-9]{2}", loc):
            print('unable to find this location')
            return
        f = lambda x: "0{}".format(x) if x < 10 else x
        ts = load.timescale()

        self.citydate.setText("{} - {}.{}.{}  {}:{}".format(loc, f(self.time.utc[2]), f(self.time.utc[1]),
                                                            self.time.utc[0], f(self.time.utc[3]),
                                                            f(self.time.utc[4])))
        self.time = ts.utc(self.datehourin.date().year(), self.datehourin.date().month(), self.datehourin.date().day(),
                                  self.datehourin.time().hour(), self.datehourin.time().minute())
        self.chart = MapCanvas(self.map_widget, self.lat, self.lon, self.time)



app = QtWidgets.QApplication(sys.argv)
gui = MainWindow()
gui.show()
sys.exit(app.exec_())