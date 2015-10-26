#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

import sys, time
from threading import Timer
import fscreengame

class Form(fscreengame.FullBox):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.whiteBox.setTimers(fbtime      = 1000,
                        blinktime   =  500,
                        blinkperiod =  100)
    
    def showFullScreen(self):
        super(Form,self).showFullScreen()
        run_at_some_times()
    
def print_and_launch():
    print("Launched at", time.time())
    f()
def run_at_some_times():
     print('Test start time', time.time())
     Timer(5, print_and_launch, ()).start()
     Timer(10, print_and_launch, ()).start()

def f():
    rate = 0.325
    form.whiteBox.slider.sliderMouseRelease.emit(rate)

app  = fscreengame.QApplication(sys.argv)
form = Form()
form.showFullScreen()
sys.exit(app.exec_())