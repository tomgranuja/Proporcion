#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from functools import partial
import uidmgr, tsequence, filelogger


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

class RateBox(CustomRateWidget):
    WIDTH  = 0.1875 * CustomRateWidget.REF_WIDTH
    HEIGHT = 0.7188 * CustomRateWidget.REF_HEIGHT
    #WIDTH  = 120
    #HEIGHT = 460
    def __init__(self, parent=None):
        super(RateBox, self).__init__(parent)
        self.blueRect = None
        self.redRect  = None
        
    def setBars(self, height, rate):
        blueHeight = 1.0
        if 0.0 < height  <= 1.0:
            self.blueRect = QRect(
                         self.xFromRate(0),
                         self.yFromRate(1-height),
                         self.wFromRate(1),
                         self.hFromRate(height)
                         )
            if 0.0 < rate <= 1.0:
                uppery = self.yFromRate(1 - rate * height)
                self.redRect = QRect(self.blueRect)
                self.redRect.setTop(uppery)
        
    def paintEvent(self, event=None):
        painter = QPainter(self)
        blueColor = QColor(85, 142, 213)
        redColor  = QColor(254, 0, 0)
        if self.blueRect:
            painter.setBrush(blueColor)
            painter.drawRect(self.blueRect)
        if self.redRect:
            painter.setBrush(redColor)
            painter.drawRect(self.redRect)
            
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
    #WIDTH  = 440
    #HEIGHT = 60
    sliderMouseRelease = pyqtSignal()
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
        #Riel
        painter.drawLine(self.riel)
        #Raya
        w = 4
        if self._userClickX:
            raya = QRect(self._userClickX - w / 2, 
                         0, 
                         w,
                         self.HEIGHT)
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
    
    def mouseReleaseEvent(self,event):
        if self._mouseListen:
            self._mouseListen = False
            self._userTime = self.testTime.elapsed()
            self.checkUserEvent(event)
            self.update()
    
    def checkUserEvent(self, event):
        x = max(self.riel.x1(), min(self.riel.x2(), event.x()))
        self._userClickX = x
        self._userRate = self.rateFromX(self._userClickX)
        self.sliderMouseRelease.emit()

class CheckWidget(CustomRateWidget):
    WIDTH  = Slider.WIDTH
    HEIGHT = Slider.HEIGHT
    def __init__(self, greenError=None, yellError=None, parent=None):
        super(CheckWidget, self).__init__(parent)
        self.gSemiWidth = 0
        self.ySemiWidth = 0
        self.setErrors(greenError, yellError)
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
            
class RefreshWidget(CustomRateWidget):
    WIDTH  = 1.0 * CustomRateWidget.REF_WIDTH
    HEIGHT = 1.03125 * CustomRateWidget.REF_HEIGHT
    #WIDTH  = 640
    #HEIGHT = 660
    def __init__(self, wdgType=None, parent=None):
        super(RefreshWidget, self).__init__(parent)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.yellow)
        self.setPalette(p)
        self.setAutoFillBackground(True)
        self.setType = {
          'intro':       self.setIntroWdg,
          'pract': partial(self.setMsgWdg,'Vamos a practicar'),
          'ready':      partial(self.setMsgWdg,'¿Estás listo?'),
          'pause':       self.setIntroWdg,
          'parcials':   partial(self.setMsgWdg,'Tus resultados...'),
          'thanks':     partial(self.setMsgWdg,'Gracias...')
        }
        self.setType.get(wdgType, self.setType['intro'])()
        layout = QVBoxLayout()
        layout.addWidget(self.wdg)
        self.setLayout(layout)
        
    def setIntroWdg(self):
        bearpix = QPixmap('ninjabear.png')
        self.wdg = QLabel()
        self.wdg.setPixmap(bearpix)
        
    def setMsgWdg(self, msg):
        self.wdg = QLabel()
        font = self.wdg.font()
        font.setPointSize(32)
        font.setBold(True)
        self.wdg.setFont(font)
        self.wdg.setText(msg)

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
        self.rateBox = RateBox()
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
        self.lPhotoBox.setPixmap(QPixmap('cherri.png'))
        self.rPhotoBox.setPixmap(QPixmap('cherrimas.png'))
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
        self.slayout= QStackedLayout()
        self.slayout.dic = self.makeStckDic('intro',
                                            'pract',
                                            'ready',
                                            'pause',
                                            'parcials',
                                            'thanks',
                                            whiteBox = self.whiteBox)
        self.setLayout(self.slayout)
        self.gameSequenceConfig()
        self.initLoggers()
        self.gameStart()
    
    def makeStckDic(self, *args, whiteBox):
        stckDic = {arg: RefreshWidget(arg) for arg in args}
        stckDic['whiteBox'] = whiteBox
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
        self.practice = tsequence.Training(tsequence.practice_data)
        self.test     = tsequence.Training(tsequence.test_data)
        self.sequence = tsequence.Sequence(self.practice, self.test)
        self.frIndex = (None, None)
        self.timeoutTimer = QTimer()
        self.timeoutTimer.setSingleShot(True)
        
    def initLoggers(self):
        if self.practice:
            pFilePath = filelogger.practiceLogPath(self.userUid)
            self.plogger = filelogger.Logger(pFilePath)
        if self.test:
            tFilePath = filelogger.testLogPath(self.userUid)
            self.tlogger = filelogger.Logger(tFilePath)

    def gameStart(self):
        sliderRelease = self.whiteBox.slider.sliderMouseRelease
        sliderRelease.connect(self.onSliderMouseRelease)
        self.timeoutTimer.timeout.connect(self.onTimeOut)
        self.setNextFrame()

    def keyPressEvent(self, e):
        if self.spListen and e.key() == Qt.Key_Space:
            print('key press event')
            self.toListen = False
            self.spListen = False
            self.userTime = self.whiteBox.slider._userTime
            self.userRate = self.whiteBox.slider._userRate
            self.currentTrial = self.test.currentTrial
            self.setNextFrame()
        else:
            super(FullBox, self).keyPressEvent(e)
    
    def onSliderMouseRelease(self):
        if self.clkListen:
            self.toListen = False
            self.clkListen = False
            self.setNextFrame()
    
    def onTimeOut(self):
        if self.toListen:
            self.whiteBox.slider._mouseListen = False
            self.setNextFrame()
    
    def setNextFrame(self):
        section = self.sequence.nextFrameSection()
        if section == None:
            finishGame()
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
            h, testR = training.current 
            userR = sldr._userRate
            check = self.whiteBox.check
            check.feedback = training.rateCheck(userR)
            check.adjustRate(testR)
            #self.check.playFeedbackSound()
            check.setVisible(True)
            check.fbBlink(1000, 150)
        else:
            self.whiteBox.check.setVisible(False)
        if frame.mustSetRate:
            sldr._userClickX = None
            training.toNextRate()
            gerror = training.GREEN_ERROR
            yerror = training.YELLOW_ERROR
            self.whiteBox.check.setErrors(gerror, yerror)
            h, r = training.current
            self.whiteBox.rateBox.setBars(h, r)
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
        pass

    
if __name__ == "__main__":
    app  = QApplication(sys.argv)
    form = FullBox()
    if form.userUid == None:
        print("No se identificó usuario, saliendo.")
        sys.exit(QDialog.Rejected)
    form.showFullScreen()
    sys.exit(app.exec_())
