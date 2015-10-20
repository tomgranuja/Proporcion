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
        self._okval = 280
        self.greenWidth = 30
        self.yellWidth  = 40
        
    @property
    def okval(self):
        span = self.greenWidth + 2 * self.yellWidth
        min_val = self.riel.left() + span 
        max_val = self.riel.right() - span
        return random.randint(min_val, max_val)
        
    def sizeHint(self):
        return self.parent().sizeHint()
    
    def paintEvent(self, event=None):
        painter = QPainter(self)
        #Green
        w = self.greenWidth
        h = self.riel.height()
        uppery = self.riel.top()
        upperx = self.riel.left() + self.okval - w / 2
        green = QRect(upperx, uppery, w, h)
        painter.setBrush(QColor(0,128,0))
        painter.drawRect(green)
        
        #leftYell
        w = self.yellWidth
        leftYell = green.translated(-w, 0)
        leftYell.setWidth(w)
        painter.setBrush(QColor(222,205,135))
        painter.drawRect(leftYell)
        
        #rightYell
        dx = leftYell.width() + green.width()
        rightYell = leftYell.translated(dx , 0)
        painter.drawRect(rightYell)
        #print("check ha sido pintado")
        

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
            print(self._userval)
            self.update()
            self.check.setVisible(True)
    
    def pausa(self):
        self.check.setVisible(False)
        self._mouseListen = True
        
if __name__ == "__main__":
    app  = QApplication(sys.argv)
    form = Slider()
    form.show()
    sys.exit(app.exec_())
