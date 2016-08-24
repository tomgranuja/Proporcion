#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

MOD_DIR = '../App/Python_Modules'
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
sys.path.append(MOD_DIR)
import fscreengame, inputdata

###########Configuración de la sesión##########################
SESSION          = 2
GAME             = ('dots', 'prop')
TEST_ERRORS      = (0.15, 0.05) ##Tamaño del feedback
INTRO_PIXMAP     = 'intro_sesion1.png' ##Imagen de intro
SLIDER_PIXMAPS   = ['i_sesion1.png','d_sesion1.png'] ##Extremos
FRUIT_BAR_RGB    = (254,0,0)   ##Color rgb de la barra
EXP_STR          = inputdata.n4col_data_img('session_prueba')
PRACTICE_STR     = inputdata.n4col_data_img('session_practice')
STIM_TIME        = [5000]
PARCIALS_TIME    = [4000]
FB_TIME          = [2000]
FB_BLINK_TIME    = [1000]
FB_BLINK_PERIOD  = [ 150]
THANKS_TIME      = [4000]
PARCIALS_PIXMAPS = ['bad.png'      ,'good.png', 'excelent.png']
FB_WAVS          = ['bad_short.wav','good.wav', 'excelent.wav']
TWO_VALS         = [0.01, 0.99]
TEST_PARTIALS    = range(9,36,9)
PRACTICE_ERRORS  = TEST_ERRORS
################################################################

def makeConfChanges():
    fscreengame.PRACTICE_STR     = PRACTICE_STR
    fscreengame.EXP_STR          = EXP_STR
    fscreengame.PRACTICE_ERRORS  = PRACTICE_ERRORS
    fscreengame.TEST_ERRORS      = TEST_ERRORS
    fscreengame.STIM_TIME        = STIM_TIME
    fscreengame.PARCIALS_TIME    = PARCIALS_TIME
    fscreengame.FB_TIME          = FB_TIME
    fscreengame.FB_BLINK_TIME    = FB_BLINK_TIME
    fscreengame.FB_BLINK_PERIOD  = FB_BLINK_PERIOD
    fscreengame.THANKS_TIME      = THANKS_TIME
    fscreengame.TWO_VALS         = TWO_VALS
    fscreengame.GAME             = GAME
    fscreengame.SESSION          = SESSION
    fscreengame.FRUIT_BAR_RGB    = FRUIT_BAR_RGB
    fscreengame.INTRO_PIXMAP     = INTRO_PIXMAP
    fscreengame.SLIDER_PIXMAPS   = SLIDER_PIXMAPS
    fscreengame.PARCIALS_PIXMAPS = PARCIALS_PIXMAPS
    fscreengame.FB_WAVS          = FB_WAVS
    fscreengame.tsequence.TEST_PARTIALS = TEST_PARTIALS

if __name__ == "__main__":
    makeConfChanges()
    app  = QApplication(sys.argv)
    form = fscreengame.FullBox()
    if form.userUid == None:
        print("No se identificó usuario, saliendo.")
        sys.exit(QDialog.Rejected)
    form.showFullScreen()
    sys.exit(app.exec_())
