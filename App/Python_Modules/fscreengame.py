#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from functools import partial
import uidmgr, tsequence, filelogger, inputdata

MEDIA_DIR = '../Media'
PRACTICE_STR = inputdata.tPractice
EXP_STR = inputdata.t_Exp_01
PRACTICE_ERRORS = (0.15, 0.05)
TEST_ERRORS     = PRACTICE_ERRORS
STIM_TIME       = [5000]
PARCIALS_TIME   = [4000]
FB_TIME         = [2000]
FB_BLINK_TIME   = [1000]
FB_BLINK_PERIOD = [ 150]
THANKS_TIME     = [4000]
FRUIT_BAR_RGB = (254, 0, 0)
path = 'intro_sesion1.png'
INTRO_PIXMAP     = '{}/{}'.format(MEDIA_DIR, path)
path = ['i_sesion1.png','d_sesion1.png']
SLIDER_PIXMAPS   = ['{}/{}'.format(MEDIA_DIR, p) for p in path ]
path = ['bad.png', 'good.png', 'excelent.png']
PARCIALS_PIXMAPS = ['{}/{}'.format(MEDIA_DIR, p) for p in path ]
path = ['bad_short.wav','good.wav', 'excelent.wav']
FB_WAVS          = ['{}/{}'.format(MEDIA_DIR, p) for p in path ]
TWO_VALS         = [0.15, 0.85]
CONTROL          = False
SESSION           = 1

def pixelFromRate(rate, t, o = 0):
    return int(round(rate*t)) + o

def rateFromPixel(pixel, t, o = 0):
    return (pixel - o) / t

class CustomRateWidget(QWidget):
    REF_WIDTH   = 0.5 * 1280 
    #REF_WIDTH  = 640
    #REF_HEIGHT = 660
    REF_HEIGHT = REF_WIDTH
    WIDTH  = 1.0 * REF_WIDTH
    HEIGHT = 1.03125 * REF_HEIGHT
    MARGIN = 0.03125 * REF_WIDTH
    def __init__(self, parent=None):
        super(CustomRateWidget, self).__init__(parent)
        fixedPol = QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.setSizePolicy(fixedPol)
        contentW = self.WIDTH - 2 * self.MARGIN
        contentH = self.HEIGHT - 2 * self.MARGIN
        self.wFromRate = partial(pixelFromRate, t=contentW)
        self.hFromRate = partial(pixelFromRate, t=contentH)
        self.xFromRate = partial(pixelFromRate,t=contentW, o=self.MARGIN)
        self.yFromRate = partial(pixelFromRate,t=contentH, o=self.MARGIN)
        self.rateFromX = partial(rateFromPixel,t=contentW, o=self.MARGIN)
    
    def sizeHint(self):
        return QSize(self.WIDTH, self.HEIGHT)

class BarsBox(CustomRateWidget):
    WIDTH  = 2 * 0.1875 * CustomRateWidget.REF_WIDTH
    HEIGHT = 0.7188 * CustomRateWidget.REF_HEIGHT
    #WIDTH  = 120
    #HEIGHT = 460
    def __init__(self, parent=None):
        super(BarsBox, self).__init__(parent)
        self.blueRect = None
        self.fruitRect  = None
        
    def setBars(self, rate, scale, width):
        blueHeight = 1.0
        height = 1 / scale
        if 0.0 < height  <= 1.0 and 0.0 < width <= 1.0:
            self.blueRect = QRect(
                         self.xFromRate((1-width)/2),
                         self.yFromRate(1-height),
                         self.wFromRate(width),
                         self.hFromRate(height)
                         )
            if 0.0 < rate <= 1.0:
                uppery = self.yFromRate(1 - rate * height)
                self.fruitRect = QRect(self.blueRect)
                self.fruitRect.setTop(uppery)
        
    def paintEvent(self, event=None):
        painter = QPainter(self)
        blueColor = QColor(85, 142, 213)
        fruitColor  = QColor(*FRUIT_BAR_RGB)
        if self.blueRect:
            painter.setBrush(blueColor)
            painter.drawRect(self.blueRect)
        if self.fruitRect:
            painter.setBrush(fruitColor)
            painter.drawRect(self.fruitRect)
            
