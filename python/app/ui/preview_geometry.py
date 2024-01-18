from tank.platform.qt import QtCore, QtGui
import os 

class Ui_Preview_Geometry(object):
    def setupUi(self, Preview_Geometry):
        Preview_Geometry.setObjectName("Preview_Geometry")
        Preview_Geometry.resize(350, 90)
        Preview_Geometry.setStyleSheet("QMainWindow{\n"
                                        "background-color: rgb(75, 75, 75);\n"
                                        "}")

        self.horizontalLayout = QtGui.QHBoxLayout(Preview_Geometry)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.update_btn = QtGui.QPushButton(Preview_Geometry)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.update_btn.sizePolicy().hasHeightForWidth())
        self.update_btn.setSizePolicy(sizePolicy)
        self.update_btn.setObjectName("update_btn")
        self.update_btn.setStyleSheet("QPushButton{\n"
                    "	background-color:  rgb(107, 107, 107);\n"
                    "	font:  15px;\n"
                    "	color:  rgb(255, 255, 255)\n"
                    "}\n"
                    "QPushButton:hover{\n"
                    "	background-color:  rgb(255, 139, 214);\n"
                    "	font:  15px;\n"
                    "	color:    rgb(28, 217, 255)\n"
                    "}\n"
                    "QPushButton:pressed{\n"
                    "	background-color:  rgb(255, 139, 214);\n"
                    "	font:  15px;\n"
                    "	color:  rgb(28, 217, 255)\n"
                    "}")
        self.horizontalLayout.addWidget(self.update_btn)

        self.finalize_btn = QtGui.QPushButton(Preview_Geometry)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.finalize_btn.sizePolicy().hasHeightForWidth())
        self.finalize_btn.setSizePolicy(sizePolicy)
        self.finalize_btn.setObjectName("finalize_btn")
        self.finalize_btn.setStyleSheet("QPushButton{\n"
            "	background-color:  rgb(107, 107, 107);\n"
            "	font:  15px;\n"
            "	color:  rgb(255, 255, 255)\n"
            "}\n"
            "QPushButton:hover{\n"
            "	background-color:  rgb(255, 139, 214);\n"
            "	font:  15px;\n"
            "	color:    rgb(28, 217, 255)\n"
            "}\n"
            "QPushButton:pressed{\n"
            "	background-color:  rgb(255, 139, 214);\n"
            "	font:  15px;\n"
            "	color:  rgb(28, 217, 255)\n"
            "}")
        self.horizontalLayout.addWidget(self.finalize_btn)

        self.retranslateUi(Preview_Geometry)
        QtCore.QMetaObject.connectSlotsByName(Preview_Geometry)

    def retranslateUi(self, Preview_Geometry):
        Preview_Geometry.setWindowTitle(QtGui.QApplication.translate("Preview_Geometry", "Preview geometry", None, QtGui.QApplication.UnicodeUTF8))
        self.update_btn.setText(QtGui.QApplication.translate("Preview_Geometry", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.finalize_btn.setText(QtGui.QApplication.translate("Preview_Geometry", "Finalize", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc