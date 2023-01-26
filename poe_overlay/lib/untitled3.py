# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 16:28:26 2023

@author: mrkure
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QPoint
from PyQt5 import QtWidgets
class MyMovableWidget(QWidget):
    """WToolBar is a personalized toolbar."""

    homeAction = None

    oldPos = QPoint()

    def __init__(self):
        super().__init__()

    def mousePressEvent(self, evt):
        """Select the toolbar."""
        self.oldPos = evt.globalPos()

    def mouseMoveEvent(self, evt):
        """Move the toolbar with mouse iteration."""

        delta = QPoint(evt.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = evt.globalPos()

    def resizeEvent(self, event):
        print("Window has been resized")
        # QtWidgets.QMainWindow.resizeEvent(self, event)
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    coolWidget = MyMovableWidget()
    coolWidget.show()
    sys.exit(app.exec_())