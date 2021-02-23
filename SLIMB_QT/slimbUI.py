# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'slimb.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtCore,  QtWidgets 


class Ui_SLIMB(object):
    def setupUi(self, SLIMB,homeurl):
        SLIMB.setObjectName("SLIMB")
        SLIMB.resize(1075, 838)
        self.centralwidget = QtWidgets.QWidget(SLIMB)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 1041, 71))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.butBack = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.butBack.setObjectName("butBack")
        self.horizontalLayout.addWidget(self.butBack)
        self.butRefresh = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.butRefresh.setObjectName("butRefresh")
        self.horizontalLayout.addWidget(self.butRefresh)
        self.butForward = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.butForward.setObjectName("butForward")
        self.horizontalLayout.addWidget(self.butForward)
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(19, 130, 1041, 661))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.webView = QWebEngineView(self.gridLayoutWidget)
        self.webView.setUrl(QtCore.QUrl(homeurl))
        self.webView.setObjectName("webView")
        self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)
        SLIMB.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SLIMB)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1075, 22))
        self.menubar.setObjectName("menubar")
        self.menuSetting = QtWidgets.QMenu(self.menubar)
        self.menuSetting.setObjectName("menuSetting")
        SLIMB.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SLIMB)
        self.statusbar.setObjectName("statusbar")
        SLIMB.setStatusBar(self.statusbar)
        self.actionReboot = QtWidgets.QAction(SLIMB)
        self.actionReboot.setObjectName("actionReboot")
        self.actionSend_Email = QtWidgets.QAction(SLIMB)
        self.actionSend_Email.setObjectName("actionSend_Email")
        self.menuSetting.addAction(self.actionReboot)
        self.menuSetting.addAction(self.actionSend_Email)
        self.menubar.addAction(self.menuSetting.menuAction())

        self.retranslateUi(SLIMB)
        self.actionReboot.triggered.connect(self.actionReboot.trigger)
        self.actionSend_Email.triggered.connect(self.actionSend_Email.trigger)
        self.butBack.clicked.connect(self.butBack.click)
        self.butForward.clicked.connect(self.butForward.click)
        self.butRefresh.clicked.connect(self.butRefresh.click)
        QtCore.QMetaObject.connectSlotsByName(SLIMB)

    def retranslateUi(self, SLIMB):
        _translate = QtCore.QCoreApplication.translate
        SLIMB.setWindowTitle(_translate("SLIMB", "MainWindow"))
        self.butBack.setText(_translate("SLIMB", "BACK"))
        self.butRefresh.setText(_translate("SLIMB", "REFRESH"))
        self.butForward.setText(_translate("SLIMB", "FORWARD"))
        self.menuSetting.setTitle(_translate("SLIMB", "Setting"))
        self.actionReboot.setText(_translate("SLIMB", "Reboot"))
        self.actionSend_Email.setText(_translate("SLIMB", "Send Email"))

