# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(473, 343)
        self.fileBox = QtWidgets.QTextBrowser(Dialog)
        self.fileBox.setGeometry(QtCore.QRect(40, 60, 271, 31))
        self.fileBox.setObjectName("fileBox")
        self.browse_btn = QtWidgets.QPushButton(Dialog)
        self.browse_btn.setGeometry(QtCore.QRect(322, 60, 131, 41))
        self.browse_btn.setObjectName("browse_btn")
        self.OK_btn = QtWidgets.QPushButton(Dialog)
        self.OK_btn.setGeometry(QtCore.QRect(190, 120, 121, 41))
        self.OK_btn.setObjectName("OK_btn")
        self.quit_btn = QtWidgets.QPushButton(Dialog)
        self.quit_btn.setGeometry(QtCore.QRect(320, 120, 131, 41))
        self.quit_btn.setObjectName("quit_btn")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 20, 131, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(230, 170, 231, 51))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.browse_btn.setText(_translate("Dialog", "Browse"))
        self.OK_btn.setText(_translate("Dialog", "O   K"))
        self.quit_btn.setText(_translate("Dialog", "Quit"))
        self.label.setText(_translate("Dialog", "Upload File"))
        self.label_2.setText(_translate("Dialog", "Design & Developed by 영환 , 소빈"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

