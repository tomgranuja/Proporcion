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
        
    def toNextRate(self):
        '''Next rate in list, update currentRate.'''
        nextRate = None
        if self.currentTrial != None:
            self.currentTrial += 1
            if self.currentTrial >= len(self.rates):
                print("Training finished, reseting trials.")
                self.currentTrial = 0
            self.currentRate = self.rates[self.currentTrial]
        
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
    sliderMouseRelease = pyqtSignal(float)
    def __init__(self, parent=None):
        super(Slider, self).__init__(parent)
        self.riel=QLine(self.xFromRate(0),
                        self.yFromRate(0.5),
                        self.xFromRate(1),
                        self.yFromRate(0.5))
        self._userClickX = None
        self._mouseListen = True
        #self.sliderMouseRelease = pyqtSignal(float)    
        
    def paintEvent(self, event=None):
        painter = QPainter(self)
        #Riel
        painter.drawLine(self.riel)
        #Raya
        w = 4
        if self._userClickX:
            raya = QRect(self._userClickX - w / 2, 
                         0, 
                         w,
                         self.HEIGHT)
            painter.setBrush(self.palette().brush(QPalette.Button))
            painter.drawRect(raya)
    
    def mouseReleaseEvent(self,event):
        if self._mouseListen:
            self._mouseListen = False
            self.checkUserEvent(None, event.x())
            self.update()
    
    def checkUserEvent(self, time, x):
        self._userClickX = max(self.riel.x1(), min(self.riel.x2(), x))
        rate = self.rateFromX(self._userClickX)
        self.sliderMouseRelease.emit(rate)

class CheckWidget(CustomRateWidget):
    WIDTH  = Slider.WIDTH
    HEIGHT = Slider.HEIGHT
    def __init__(self, greenError=None, yellError=None, parent=None):
        super(CheckWidget, self).__init__(parent)
        self.setVisible(False)
        self.gSemiWidth = self.wFromRate(greenError)
        self.ySemiWidth = self.wFromRate(yellError)
        self.yellLeftX  = None
        self.greenLeftX = None
        self.feedback   = None
        self.intermitent = False
        
    def adjustRate(self, center):
        spanCenterX = self.xFromRate(center)
        self.yellLeftX  = spanCenterX - self.ySemiWidth
        self.greenLeftX = spanCenterX - self.gSemiWidth
    
    def fbBlink(self, time, period):
        self.timer = QTimer()
        self.timer.timeout.connect(self.fbBlinkStop)
        self.blinktimer = QTimer()
        self.blinktimer.timeout.connect(self.blink)
        self.timer.start(time)
        self.blinktimer.start(period)
        
    def fbBlinkStop(self):
        self.timer.stop()
        self.blinktimer.stop()
        self.intermitent = False
        self.update()
        
    def blink(self):
        self.intermitent = not self.intermitent
        self.update()
        
    
    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        greenColor = QColor(0,128,0,150)
        yellowColor = QColor(222,205,135,150)
        outsideColor = QColor(0,0,0,0)
        h = self.hFromRate(1)
        top = self.xFromRate(0)
        #yellowBox
        if self.yellLeftX:
            painter.setBrush(yellowColor)
            yellowBox = QRect(self.yellLeftX, top, self.ySemiWidth * 2, h)
            painter.drawRect(yellowBox)
        #greenBox
        if self.greenLeftX:
            painter.setBrush(greenColor)
            dx = self.ySemiWidth - self.gSemiWidth
            green = yellowBox.translated(dx , 0)
            green.setWidth(self.gSemiWidth * 2)
            painter.drawRect(green)
        
        feedbackBox = QRect(self.xFromRate(0) - self.MARGIN,
                            self.yFromRate(0) - self.MARGIN,
                            self.WIDTH, 
                            self.HEIGHT)
        box_color = {'outside':outsideColor,
                     'in_yellow':yellowColor,
                      'in_green':greenColor}
        if self.feedback:
            painter.setBrush(box_color[self.feedback])
            if self.intermitent:
                painter.drawRect(feedbackBox)
            
            
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
        self.slider.sliderMouseRelease.connect(self.onSliderMouseRelease)
        
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
        self.rPhotoBox = QLabel("Right Photo")
        self.slider = Slider()
        self.check = CheckWidget(self.test.GREEN_ERROR,
                                 self.test.YELLOW_ERROR,
                                 parent = self.slider)
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.lPhotoBox)
        layout.addWidget(self.slider)
        layout.addWidget(self.rPhotoBox)
        layout.addStretch()
        return layout
    
    def onSliderMouseRelease(self, rate):
        self.test.writeAnswer(None, rate)
        self.check.feedback = self.test.rateCheck(rate)
        self.check.adjustRate(self.test.currentRate)
        #self.check.playFeedbackSound()
        self.check.setVisible(True)
        self.check.fbBlink(1600, 200)
        QTimer.singleShot(3000, self.nextGame)
        
    def nextGame(self):
        self.check.setVisible(False)
        self.test.toNextRate()
        self.rateBox.setBars(1.0, self.test.currentRate)
        self.rateBox.update()
        self.slider._mouseListen = True
        

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
