#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

import sys, time
from threading import Timer
from PyQt4.QtTest import QTest
import fscreengame

class Form(fscreengame.FullBox):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.whiteBox.setTimers(fbtime      = 1000,
                        blinktime   =  500,
                        blinkperiod =  100)
    
    def showFullScreen(self):
        super(Form,self).showFullScreen()
        self.whiteBox.test.testTime.start()
        run_at_some_times()
    
def print_and_launch():
    print("Click release at", time.time())
    f()
def run_at_some_times():
     print('Test start time', time.time())
     for secs in range(5,50,5):
         Timer(secs, print_and_launch, ()).start()

def f():
    QTest.mouseRelease(
        form.whiteBox.slider,
        fscreengame.Qt.MouseButton(fscreengame.Qt.LeftButton))
    #form.whiteBox.slider.mouseReleaseEvent.emit(event)

app  = fscreengame.QApplication(sys.argv)
form = Form()
form.showFullScreen()
sys.exit(app.exec_())