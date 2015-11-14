#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

APP_DIR = '..'
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
sys.path.append(APP_DIR)
import fscreengame, inputdata

#Probamos redefinir constante
fscreengame.INTRO_PIXMAP = '{}/{}'.format(APP_DIR,              
                                          fscreengame.INTRO_PIXMAP)
fscreengame.SLIDER_PIXMAPS = [ '{}/{}'.format(APP_DIR, w)
                                for w in fscreengame.SLIDER_PIXMAPS]
fscreengame.PARCIALS_PIXMAPS = [ '{}/{}'.format(APP_DIR, w)
                                for w in fscreengame.PARCIALS_PIXMAPS]
fscreengame.FB_WAVS = [ '{}/{}'.format(APP_DIR, w) 
                       for w in fscreengame.FB_WAVS]
fscreengame.SLIDER_PIXMAPS[0] = '{}/{}'.format(APP_DIR,'agua.png')
fscreengame.CONTROL = True
fscreengame.SESSION  = 5
fscreengame.PRACTICE_ERRORS = (0.0, 0.05)
fscreengame.FB_BLINK_PERIOD = [70]
fscreengame.STIM_TIME       = [2000, 1000]
fscreengame.PRACTICE_STR = ''
fscreengame.TEST_STR = inputdata.dbgTest01
fscreengame.tsequence.TEST_PARTIALS = [2,3]
fscreengame.filelogger.LOGDIR = '../Logger'

if __name__ == "__main__":
    app  = QApplication(sys.argv)
    form = fscreengame.FullBox()
    if form.userUid == None:
        print("No se identificó usuario, saliendo.")
        sys.exit(QDialog.Rejected)
    form.showFullScreen()
    sys.exit(app.exec_())