class DotsBox(CustomRateWidget):
    '''Container for dots stimuli presentation.'''
    WIDTH  = 0.875 * CustomRateWidget.REF_WIDTH
    HEIGHT = 0.830 * CustomRateWidget.REF_HEIGHT
    def __init__(self, parent=None):
        super(DotsBox, self).__init__(parent)
        self.pixmp = None
        self.origin = self.calcUpperLeft()

    def calcUpperLeft(self):
        x, y = 0, 0
        if self.pixmp:
            x = (self.WIDTH - self.pixmp.width()) / 2
            y = (self.HEIGHT - self.pixmp.height()) / 2
        return QPointF(x, y)

    def setStim(self, rate, scale, pixpath):
        '''Discard rate, scale. Set image from pixpath.'''
        if pixpath:
            self.pixmp = QPixmap(pixpath)
            self.origin = self.calcUpperLeft()

    def paintEvent(self, event=None):
        if self.pixmp:
            painter = QPainter(self)
            painter.drawPixmap(self.origin, self.pixmp)

class RestBox(CustomRateWidget):
    WIDTH  = RateBox.WIDTH
    HEIGHT = RateBox.HEIGHT
    def __init__(self, parent=None):
        super(RestBox, self).__init__(parent)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        self.setAutoFillBackground(True)

class Slider(CustomRateWidget):
    WIDTH  = 0.6875 * CustomRateWidget.REF_WIDTH
    HEIGHT = 0.0938 * CustomRateWidget.REF_HEIGHT
    RIEL_WIDTH = 3
    #WIDTH  = 440
    #HEIGHT = 60
    sliderMousePress = pyqtSignal()
    def __init__(self, parent=None):
        super(Slider, self).__init__(parent)
        self.testTime = QTime()
        self.riel=QLine(self.xFromRate(0),
                        self.yFromRate(0.5),
                        self.xFromRate(1),
                        self.yFromRate(0.5))
        self._userClickX = None
        self._userRate = None
        self._userTime   = None
        self._mouseListen = True
        
    def paintEvent(self, event=None):
        painter = QPainter(self)
        pen = painter.pen()
        #Riel
        pen.setWidth(self.RIEL_WIDTH)
        painter.setPen(pen)
        painter.drawLine(self.riel)
        #Raya
        pen.setWidth(1)
        painter.setPen(pen)
        w = 4
        if self._userClickX:
            raya = QRect(self._userClickX - w / 2, 
                         0, 
                         w,
                         self.HEIGHT - 1)
            painter.setBrush(self.palette().brush(QPalette.Button))
            painter.drawRect(raya)
    
    def enterEvent(self, event=None):
        self.setMouseTracking(True)
    
    def leaveEvent(self, event=None):
        self.setMouseTracking(False)
    
    def mouseMoveEvent(self, event=None):
        if self._mouseListen:
            x = max(self.riel.x1(), min(self.riel.x2(), event.x()))
            self._userClickX = x
            self.update()
    
    def mousePressEvent(self,event):
        if self._mouseListen:
            self._mouseListen = False
            self._userTime = self.testTime.elapsed()
            self.checkUserEvent(event)
            self.update()
    
    def checkUserEvent(self, event):
        x = max(self.riel.x1(), min(self.riel.x2(), event.x()))
        self._userClickX = x
        self._userRate = self.rateFromX(self._userClickX)
        self.sliderMousePress.emit()

class TwoValSlider(Slider):
    def mouseMoveEvent(self, event=None):
        if self._mouseListen:
            x = event.x()
            MIN, MAX = range(2)
            if self.rateFromX(x) > 0.5:
                self._userClickX = self.xFromRate(TWO_VALS[MAX])
            else:
                self._userClickX = self.xFromRate(TWO_VALS[MIN])
            self.update()
    def checkUserEvent(self, event):
        x = event.x()
        MIN, MAX = range(2)
        if self.rateFromX(x) > 0.5:
            self._userClickX = self.xFromRate(TWO_VALS[MAX])
            self._userRate = self.rateFromX(self._userClickX)
        else:
            self._userClickX = self.xFromRate(TWO_VALS[MIN])
            self._userRate = self.rateFromX(self._userClickX)
        self.sliderMousePress.emit()


