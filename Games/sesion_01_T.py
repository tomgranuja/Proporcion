#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

APP_DIR = '..'
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
sys.path.append(APP_DIR)
import fscreengame, inputdata

#Probamos redefinir constante

fscreengame.PRACTICE_ERRORS = (0.0, 0.05)
fscreengame.FB_BLINK_PERIOD = [70]
fscreengame.STIM_TIME       = [2000, 500]
#fscreengame.PRACTICE_STR = inputdata.tPractice
#fscreengame.TEST_STR = ''
fscreengame.tsequence.TEST_PARTIALS = [2,3]

if __name__ == "__main__":
    app  = QApplication(sys.argv)
    form = fscreengame.FullBox()
    if form.userUid == None:
        print("No se identificó usuario, saliendo.")
        sys.exit(QDialog.Rejected)
    form.showFullScreen()
    sys.exit(app.exec_())