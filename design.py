# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(742, 450)

        oImage = QImage("tedd_codd.jpg")
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(oImage))
        self.setPalette(palette)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.def_q1_button = QtWidgets.QPushButton(self.centralwidget)
        self.def_q1_button.setGeometry(QtCore.QRect(10, 40, 261, 61))
        self.def_q1_button.setStyleSheet("background:transparent;\n"
"background-color: rgb(255, 255, 255);")
        self.def_q1_button.setObjectName("def_q1_button")
        self.def_q2_button = QtWidgets.QPushButton(self.centralwidget)
        self.def_q2_button.setGeometry(QtCore.QRect(10, 120, 261, 61))
        self.def_q2_button.setStyleSheet("background:transparent;\n"
"background-color: rgb(255, 255, 255);")
        self.def_q2_button.setObjectName("def_q2_button")
        self.def_q3_button = QtWidgets.QPushButton(self.centralwidget)
        self.def_q3_button.setGeometry(QtCore.QRect(10, 200, 261, 61))
        self.def_q3_button.setStyleSheet("background:transparent;\n"
"background-color: rgb(255, 255, 255);")
        self.def_q3_button.setObjectName("def_q3_button")
        self.def_q4_button = QtWidgets.QPushButton(self.centralwidget)
        self.def_q4_button.setGeometry(QtCore.QRect(10, 280, 261, 61))
        self.def_q4_button.setStyleSheet("background:transparent;\n"
"background-color: rgb(255, 255, 255);")
        self.def_q4_button.setObjectName("def_q4_button")
        self.def_q5_button = QtWidgets.QPushButton(self.centralwidget)
        self.def_q5_button.setGeometry(QtCore.QRect(10, 360, 261, 61))
        self.def_q5_button.setStyleSheet("background:transparent;\n"
"background-color: rgb(255, 255, 255);")
        self.def_q5_button.setObjectName("def_q5_button")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(300, 40, 431, 301))
        self.textEdit.setStyleSheet("background:transparent;\n"
"background-color: rgb(255, 255, 255);")
        self.textEdit.setObjectName("textEdit")
        self.exe_button = QtWidgets.QPushButton(self.centralwidget)
        self.exe_button.setGeometry(QtCore.QRect(410, 350, 221, 31))
        self.exe_button.setStyleSheet("background:transparent;\n"
"background-color: rgb(255, 255, 255);")
        self.exe_button.setObjectName("exe_button")
        self.def_label = QtWidgets.QLabel(self.centralwidget)
        self.def_label.setGeometry(QtCore.QRect(80, 10, 111, 16))
        self.def_label.setStyleSheet("background:transparent;\n"
"background-color: rgb(255, 255, 255);")
        self.def_label.setObjectName("def_label")
        self.ur_label = QtWidgets.QLabel(self.centralwidget)
        self.ur_label.setGeometry(QtCore.QRect(470, 10, 101, 16))
        self.ur_label.setStyleSheet("background:transparent;\n"
"background-color: rgb(255, 255, 255);")
        self.ur_label.setObjectName("ur_label")
        self.gen_data_button = QtWidgets.QPushButton(self.centralwidget)
        self.gen_data_button.setGeometry(QtCore.QRect(410, 390, 221, 31))
        self.gen_data_button.setStyleSheet("background:transparent;\n"
"background-color: rgb(255, 255, 255);")
        self.gen_data_button.setObjectName("gen_data_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.def_q1_button.setText(_translate("MainWindow", "Default Qeury 1"))
        self.def_q2_button.setText(_translate("MainWindow", "Default Qeury 2"))
        self.def_q3_button.setText(_translate("MainWindow", "Default Qeury 3"))
        self.def_q4_button.setText(_translate("MainWindow", "Default Qeury 4"))
        self.def_q5_button.setText(_translate("MainWindow", "Default Qeury 5"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:9pt; color:#000000;\">Some text</span></p></body></html>"))
        self.exe_button.setText(_translate("MainWindow", "Execute"))
        self.def_label.setText(_translate("MainWindow", " Default queries"))
        self.ur_label.setText(_translate("MainWindow", "  Your queries"))
        self.gen_data_button.setText(_translate("MainWindow", "Generate Data"))