class CheckWidget(CustomRateWidget):
    WIDTH  = Slider.WIDTH
    HEIGHT = Slider.HEIGHT
    def __init__(self, greenError=None, yellError=None, parent=None):
        super(CheckWidget, self).__init__(parent)
        self.gSemiWidth = 0
        self.ySemiWidth = 0
        self.setErrors(greenError, yellError)
        self.audio = self.gameAudioConfig()
        self.yellLeftX  = None
        self.greenLeftX = None
        self.feedback   = None
        self.intermitent = False
        
    def setErrors(self, green, yell):
        if green:
            self.gSemiWidth = self.wFromRate(green)
        if yell:
            self.ySemiWidth = self.wFromRate(yell)
    
    def adjustRate(self, center):
        spanCenterX = self.xFromRate(center)
        self.yellLeftX  = spanCenterX - self.ySemiWidth
        self.greenLeftX = spanCenterX - self.gSemiWidth
    
    def fbBlink(self, time, period):
        self.timer = QTimer()
        self.timer.timeout.connect(self.fbBlinkStop)
        self.blinktimer = QTimer()
        self.blinktimer.timeout.connect(self.blink)
        self.timer.start(time)
        self.blinktimer.start(period)
        
    def fbBlinkStop(self):
        self.timer.stop()
        self.blinktimer.stop()
        self.intermitent = False
        self.update()
        
    def blink(self):
        self.intermitent = not self.intermitent
        self.update()
        
    def gameAudioConfig(self):
        audio = None
        if QSound.isAvailable():
            audio = 'qsound'
        else:
            from PyQt4.phonon import Phonon
            self.phononSource = Phonon.MediaSource
            self.m_media = Phonon.MediaObject()
            self.audioOut = Phonon.AudioOutput(Phonon.GameCategory)
            Phonon.createPath(self.m_media, self.audioOut)
            audio = 'phonon'
        return audio
    
    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        greenColor = QColor(0,128,0,150)
        yellowColor = QColor(222,205,135,150)
        outsideColor = QColor(0,0,0,0)
        h = self.hFromRate(1)
        top = self.xFromRate(0)
        #yellowBox
        if self.yellLeftX:
            painter.setBrush(yellowColor)
            yellowBox = QRect(self.yellLeftX, top, self.ySemiWidth * 2, h)
            painter.drawRect(yellowBox)
        #greenBox
        if self.greenLeftX:
            painter.setBrush(greenColor)
            dx = self.ySemiWidth - self.gSemiWidth
            green = yellowBox.translated(dx , 0)
            green.setWidth(self.gSemiWidth * 2)
            painter.drawRect(green)
        
        feedbackBox = QRect(self.xFromRate(0) - self.MARGIN,
                            self.yFromRate(0) - self.MARGIN,
                            self.WIDTH, 
                            self.HEIGHT)
        box_color = {'outside':outsideColor,
                     'in_yellow':yellowColor,
                      'in_green':greenColor}
        if self.feedback:
            painter.setBrush(box_color[self.feedback])
            if self.intermitent:
                painter.drawRect(feedbackBox)

    def playFeedbackSound(self):
        bad, good, excl = range(3)
        wavs = {'outside'  : FB_WAVS[bad],
                'in_yellow': FB_WAVS[good],
                'in_green' : FB_WAVS[excl]}
        wav = wavs.get(self.feedback, wavs['outside'])
        if self.audio == 'qsound':
            QSound.play(wav)
        elif self.audio == 'phonon':
            self.m_media.setCurrentSource(self.phononSource(wav))
            self.m_media.play()

