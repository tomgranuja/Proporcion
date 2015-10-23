#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

import sys, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *
audio = None
if QSound.isAvailable():
    audio = 'qsound'
else:
    from PyQt4.phonon import Phonon
    m_media = Phonon.MediaObject()
    audioOutput = Phonon.AudioOutput(Phonon.GameCategory)
    Phonon.createPath(m_media, audioOutput)
    audio = 'phonon'

class Training():
    MIN_RATE = 0.2
    MAX_RATE = 0.8
    GREEN_ERROR  = 0.05
    YELLOW_ERROR = 0.15
    
    def __init__(self, rates_data=None):
        self.currentTrial = None
        self.rates = self.getRates(rates_data)
    
    def getRates(self, data):
        '''Rates from data string, reset trial counter.'''
        float_list = None
        if data:
            float_list = [ float(n) for n in data.split() ]
            self.currentTrial = 0
            print(float_list)
        return float_list
        
    def nextRate(self):
        '''Next rate in list, update current trial counter.'''
        nextRate = None
        if self.currentTrial != None:
            self.currentTrial += 1
            if self.currentTrial >= len(self.rates):
                print("Training finished, reseting trials.")
                self.currentTrial = 0
            nextRate = self.rates[self.currentTrial]
        return nextRate
        
    def rateCheck(self, r=None):
        result = None
        if 0 <= r <= 1:
            result = 'outside'
            correctRate = self.rates[self.currentTrial]
            error = abs(r - correctRate)
            if error <= Training.YELLOW_ERROR:
                result = 'in_yellow'
                if error <= Training.GREEN_ERROR:
                    result = 'in_green'
        return result
        
    def writeAnswer(self, time, rate):
        print(self.currentTrial, time, rate)


class CheckWidget(QWidget):
    def __init__(self, riel=None, greenWidth=None, yellWidth=None,
                 parent=None):
        super(CheckWidget, self).__init__(parent)
        self.riel = riel
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                       QSizePolicy.Fixed))
        self.setVisible(False)
        self.greenWidth = greenWidth
        self.yellWidth  = yellWidth
        self.spanLeft = None
        self.feedback = None
        
    def setSpanLeft(self, center):
        span = self.yellWidth
        min_val = self.riel.left() 
        max_val = self.riel.right() - span
        left = center - int(span / 2)
        self.spanLeft = max(min_val, min(max_val, left))
        
    def sizeHint(self):
        return self.parent().sizeHint()
                
    def paintEvent(self, event=None):
        painter = QPainter(self)
        greenColor = QColor(0,128,0)
        yellowColor = QColor(222,205,135)
        
        h = self.riel.height()
        top = self.riel.top()
        if self.spanLeft:
            painter.setBrush(yellowColor)
            #yellowBox
            yellowBox = QRect(self.spanLeft, top, self.yellWidth, h)
            painter.drawRect(yellowBox)
            #greenBox
            painter.setBrush(greenColor)
            dx = (self.yellWidth - self.greenWidth)/ 2
            green = yellowBox.translated(dx , 0)
            green.setWidth(self.greenWidth)
            painter.drawRect(green)
        
        feedbackBox = QRect(self.riel.left(),
                            self.parent().cuadro.top(),
                            self.riel.width(), 
                            self.riel.height() / 2)
        box_color = {'outside':self.palette().brush(QPalette.Midlight),
                     'in_yellow':yellowColor,
                      'in_green':greenColor}
        if self.feedback:
            painter.setBrush(box_color[self.feedback])
            painter.drawRect(feedbackBox)
            
            
    def playFeedbackSound(self):
        if self.feedback:
            wav = {'outside'  : 'bad2.wav',
                   'in_yellow': 'good.wav',
                   'in_green' : 'excelent.wav'}
            if audio == 'qsound':
                QSound.play(wav[self.feedback])
            elif audio == 'phonon':
                m_media.setCurrentSource(
                    Phonon.MediaSource(wav[self.feedback]))
                m_media.play()

class Slider(QWidget):
    XMAR = 20
    YMAR = 10
    def __init__(self, parent=None):
        super(Slider, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                       QSizePolicy.Fixed))
        self.cuadro = QRect(Slider.XMAR, Slider.YMAR, 400, 80)
        rielH = 20
        self.riel=QRect(Slider.XMAR,
                   (self.cuadro.height() - rielH) / 2 + Slider.YMAR,
                    self.cuadro.width(),
                    rielH)
        self._userClickX = None
        self._mouseListen = True
        self.test = Training('0.2 0.3 0.4 0.5 0.6 0.7 0.8')
        self.correctRate = self.test.rates[self.test.currentTrial]
        gwidth = self.xFromRate(2 * self.test.GREEN_ERROR) - Slider.XMAR
        ywidth = self.xFromRate(2 * self.test.YELLOW_ERROR) - Slider.XMAR
        self.check = CheckWidget(self.riel, gwidth, ywidth, self)

    def sizeHint(self):
        w = self.cuadro.width() + Slider.XMAR * 2 
        h = self.cuadro.height() + Slider.YMAR * 2
        return QSize(w, h)
    
    def xFromRate(self, r):
        x = self.riel.left() + r * self.riel.width() 
        return int(x)
    
    def rateFromX(self, x):
        r = (x - self.riel.left())/ self.riel.width()
        return float(r)
    
    def paintEvent(self, event=None):
        painter = QPainter(self)
        #Cuadro
        painter.drawRect(self.cuadro)
        #Riel
        painter.setBrush(self.palette().brush(QPalette.Midlight))
        painter.drawRect(self.riel)
        #Raya
        w = 10
        over =  20 
        h = self.riel.height() + 2 * over
        uppery = self.riel.top() - over
        if self._userClickX:
            upperx = self._userClickX - w / 2
            raya = QRect(upperx, uppery, w, h)
            painter.setBrush(self.palette().brush(QPalette.Button))
            painter.drawRect(raya)
        #print("form ha sido pintado")
        
    def mouseReleaseEvent(self,event):
        if self._mouseListen:
            self._mouseListen = False
            self.checkUserEvent(None, event.x())
            self.refresh()
            QTimer.singleShot(2000, self.nextGame)
            
    def checkUserEvent(self, time, x):
        min_val = self.riel.left()
        max_val = self.riel.right()
        x_in_riel = max(self.riel.left(), min(self.riel.right(), x))
        self._userClickX = x_in_riel
        rate = self.rateFromX(x_in_riel)
        self.test.writeAnswer(time, rate)
        self.check.feedback = self.test.rateCheck(rate)
        center = self.xFromRate(self.correctRate)
        self.check.setSpanLeft(center)
        self.check.playFeedbackSound()
        self.refresh()
        self.check.setVisible(True)
            
    def refresh(self):
        self.update()
    
    def nextGame(self):
        self.check.setVisible(False)
        self.correctRate= self.test.nextRate()
        self.parent().rateBox.setBars(1.0, self.correctRate)
        self.parent().rateBox.update()
        self._mouseListen = True
        
if __name__ == "__main__":
    app  = QApplication(sys.argv)
    form = Slider()
    form.show()
    sys.exit(app.exec_())
