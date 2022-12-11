# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cost_table.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dlgCosts(object):
    def setupUi(self, dlgCosts):
        dlgCosts.setObjectName("dlgCosts")
        dlgCosts.resize(656, 297)
        self.tblCosts = QtWidgets.QTableWidget(dlgCosts)
        self.tblCosts.setGeometry(QtCore.QRect(10, 20, 631, 261))
        self.tblCosts.setAlternatingRowColors(True)
        self.tblCosts.setObjectName("tblCosts")
        self.tblCosts.setColumnCount(6)
        self.tblCosts.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tblCosts.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblCosts.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblCosts.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblCosts.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblCosts.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tblCosts.setHorizontalHeaderItem(5, item)

        self.retranslateUi(dlgCosts)
        QtCore.QMetaObject.connectSlotsByName(dlgCosts)

    def retranslateUi(self, dlgCosts):
        _translate = QtCore.QCoreApplication.translate
        dlgCosts.setWindowTitle(_translate("dlgCosts", "Koszty map w powiatach"))
        item = self.tblCosts.horizontalHeaderItem(0)
        item.setText(_translate("dlgCosts", "Powiat"))
        item = self.tblCosts.horizontalHeaderItem(1)
        item.setText(_translate("dlgCosts", "powierzchnia"))
        item = self.tblCosts.horizontalHeaderItem(2)
        item.setText(_translate("dlgCosts", "koszt (1:500)"))
        item = self.tblCosts.horizontalHeaderItem(3)
        item.setText(_translate("dlgCosts", "koszt (1:1000)"))
        item = self.tblCosts.horizontalHeaderItem(4)
        item.setText(_translate("dlgCosts", "koszt (1:2000)"))
        item = self.tblCosts.horizontalHeaderItem(5)
        item.setText(_translate("dlgCosts", "koszt (1:5000)"))
