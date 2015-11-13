#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

APP_DIR = '..'
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
sys.path.append(APP_DIR)
import fscreengame

#Probamos redefinir constante

fscreengame.tsequence.TEST_PARTIALS = [2,3]

if __name__ == "__main__":
    app  = QApplication(sys.argv)
    form = fscreengame.FullBox()
    if form.userUid == None:
        print("No se identificó usuario, saliendo.")
        sys.exit(QDialog.Rejected)
    form.showFullScreen()
    sys.exit(app.exec_())