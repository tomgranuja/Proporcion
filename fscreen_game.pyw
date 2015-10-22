#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

import sys, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import slider

class WhiteBox(QWidget):
    WIDTH = 640
    HEIGHT= 660
    MARGIN= 20
    def __init__(self, parent=None):
        super(WhiteBox, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                       QSizePolicy.Fixed))
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        self.setAutoFillBackground(True)
        self.sliderLayout = self.setSliderLayout()
        self.setRateBox()
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addLayout(self.sliderLayout)
        self.setLayout(layout)
    
    def sizeHint(self):
        return QSize(WhiteBox.WIDTH, WhiteBox.HEIGHT)
    
    def setSliderLayout(self):
        self.lPhotoBox = QLabel("L")
        self.slider = slider.Slider()
        self.rPhotoBox = QLabel("R")
        layout = QHBoxLayout()
        layout.addWidget(self.lPhotoBox)
        layout.addWidget(self.slider)
        layout.addWidget(self.rPhotoBox)
        return layout
    
    def setRateBox(self):
        pass

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