class PartialWidget(CustomRateWidget):
    def __init__(self, parent=None):
        super(PartialWidget, self).__init__(parent)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(255,255,255))
        self.setPalette(p)
        self.setAutoFillBackground(True)
        self.greenBorder = QRect(self.xFromRate(0.5/4),
                                 self.yFromRate(0.5),
                                 self.wFromRate(0.5/3),
                                 self.hFromRate(0.5))
        dx = self.wFromRate(0.5/3 + 0.5/4)
        self.yellBorder  = self.greenBorder.translated( dx, 0 )
        self.outBorder   = self.yellBorder.translated(dx, 0)
        self.count = [ 0, 0, 0 ]
        self.bars  = [self.greenBorder, 
                      self.yellBorder, 
                      self.outBorder]
        self.barUnit = None

    def setBarUnit(self, dataLen):
        barMaxH = self.hFromRate(1) - 100
        self.barUnit = barMaxH / dataLen
    
    def setBars(self, feedback):
        GREEN, YELL, OUT = range(3)
        fbdic = {'in_green' : GREEN,
                 'in_yellow': YELL,
                 'outside'  : OUT}
        self.count[fbdic.get(feedback, OUT)] += 1
        tops = [ self.hFromRate(1) - c * self.barUnit
                for c in self.count ]
        [self.bars[i].setTop(tops[i]) for i,_ in enumerate(tops)]
        self.update()

    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        greenColor = QColor(0,128,0)
        yellowColor = QColor(222,205,135)
        outsideColor = QColor(179,179,179)
        bad, good, excl = range(3)
        #green
        painter.setBrush(greenColor)
        painter.drawRect(self.greenBorder)
        greenPix = QPixmap(PARCIALS_PIXMAPS[excl])
        greenX = self.greenBorder.left()
        greenY = self.greenBorder.top() - 100
        painter.drawPixmap(greenX, greenY, greenPix)
        #yell
        #if not CONTROL:
        painter.setBrush(yellowColor)
        painter.drawRect(self.yellBorder)
        yellPix = QPixmap(PARCIALS_PIXMAPS[good])
        yellX = self.yellBorder.left()
        yellY = self.yellBorder.top() - 100
        painter.drawPixmap(yellX, yellY, yellPix)
        #out
        painter.setBrush(outsideColor)
        painter.drawRect(self.outBorder)
        outPix = QPixmap(PARCIALS_PIXMAPS[bad])
        outX = self.outBorder.left()
        outY = self.outBorder.top() - 100
        painter.drawPixmap(outX, outY, outPix)
            
class RefreshWidget(CustomRateWidget):
    #WIDTH  = 1.0 * CustomRateWidget.REF_WIDTH
    #HEIGHT = 1.03125 * CustomRateWidget.REF_HEIGHT
    #WIDTH  = 640
    #HEIGHT = 660
    def __init__(self, wdgType=None, parent=None):
        super(RefreshWidget, self).__init__(parent)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(179,179,179))
        self.setPalette(p)
        self.setAutoFillBackground(True)
        self.setType = {
          'pract': partial(self.setMsgWdg,'¡Vamos a practicar!'),
          'ready':      partial(self.setMsgWdg,'¿Estás listo?'),
          'pause':      partial(self.setMsgWdg,'¿Descansamos?'),
          'parcials':   self.setPartialWdg,
          'thanks':     partial(self.setMsgWdg,'¡¡¡Gracias!!!')
        }
        self.setType.get(wdgType, self.setType['pract'])()
        layout = QVBoxLayout()
        layout.addWidget(self.wdg)
        self.setLayout(layout)
        
    def setPartialWdg(self):
        self.wdg = PartialWidget()

    def setMsgWdg(self, msg):
        self.wdg = QLabel()
        font = self.wdg.font()
        font.setPointSize(32)
        font.setBold(True)
        self.wdg.setFont(font)
        self.wdg.setText(msg)
        self.wdg.setAlignment(Qt.AlignCenter)

class IntroWidget(CustomRateWidget):
    def __init__(self, pixpath=None, parent=None):
        super(IntroWidget, self).__init__(parent)
        self.pixmp = QPixmap(pixpath)
        self.origin = self.calcUpperLeft()

    def calcUpperLeft(self):
        x = (self.WIDTH - self.pixmp.width()) / 2
        y = (self.HEIGHT - self.pixmp.height()) / 2
        return QPointF(x, y)

    def paintEvent(self, event=None):
        painter = QPainter(self)
        #painter.setPen(Qt.NoPen)
        #greenColor = QColor(0,128,0)
        painter.drawPixmap(self.origin, self.pixmp)

class WhiteBox(CustomRateWidget):
    #WIDTH  = 640
    #HEIGHT = 660
    def __init__(self, parent=None):
        super(WhiteBox, self).__init__(parent)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        self.setAutoFillBackground(True)
        layout = QVBoxLayout()
        layout.addLayout(self.rateBoxLayout())
        layout.addStretch()
        layout.addLayout(self.sliderLayout())
        self.setLayout(layout)

    def rateBoxLayout(self):
        self.rateBox = BarsBox()
        self.restBox = RestBox(self.rateBox)
        self.restBox.setVisible(False)
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.rateBox)
        layout.addStretch()
        return layout

    def sliderLayout(self):
        self.lPhotoBox = QLabel()
        self.rPhotoBox = QLabel()
        left, right = range(2)
        self.lPhotoBox.setPixmap(QPixmap(SLIDER_PIXMAPS[left]))
        self.rPhotoBox.setPixmap(QPixmap(SLIDER_PIXMAPS[right]))
        if CONTROL:
            self.slider = TwoValSlider()
        else:
            self.slider = Slider()
        self.check = CheckWidget(parent = self.slider)
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.lPhotoBox)
        layout.addWidget(self.slider)
        layout.addWidget(self.rPhotoBox)
        layout.addStretch()
        return layout
        
