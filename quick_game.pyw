#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

MOD_DIR = 'App/Python_Modules'
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
sys.path.append(MOD_DIR)
import fscreengame, inputdata, tsequence

tsequence.TEST_PARTIALS       = [4,10]
tsequence.TEST_PAUSES         = [6]
MEDIA_DIR                     = 'App/Media'
fscreengame.PRACTICE_STR      = ''
fscreengame.EXP_STR           = inputdata.dbg_sesion01
fscreengame.filelogger.LOGDIR = 'Logger'

path = 'intro_sesion1.png'
fscreengame.INTRO_PIXMAP      = '{}/{}'.format(MEDIA_DIR, path)
path = ['i_sesion1.png','d_sesion1.png']
fscreengame.SLIDER_PIXMAPS    = ['{}/{}'.format(MEDIA_DIR, p) 
                                 for p in path ]
path = ['bad.png', 'good.png', 'excelent.png']
fscreengame.PARCIALS_PIXMAPS  = ['{}/{}'.format(MEDIA_DIR, p) 
                                 for p in path ]
path = ['bad_short.wav','good.wav', 'excelent.wav']
fscreengame.FB_WAVS           = ['{}/{}'.format(MEDIA_DIR, p) 
                                 for p in path ]

class QuickSequence(tsequence.Sequence):
    def createSequence(self,toSection = None, toFrame = None):
        self.framesDic = {}
        if self.testObject:
            self.addTestToSequence(self.testObject)
        self.addThanksToSequence()
        self.frIndex = (toSection, toFrame)
        
    def addTestToSequence(self, tr_object):
        k = 'test'
        self.overview = [k]
        restFrame  = tsequence.Frame(timeout = 100, restIsVisible = True,
                           setRate = True)
        rateFrame  = tsequence.Frame(clkListen = True, isStim = True,
                           timeout = self.tout['testSt'])
        fbFrame    = tsequence.Frame(timeout = self.tout['testFb'], 
                           fbActive = True, dataWrite = True)
        partFrame  = tsequence.Frame(refreshWdg = 'parcials', 
                           timeout = self.tout['tparcials'])
        pauseFrame = tsequence.Frame(refreshWdg = 'pause', timeout = 3000)
        self.framesDic[k] = []
        self.tFrames = []
        for n, rate in enumerate(tr_object.data):
            self.tFrames.append('trial {:02}: {}'.format(n+1,rate))
            if n in tsequence.TEST_PAUSES:
                self.framesDic[k] += [partFrame]
                self.framesDic[k] += [pauseFrame, restFrame,
                                      rateFrame, fbFrame ]
            elif n in tsequence.TEST_PARTIALS:
                self.framesDic[k] += [partFrame]
                self.framesDic[k] += [ restFrame, rateFrame, fbFrame ]
            else:
                self.framesDic[k] += [ restFrame, rateFrame, fbFrame ]
        self.framesDic[k] += [ partFrame ]
        
class Form(fscreengame.FullBox):
    def setUserSession(self):
        self.userUid = 'quick_game'
    def gameSequenceConfig(self):
        self.practice = tsequence.Training(fscreengame.PRACTICE_STR,                     
                                           *fscreengame.PRACTICE_ERRORS)
        self.test     = tsequence.Training(fscreengame.EXP_STR,
                                           *fscreengame.TEST_ERRORS)
        self.sequence = QuickSequence(t = self.test)
        dic = { 'fbBlinkTime'  : fscreengame.FB_BLINK_TIME[0],
                'fbBlinkPeriod': fscreengame.FB_BLINK_PERIOD[0]
               }
        self.sequence.setTimeouts(dic)
        self.frIndex = (None, None)
        self.timeoutTimer = QTimer()
        self.timeoutTimer.setSingleShot(True)

    
if __name__ == "__main__":
    app  = QApplication(sys.argv)
    form = Form()
    form.showFullScreen()
    sys.exit(app.exec_())
