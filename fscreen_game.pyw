#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

import sys, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#import slider_camilo

class WhiteBox(QWidget):
    WIDTH = 640
    HEIGHT= 660
    def __init__(self, parent=None):
        super(WhiteBox, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                       QSizePolicy.Fixed))
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        self.setAutoFillBackground(True)
    
    def sizeHint(self):
        return QSize(WhiteBox.WIDTH, WhiteBox.HEIGHT)


class FullBox(QDialog):
    def __init__(self, parent=None):
        super(FullBox, self).__init__(parent)
        p = self.palette()
        bgColor = QColor(179,179,179)
        p.setColor(self.backgroundRole(), bgColor)
        self.setPalette(p)
        self.setAutoFillBackground(True)
        self.whiteBox = WhiteBox()
        layout = QHBoxLayout()
        layout.addWidget(self.whiteBox)
        self.setLayout(layout)
        
        
if __name__ == "__main__":
    app  = QApplication(sys.argv)
    form = FullBox()
    form.showFullScreen()
    sys.exit(app.exec_())
