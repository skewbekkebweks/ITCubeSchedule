# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_office.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddOffice(object):
    def setupUi(self, AddOffice):
        AddOffice.setObjectName("AddOffice")
        AddOffice.resize(374, 468)
        self.centralwidget = QtWidgets.QWidget(AddOffice)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.number_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.number_edit.setObjectName("number_edit")
        self.gridLayout.addWidget(self.number_edit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.title_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.title_edit.setObjectName("title_edit")
        self.gridLayout.addWidget(self.title_edit, 1, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 1, 1, 1)
        AddOffice.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(AddOffice)
        self.statusbar.setObjectName("statusbar")
        AddOffice.setStatusBar(self.statusbar)

        self.retranslateUi(AddOffice)
        QtCore.QMetaObject.connectSlotsByName(AddOffice)

    def retranslateUi(self, AddOffice):
        _translate = QtCore.QCoreApplication.translate
        AddOffice.setWindowTitle(_translate("AddOffice", "Добавление кабинета"))
        self.label.setText(_translate("AddOffice", "Введите номер кабинета"))
        self.label_2.setText(_translate("AddOffice", "Введите название кабинета"))
        self.pushButton.setText(_translate("AddOffice", "Готово"))
