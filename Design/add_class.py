# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_class.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddClass(object):
    def setupUi(self, AddClass):
        AddClass.setObjectName("AddClass")
        AddClass.resize(400, 300)
        self.centralwidget = QtWidgets.QWidget(AddClass)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_start = QtWidgets.QLabel(self.centralwidget)
        self.label_start.setObjectName("label_start")
        self.gridLayout.addWidget(self.label_start, 0, 0, 1, 1)
        self.time_start = QtWidgets.QTimeEdit(self.centralwidget)
        self.time_start.setObjectName("time_start")
        self.gridLayout.addWidget(self.time_start, 0, 1, 1, 1)
        self.label_stop = QtWidgets.QLabel(self.centralwidget)
        self.label_stop.setObjectName("label_stop")
        self.gridLayout.addWidget(self.label_stop, 1, 0, 1, 1)
        self.time_stop = QtWidgets.QTimeEdit(self.centralwidget)
        self.time_stop.setObjectName("time_stop")
        self.gridLayout.addWidget(self.time_stop, 1, 1, 1, 1)
        self.label_group = QtWidgets.QLabel(self.centralwidget)
        self.label_group.setObjectName("label_group")
        self.gridLayout.addWidget(self.label_group, 2, 0, 1, 1)
        self.group_box = QtWidgets.QComboBox(self.centralwidget)
        self.group_box.setObjectName("group_box")
        self.gridLayout.addWidget(self.group_box, 2, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 1, 1, 1)
        AddClass.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(AddClass)
        self.statusbar.setObjectName("statusbar")
        AddClass.setStatusBar(self.statusbar)

        self.retranslateUi(AddClass)
        QtCore.QMetaObject.connectSlotsByName(AddClass)

    def retranslateUi(self, AddClass):
        _translate = QtCore.QCoreApplication.translate
        AddClass.setWindowTitle(_translate("AddClass", "Добавление занятия"))
        self.label_start.setText(_translate("AddClass", "Введите начало занятия"))
        self.label_stop.setText(_translate("AddClass", "Введите конец занятия"))
        self.label_group.setText(_translate("AddClass", "Выберите группу"))
        self.pushButton.setText(_translate("AddClass", "Готово"))
