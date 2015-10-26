#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

import sys, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from functools import partial

class Training():
    GREEN_ERROR  = 0.05
    YELLOW_ERROR = 0.15
    
    def __init__(self, rates_data=None):
        self.currentTrial = None
        self.rates = self.getRates(rates_data)
        self.currentRate = self.rates[self.currentTrial]
    
    def getRates(self, data):
        '''Rates from data string, reset trial counter.'''
        float_list = None
        if data:
            float_list = [ float(n) for n in data.split() ]
            self.currentTrial = 0
            print(float_list)
        return float_list
        
    def nextRate(self):
        '''Next rate in list, update currentRate.'''
        nextRate = None
        if self.currentTrial != None:
            self.currentTrial += 1
            if self.currentTrial >= len(self.rates):
                print("Training finished, reseting trials.")
                self.currentTrial = 0
            self.currentRate = self.rates[self.currentTrial]
        return self.currentRate
        
    def rateCheck(self, r=None):
        result = None
        if 0 <= r <= 1:
            result = 'outside'
            error = abs(r - self.currentRate)
            if error <= Training.YELLOW_ERROR:
                result = 'in_yellow'
                if error <= Training.GREEN_ERROR:
                    result = 'in_green'
        return result
        
    def writeAnswer(self, time, rate):
        print(self.currentTrial, time, rate)


def pixelFromRate(rate, t, o = 0):
    return int(round(rate*t)) + o

def rateFromPixel(pixel, t, o = 0):
    return (pixel - o) / t

class CustomRateWidget(QWidget):
    WIDTH  = 50
    HEIGHT = 100
    MARGIN = 20
    def __init__(self, parent=None):
        super(CustomRateWidget, self).__init__(parent)
        fixedPol = QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.setSizePolicy(fixedPol)
        contentW = self.WIDTH - 2 * self.MARGIN
        contentH = self.HEIGHT - 2 * self.MARGIN
        self.wFromRate = partial(pixelFromRate, t=contentW)
        self.hFromRate = partial(pixelFromRate, t=contentH)
        self.xFromRate = partial(pixelFromRate,t=contentW, o=self.MARGIN)
        self.yFromRate = partial(pixelFromRate,t=contentH, o=self.MARGIN)
        self.rateFromX = partial(rateFromPixel,t=contentW, o=self.MARGIN)
    
    def sizeHint(self):
        return QSize(self.WIDTH, self.HEIGHT)

class RateBox(CustomRateWidget):
    WIDTH  = 120
    HEIGHT = 460
    def __init__(self, parent=None):
        super(RateBox, self).__init__(parent)
        self.blueRect = None
        self.redRect  = None
        
    def setBars(self, height, rate):
        blueHeight = 1.0
        if 0.0 < height  <= 1.0:
            self.blueRect = QRect(
                         self.xFromRate(0),
                         self.yFromRate(0),
                         self.wFromRate(1),
                         self.hFromRate(height)
                         )
            if 0.0 < rate <= 1.0:
                uppery = self.yFromRate(1 - rate * height)
                self.redRect = QRect(self.blueRect)
                self.redRect.setTop(uppery)
        
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

class Slider(CustomRateWidget):
    WIDTH  = 440
    HEIGHT = 60
    def __init__(self, parent=None):
        super(Slider, self).__init__(parent)
        self.riel=QLine(self.xFromRate(0),
                        self.yFromRate(0.5),
                        self.xFromRate(1),
                        self.yFromRate(0.5))
        self._userClickX = None
        self._mouseListen = True
        
    def paintEvent(self, event=None):
        painter = QPainter(self)
        #Riel
        painter.drawLine(self.riel)
        #Raya
        w = 4
        if self._userClickX:
            raya = QRect(self._userClickX - w / 2, 
                         self.yFromRate(0), 
                         w,
                         self.hFromRate(1))
            painter.setBrush(self.palette().brush(QPalette.Button))
            painter.drawRect(raya)
    
    def mouseReleaseEvent(self,event):
        if self._mouseListen:
            self._mouseListen = False
            self.checkUserEvent(None, event.x())
            self.update()
            QTimer.singleShot(200, self.nextGame)
    
    def checkUserEvent(self, time, x):
        self._userClickX = max(self.riel.x1(), min(self.riel.x2(), x))
        rate = self.rateFromX(self._userClickX)
        self.parent().test.writeAnswer(time, rate)
        #self.check.feedback = self.test.rateCheck(rate)
        #center = self.xFromRate(self.correctRate)
        #self.check.setSpanLeft(center)
        #self.check.playFeedbackSound()
        #self.refresh()
        #self.check.setVisible(True)
    
    def nextGame(self):
        #self.check.setVisible(False)
        self.currentRate = self.parent().test.nextRate()
        self.parent().rateBox.setBars(1.0, self.currentRate)
        self.parent().rateBox.update()
        self._mouseListen = True
    


class WhiteBox(CustomRateWidget):
    WIDTH  = 640
    HEIGHT = 660
    def __init__(self, parent=None):
        super(WhiteBox, self).__init__(parent)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        self.setAutoFillBackground(True)
        self.test = Training('0.5 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.5')
        layout = QVBoxLayout()
        layout.addLayout(self.rateBoxLayout())
        layout.addStretch()
        layout.addLayout(self.sliderLayout())
        self.setLayout(layout)
        
    def rateBoxLayout(self):
        self.rateBox = RateBox()
        self.rateBox.setBars(1.0, self.test.currentRate)
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.rateBox)
        layout.addStretch()
        return layout
    
    def sliderLayout(self):
        self.lPhotoBox = QLabel("Left Photo")
        self.slider = Slider()
        self.rPhotoBox = QLabel("Right Photo")
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
