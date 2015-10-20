#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

import sys, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class CheckWidget(QWidget):
    def __init__(self, parent=None):
        super(CheckWidget, self).__init__(parent)
        self.riel = self.parent().riel
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                       QSizePolicy.Fixed))
        self.setVisible(False)
        self.greenWidth = 30
        self.yellWidth  = 40
        self.feedback   = 'outside'
        self.span = self.greenWidth + 2 * self.yellWidth
        min_val = int(self.riel.left() + self.span / 2) 
        max_val = int(self.riel.right() - self.span / 2)
        self._okvals = [ random.randint(min_val, max_val)
                         for n in range(20) ]
        print(self._okvals)
        
    @property
    def okval(self):
        return self._okvals[self.parent().trial]
        
    def sizeHint(self):
        return self.parent().sizeHint()
    
    def setFeedback(self, xval):
        distance = self.riel.width()
        if self.riel.contains(QPoint(xval,self.riel.top())):
            distance = abs(xval - self.okval)
        self.feedback = 'outside'
        if distance <= self.span / 2:
            self.feedback = 'in_yellow'
            if distance <= self.greenWidth / 2:
                self.feedback = 'in_green'
                
    def paintEvent(self, event=None):
        painter = QPainter(self)
        greenColor = QColor(0,128,0)
        yellowColor = QColor(222,205,135)
         
        #Green
        w = self.greenWidth
        h = self.riel.height()
        uppery = self.riel.top()
        upperx = self.okval - w / 2
        print(self.okval)
        green = QRect(upperx, uppery, w, h)
        painter.setBrush(greenColor)
        painter.drawRect(green)
        
        #leftYell
        w = self.yellWidth
        leftYell = green.translated(-w, 0)
        leftYell.setWidth(w)
        painter.setBrush(yellowColor)
        painter.drawRect(leftYell)
        
        #rightYell
        dx = leftYell.width() + green.width()
        rightYell = leftYell.translated(dx , 0)
        painter.drawRect(rightYell)
        #print("check ha sido pintado")
        
        #feedbackBox
        w = self.riel.width()
        h = self.riel.height() / 2
        uppery = self.parent().cuadro.top()
        upperx = self.riel.left()
        feedbackBox = QRect(upperx, uppery, w, h)
        box_color = {'outside':self.palette().brush(QPalette.Midlight),
                     'in_yellow':yellowColor,
                     'in_green':greenColor}
        painter.setBrush(box_color[self.feedback])
        painter.drawRect(feedbackBox)

class Slider(QWidget):
    XMAR = 20
    YMAR = 10
    def __init__(self, parent=None):
        super(Slider, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                       QSizePolicy.Fixed))
        self.cuadro = QRect(Slider.XMAR, Slider.YMAR, 560, 80)
        h = 20
        self.riel = QRect(Slider.XMAR,
                          (self.cuadro.height() - h) / 2 + Slider.YMAR,
                          self.cuadro.width(),
                          h)
        self._userval = self.cuadro.left() + self.cuadro.width() / 2
        self._mouseListen = True
        self.check = CheckWidget(self)
        self.trial = 0

    def sizeHint(self):
        w = self.cuadro.width() + Slider.XMAR * 2 
        h = self.cuadro.height() + Slider.YMAR * 2
        return QSize(w, h)
    
    def paintEvent(self, event=None):
        painter = QPainter(self)
        #Cuadro
        painter.drawRect(self.cuadro)
        #Riel
        painter.setBrush(self.palette().brush(QPalette.Midlight))
        painter.drawRect(self.riel)
        #Boton
        w = 10
        over =  20 
        h = self.riel.height() + 2 * over
        uppery = self.riel.top() - over
        upperx = self._userval - w / 2
        but = QRect(upperx, uppery, w, h)
        painter.setBrush(self.palette().brush(QPalette.Button))
        painter.drawRect(but)
        #print("form ha sido pintado")
        
    def mouseReleaseEvent(self,event):
        if self._mouseListen:
            self._mouseListen = False
            QTimer.singleShot(2000, self.pausa)
            min_val = self.riel.left()
            max_val = self.riel.right()
            x = max(self.riel.left(), min(self.riel.right(), event.x()))
            self._userval = x
            self.check.setFeedback(self._userval)
            print(self.trial, self._userval, self.check.feedback)
            self.update()
            self.check.setVisible(True)
            
    
    def pausa(self):
        self.check.setVisible(False)
        self.trial += 1
        self._mouseListen = True
        
if __name__ == "__main__":
    app  = QApplication(sys.argv)
    form = Slider()
    form.show()
    sys.exit(app.exec_())