class UserChooser(QDialog):
    def __init__(self, parent=None):
        super(UserChooser, self).__init__(parent)
        self.label    = QLabel("Identificación")
        self.lineEdit = QLineEdit('ABC')
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok |
                                          QDialogButtonBox.Cancel)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        layout.addWidget(buttonBox)
        self.setLayout(layout)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.lineEdit.selectAll()
        self.lineEdit.setFocus()
        self.choosenUid = None
    
    def accept(self):
        userUpperText = self.lineEdit.text().upper()
        validation = uidmgr.isValidUid(userUpperText)
        if validation:
            self.choosenUid = userUpperText
            QDialog.accept(self)
        else:
            self.label.setText("¡¡Uid inválida!!")
            self.lineEdit.selectAll()
            self.lineEdit.setFocus()
            return
        
class FullBox(QDialog):
    def __init__(self, parent=None):
        super(FullBox, self).__init__(parent)
        self.setTheBackground(179,179,179)
        self.setUserSession()
        if self.userUid:
            print("Construyendo juego para {}".format(self.userUid))
            self.buildGame()

    def setTheBackground(self,r,g,b):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(r,g,b))
        self.setPalette(p)
        self.setAutoFillBackground(True)
        
    def setUserSession(self):
        dialog = UserChooser(self)
        self.userUid = None
        if dialog.exec_():
            self.userUid = dialog.choosenUid
            print("Usuario {} identificado.".format(self.userUid))
    
    def buildGame(self):
        self.whiteBox = WhiteBox()
        self.introWdg = IntroWidget(pixpath=INTRO_PIXMAP)
        self.slayout= QStackedLayout()
        self.slayout.dic = self.makeStckDic('pract',
                                            'ready',
                                            'pause',
                                            'parcials',
                                            'thanks',
                                            intro = self.introWdg,
                                            whiteBox = self.whiteBox)
        self.setLayout(self.slayout)
        self.gameSequenceConfig()
        self.initLoggers()
        self.gameStart()
    
    def makeStckDic(self, *args, intro, whiteBox):
        stckDic = {arg: RefreshWidget(arg) for arg in args}
        stckDic['whiteBox'] = whiteBox
        stckDic['intro'] = intro
        for k in stckDic:
            self.slayout.addWidget(stckDic[k])
        return stckDic
    
    def setLayout(self,ly):
        '''Reimplement to center 'ly' layout arg.'''
        layout = QVBoxLayout()
        hlayout = QHBoxLayout()
        hlayout.addStretch()
        hlayout.addLayout(ly)
        hlayout.addStretch()
        layout.addStretch()
        layout.addLayout(hlayout)
        layout.addStretch()
        super(FullBox, self).setLayout(layout)
    
    def gameSequenceConfig(self):
        if CONTROL:
                
            self.practice = tsequence.TwoValsTraining(PRACTICE_STR,
                            *PRACTICE_ERRORS, twoVals=TWO_VALS)
            self.test     = tsequence.TwoValsTraining(EXP_STR,
                            *TEST_ERRORS, twoVals=TWO_VALS)
        else:    
            self.practice = tsequence.Training(PRACTICE_STR,                     
                                               *PRACTICE_ERRORS)
            self.test     = tsequence.Training(EXP_STR, *TEST_ERRORS)
        self.sequence = tsequence.Sequence(self.practice, self.test)
        dic = { 'practSt'  : STIM_TIME[0],
                'testSt'   : STIM_TIME[-1],
                'practFb'  : FB_TIME[0],
                'testFb'   : FB_TIME[-1],
                'pparcials': PARCIALS_TIME[0],
                'tparcials': PARCIALS_TIME[-1],
                'thanks'   : THANKS_TIME[0],
                'fbBlinkTime'  : FB_BLINK_TIME[0],
                'fbBlinkPeriod':  FB_BLINK_PERIOD[0]
               }
        self.sequence.setTimeouts(dic)
        self.frIndex = (None, None)
        self.timeoutTimer = QTimer()
        self.timeoutTimer.setSingleShot(True)

    def initLoggers(self):
        if self.practice:
            pFilePath = filelogger.practiceLogPath(self.userUid,
                                                   sess=SESSION,
                                                   isCtrl=CONTROL)
            self.plogger = filelogger.Logger(pFilePath)
        if self.test:
            tFilePath = filelogger.testLogPath(self.userUid,
                                               sess=SESSION,
                                               isCtrl=CONTROL)
            self.tlogger = filelogger.Logger(tFilePath)

    def gameStart(self):
        sldr = self.whiteBox.slider
        sldr._mouseListen = False
        sldr.sliderMousePress.connect(self.onSliderMousePress)
        self.timeoutTimer.timeout.connect(self.onTimeOut)
        self.setNextFrame()

    def keyPressEvent(self, e):
        if self.spListen and e.key() == Qt.Key_Space:
            self.toListen = False
            self.spListen = False
            self.userTime = self.whiteBox.slider._userTime
            self.userRate = self.whiteBox.slider._userRate
            self.currentTrial = self.test.currentTrial
            self.setNextFrame()
        else:
            super(FullBox, self).keyPressEvent(e)
    
    def onSliderMousePress(self):
        if self.clkListen:
            self.toListen = False
            self.clkListen = False
            self.setNextFrame()
    
    def onTimeOut(self):
        if self.toListen:
            sldr = self.whiteBox.slider
            sldr._mouseListen = False
            sldr._userTime = sldr.testTime.elapsed()
            sldr._userRate = None
            self.setNextFrame()
    
    def setNextFrame(self):
        section = self.sequence.nextFrameSection()
        if section == None:
            self.finishGame()
            return
        _, frN = self.sequence.frIndex
        frame = self.sequence.framesDic[section][frN]
        training, logger = None, None
        if section == 'practice':
            training = self.practice
            logger = self.plogger
        elif section == 'test':
            training = self.test
            logger = self.tlogger
        sldr = self.whiteBox.slider
        if frame.mustDataWrite:
            n = training.currentTrial
            t, r = sldr._userTime, sldr._userRate
            logger.write(n, t, r)
        if frame.fbActive:
            testR, s, w = training.current 
            userR = sldr._userRate
            partialWdg = self.slayout.dic['parcials'].wdg
            check = self.whiteBox.check
            check.feedback = training.rateCheck(userR)
            if CONTROL:
                MIN, MAX = range(2)
                if testR > 0.5:
                    testR = TWO_VALS[MAX]
                else:
                    testR = TWO_VALS[MIN]
            check.adjustRate(testR)
            partialWdg.setBarUnit(len(training.data))
            partialWdg.setBars(check.feedback)
            check.playFeedbackSound()
            check.setVisible(True)
            check.fbBlink(self.sequence.tout['fbBlinkTime'], 
                          self.sequence.tout['fbBlinkPeriod'])
        else:
            self.whiteBox.check.setVisible(False)
        if frame.mustSetRate:
            sldr._userClickX = None
            training.toNextRate()
            gerror = training.gError
            yerror = training.yError
            self.whiteBox.check.setErrors(gerror, yerror)
            r, s, w = training.current
            self.whiteBox.rateBox.setBars(r, s, w)
        if frame.isStim:
            sldr._userClickX = None
            sldr._mouseListen = True
            sldr.testTime.start()
        self.setRefreshWdg(frame.refreshWdg)
        self.setListenFlags(frame.spListen, frame.clkListen)
        self.whiteBox.restBox.setVisible(frame.restIsVisible)
        self.setTimeout(frame.timeout)

    def setListenFlags(self, sp, clk):
        self.spListen = sp
        self.clkListen= clk

    def setRefreshWdg(self, wdg_id):
        if wdg_id:
            wdg = self.slayout.dic[wdg_id]
            self.slayout.setCurrentWidget(wdg)
        else:
            self.slayout.setCurrentWidget(self.whiteBox)
    
    def setTimeout(self, t):
        if t:
            self.timeoutTimer.setInterval(t)
            self.timeoutTimer.start()
            self.toListen = True

    def finishGame(self):
        self.close()

    
if __name__ == "__main__":
    app  = QApplication(sys.argv)
    form = FullBox()
    if form.userUid == None:
        print("No se identificó usuario, saliendo.")
        sys.exit(QDialog.Rejected)
    form.showFullScreen()
    sys.exit(app.exec_())
