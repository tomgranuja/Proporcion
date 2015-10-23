#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

import sys, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import slider

class RateBox(QWidget):
    WIDTH  = 120
    HEIGHT = 460
    MARGIN = 20
    def __init__(self, parent=None):
        super(RateBox, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                       QSizePolicy.Fixed))
        self.blueRect = None
        self.redRect  = None
        
    def sizeHint(self):
        return QSize(RateBox.WIDTH, RateBox.HEIGHT)
    
    def setBars(self, height, rate):
        blueHeight = 1.0
        if 0.0 < height  <= 1.0:
            blueHeight = height * (self.height() - RateBox.MARGIN * 2)
            self.blueRect = QRect(
                         RateBox.MARGIN,
                         self.height() - blueHeight - RateBox.MARGIN,
                         self.width() - 2 * RateBox.MARGIN,
                         blueHeight
                         )
            if 0.0 < rate <= 1.0:
                redHeight = rate * blueHeight
                self.redRect = QRect(
                         RateBox.MARGIN,
                         self.height() - redHeight - RateBox.MARGIN,
                         self.width() - 2 * RateBox.MARGIN,
                         redHeight
                         )
        
    def paintEvent(self, event=None):
        painter = QPainter(self)
        blueColor = QColor(85, 142, 213)
        redColor  = QColor(254, 0, 0)
        if self.blueRect:
            painter.setBrush(blueColor)
            painter.drawRect(self.blueRect)
        if self.redRect:
            painter.setBrush(redColor)
            painter.drawRect(self.redRect)

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
        layout = QVBoxLayout()
        layout.addLayout(self.rateBoxLayout())
        layout.addStretch()
        layout.addLayout(self.sliderLayout())
        self.setLayout(layout)
    
    def sizeHint(self):
        return QSize(WhiteBox.WIDTH, WhiteBox.HEIGHT)
    
    def rateBoxLayout(self):
        self.rateBox = RateBox()
        self.rateBox.setBars(1.0, 0.5)
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.rateBox)
        layout.addStretch()
        return layout
    
    def sliderLayout(self):
        self.lPhotoBox = QLabel("L")
        self.slider = slider.Slider()
        self.rPhotoBox = QLabel("R")
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.lPhotoBox)
        layout.addWidget(self.slider)
        layout.addWidget(self.rPhotoBox)
        layout.addStretch()
        return layout


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
