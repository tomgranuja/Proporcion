#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

import sys, time
from PyQt4.QtTest import QTest
import fscreengame, tsequence

tsequence.TEST_PARTIALS = []
tsequence.TEST_PAUSES = []
fscreengame.PRACTICE_STR = ''


class ShortSequence(tsequence.Sequence):
    def createSequence(self,toSection = None, toFrame = None):
        self.framesDic = {}
        if self.testObject:
            self.addTestToSequence(self.testObject)
        self.addThanksToSequence()
        self.frIndex = (toSection, toFrame)
    
    def addTestToSequence(self, tr_object):
        k = 'test'
        self.overview = [k]
        restFrame  = tsequence.Frame(spListen = True, 
                                     restIsVisible = True,
                                     setRate = True)
        rateFrame  = tsequence.Frame(clkListen = True, 
                                     isStim = True)
        fbFrame    = tsequence.Frame(timeout = self.tout['testFb'], 
                                     fbActive = True, 
                                     dataWrite = True)
        self.framesDic[k] = []
        self.tFrames = []
        for n, rate in enumerate(tr_object.data):
            self.tFrames.append('trial {:02}: {}'.format(n+1,rate))
            self.framesDic[k] += [ restFrame, rateFrame, fbFrame ]

class Form(fscreengame.FullBox):
    def setUserSession(self):
        self.userUid = 'time_test'
    
    def gameSequenceConfig(self):
        self.practice = tsequence.Training(fscreengame.PRACTICE_STR,                     
                                           *fscreengame.PRACTICE_ERRORS)
        self.test     = tsequence.Training(fscreengame.EXP_STR,
                                           *fscreengame.TEST_ERRORS)
        self.sequence = ShortSequence(t = self.test)
        dic = { 'fbBlinkTime'  : fscreengame.FB_BLINK_TIME[0],
                'fbBlinkPeriod':  fscreengame.FB_BLINK_PERIOD[0]
               }
        self.sequence.setTimeouts(dic)
        self.frIndex = (None, None)
        self.timeoutTimer = fscreengame.QTimer()
        self.timeoutTimer.setSingleShot(True)
    
    def showFullScreen(self):
        super(Form,self).showFullScreen()
        #self.whiteBox.test.testTime.start()
        run_at_some_times()
    
def print_and_sp():
    print("Space at", time.time())
    f()

def print_and_click():
    print("Click at", time.time())
    g()

def run_at_some_times():
     print('Test start time', time.time())
     for secs in range(0,36*4,4):
         fscreengame.QTimer.singleShot(secs*1000, print_and_sp)
         fscreengame.QTimer.singleShot((secs + 1)*1000, print_and_click)
         
def f():
    QTest.keyEvent(QTest.Click, form, fscreengame.Qt.Key_Space)
    
def g():
    QTest.mousePress(
        form.whiteBox.slider,
        fscreengame.Qt.MouseButton(fscreengame.Qt.LeftButton))
    #form.whiteBox.slider.mouseReleaseEvent.emit(event)



app  = fscreengame.QApplication(sys.argv)
form = Form()
form.showFullScreen()
_ = input()
#sys.exit(app.exec_())