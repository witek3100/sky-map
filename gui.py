from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1015, 696)
        MainWindow.setStyleSheet("background:rgb(25, 25, 25)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-30, -20, 1061, 211))
        self.label.setStyleSheet("background:rgb(0, 0, 85,100)")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(260, 80, 121, 41))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 15pt \"Yu Gothic UI Semilight\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(380, 10, 291, 61))
        self.label_3.setStyleSheet("color:rgb(255, 255, 255);\n"
"font: 25 22pt \"Segoe UI Light\";")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(650, 80, 121, 41))
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 15pt \"Yu Gothic UI Semilight\";")
        self.label_4.setObjectName("label_4")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox.setGeometry(QtCore.QRect(590, 130, 81, 41))
        self.doubleSpinBox.setStyleSheet("background-color: rgb(132, 132, 132);")
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(170, 130, 151, 41))
        self.dateEdit.setStyleSheet("background-color: rgb(132, 132, 132);")
        self.dateEdit.setObjectName("dateEdit")
        self.timeEdit = QtWidgets.QTimeEdit(self.centralwidget)
        self.timeEdit.setGeometry(QtCore.QRect(340, 130, 81, 41))
        self.timeEdit.setStyleSheet("background-color: rgb(132, 132, 132);")
        self.timeEdit.setObjectName("timeEdit")
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_2.setGeometry(QtCore.QRect(730, 130, 81, 41))
        self.doubleSpinBox_2.setStyleSheet("background-color: rgb(132, 132, 132);")
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(860, 130, 91, 41))
        self.pushButton.setStyleSheet("background-color: rgb(132, 132, 132);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 130, 91, 41))
        self.pushButton_2.setStyleSheet("background-color: rgb(132, 132, 132);")
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "select date"))
        self.label_3.setText(_translate("MainWindow", "S K Y M A P"))
        self.label_4.setText(_translate("MainWindow", "set location"))
        self.pushButton.setText(_translate("MainWindow", "show map"))
        self.pushButton_2.setText(_translate("MainWindow", "settings"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
