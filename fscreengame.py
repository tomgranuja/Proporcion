#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

import sys, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from functools import partial
import uidmgr

#example_data = '''
#1.0 0.5
#1.0 0.25
#0.6 0.5
#0.6 0.75
#0.6 0.25
#0.3 0.8
#0.3 0.2
#0.3 0.5
#0.3 0.75
#1.0 0.2
#1.0 0.8
#1.0 0.5
#1.0 0.25
#1.0 0.75
#1.0 0.5
#1.0 0.5
#1.0 0.25
#0.6 0.5
#0.6 0.75
#0.6 0.25
#0.3 0.8
#0.3 0.2
#0.3 0.5
#0.3 0.75
#1.0 0.2
#1.0 0.8
example_data= '''
1.0 0.5
1.0 0.25
1.0 0.75
1.0 0.5
0.6 0.75
0.6 0.25
0.3 0.8
0.3 0.2
0.3 0.5
0.3 0.75
'''[1:]

practice_data = '''
0.75 0.25
0.75 0.75
0.75 0.5
'''[1:]


class Training():
    GREEN_ERROR  = 0.05
    YELLOW_ERROR = 0.15
    TEST_PARTIALS  = [2,4,6,8]
    TEST_PAUSE     = [5]
    #TEST_PARTIALS  = range(9,36,9)
    #TEST_PAUSE     = [18]
    
    def __init__(self, uid=None, 
                       dataStr=None, 
                       practiceStr = None, 
                       break_function=None):
        self.user = uidmgr.User(uid)
        self.initFileRecord()
        self.currentTrial = None
        self.dataStr = dataStr
        self.data = self.getRates(self.dataStr)
        self.practice = False
        if practiceStr:
            self.practice = True
            self.data = self.getRates(practiceStr)
        self.currentHeight= self.data[self.currentTrial][0]
        self.currentRate  = self.data[self.currentTrial][1]
        self.break_function = break_function
    
    def initFileRecord(self):
        lastSession = self.user.getLastSessionId()
        currentSession = uidmgr.nextSessionId(lastSession)
        with open(self.user.recFPath, 'a') as f:
            s = '#{}\n'.format(currentSession)
            f.write(s)
        
    def getRates(self, data):
        '''Heights,rates from data string, reset trial counter.'''
        tupls_list = None
        if data:
            tupls_list = [ (float(h), float(r)) for h,r in[
                           tuple(l.split()) for l in data.splitlines()
                           ]]
            self.currentTrial = 0
            print(tupls_list)
        return tupls_list
        
    def toNextRate(self):
        '''Next rate in list, update currentRate.'''
        if self.currentTrial != None:
            self.currentTrial += 1
            if self.practice:
                if self.currentTrial >= len(self.data):
                    self.practice = False
                    self.data = self.getRates(self.dataStr)
                    self.callBreakFunction('listo?')
            else:
                if self.currentTrial >= len(self.data):
                    print("Training finished, reseting trials.")
                    self.currentTrial = 0
                    self.callBreakFunction('gracias')
                if self.currentTrial in self.TEST_PARTIALS:
                    self.callBreakFunction('parciales')
                elif self.currentTrial in self.TEST_PAUSE:
                    self.callBreakFunction('pausa')
            self.currentHeight = self.data[self.currentTrial][0]
            self.currentRate = self.data[self.currentTrial][1]
        
    def rateCheck(self, r=None):
        result = None
        if r and 0 <= r <= 1:
            result = 'outside'
            error = abs(r - self.currentRate)
            if error <= Training.YELLOW_ERROR:
                result = 'in_yellow'
                if error <= Training.GREEN_ERROR:
                    result = 'in_green'
        return result
        
    def writeAnswer(self, time, rate):
        print(self.currentTrial, time, rate)
        with open(self.user.recFPath, 'a') as f:
            s = '{} {} {}\n'.format(self.currentTrial, time, rate)
            f.write(s)
    
    def callBreakFunction(self, btype=None):
        if self.break_function:
            self.break_function(btype)


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

class Slider(CustomRateWidget):
    WIDTH  = 0.6875 * CustomRateWidget.REF_WIDTH
    HEIGHT = 0.0938 * CustomRateWidget.REF_HEIGHT 
    #WIDTH  = 440
    #HEIGHT = 60
    sliderMouseRelease = pyqtSignal(bool)
    def __init__(self, timeoutTimer = QTimer(), 
                 testTime     = QTime(),
                 parent=None):
        super(Slider, self).__init__(parent)
        self.timeoutTimer = timeoutTimer
        self.testTime = testTime
        self.riel=QLine(self.xFromRate(0),
                        self.yFromRate(0.5),
                        self.xFromRate(1),
                        self.yFromRate(0.5))
        self._userClickX = None
        self._userTime   = None
        self._mouseListen = True
        #self.sliderMouseRelease = pyqtSignal(float)    
        
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
        self._userClickX = None
        self.update()
    
    def mouseMoveEvent(self, event=None):
        x = event.x()
        self._userClickX = max(self.riel.x1(), min(self.riel.x2(), x))
        self.update()
    
    def mouseReleaseEvent(self,event=QEvent(QEvent.User)):
        if self._mouseListen:
            self._mouseListen = False
            self.timeoutTimer.stop()
            event.time = self.testTime.elapsed()
            self.checkUserEvent(event)
            self.update()
    
    def checkUserEvent(self, event):
        t = None
        x = None
        user_release = False
        if event.type() == QEvent.MouseButtonRelease:
            user_release = True
            x = max(self.riel.x1(), min(self.riel.x2(), event.x()))
            t = event.time
        self._userClickX = x
        self._userTime = t
        self.sliderMouseRelease.emit(user_release)

class CheckWidget(CustomRateWidget):
    WIDTH  = Slider.WIDTH
    HEIGHT = Slider.HEIGHT
    def __init__(self, greenError=None, yellError=None, parent=None):
        super(CheckWidget, self).__init__(parent)
        self.setVisible(False)
        self.gSemiWidth = self.wFromRate(greenError)
        self.ySemiWidth = self.wFromRate(yellError)
        self.yellLeftX  = None
        self.greenLeftX = None
        self.feedback   = None
        self.intermitent = False
        
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
          'a_practicar': partial(self.setMsgWdg,'Vamos a practicar'),
          'listo?':      partial(self.setMsgWdg,'¿Estás listo?'),
          'pausa':       self.setIntroWdg,
          'parciales':   partial(self.setMsgWdg,'Tus resultados...'),
          'gracias':     partial(self.setMsgWdg,'Gracias...')
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
    def __init__(self, uid = None, break_function=None, parent=None):
        super(WhiteBox, self).__init__(parent)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        self.setAutoFillBackground(True)
        self.setTimers()
        self.test = Training(uid, 
                             example_data,
                             practice_data,
                             break_function)
        layout = QVBoxLayout()
        layout.addLayout(self.rateBoxLayout())
        layout.addStretch()
        layout.addLayout(self.sliderLayout())
        self.setLayout(layout)
        self.slider.sliderMouseRelease.connect(self.onSliderMouseRelease)
        self.updateTime()
        
    def rateBoxLayout(self):
        self.rateBox = RateBox()
        self.rateBox.setBars(self.test.currentHeight, 
                             self.test.currentRate)
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
        self.slider = Slider(timeoutTimer = self.timeoutTimer,
                             testTime     = self.testTime)
        self.check = CheckWidget(self.test.GREEN_ERROR,
                                 self.test.YELLOW_ERROR,
                                 parent = self.slider)
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.lPhotoBox)
        layout.addWidget(self.slider)
        layout.addWidget(self.rPhotoBox)
        layout.addStretch()
        return layout
    
    def onSliderMouseRelease(self, byUser=False):
        mseconds =self.slider._userTime
        rate = None
        if byUser:
            rate = self.slider.rateFromX(self.slider._userClickX)
        self.test.writeAnswer(mseconds, rate)
        self.check.feedback = self.test.rateCheck(rate)
        self.check.adjustRate(self.test.currentRate)
        #self.check.playFeedbackSound()
        self.check.setVisible(True)
        self.check.fbBlink(self.blinktime, self.blinkperiod)
        QTimer.singleShot(self.fbtime, self.nextGame)
        
    def nextGame(self):
        self.check.setVisible(False)
        self.test.toNextRate()
        self.rateBox.setBars(self.test.currentHeight,
                             self.test.currentRate)
        self.rateBox.update()
        self.slider._userClickX = None
        self.slider._mouseListen = True
        self.updateTime()
        
    def setTimers(self, fbtime      = 3000, 
                        blinktime   = 1600, 
                        blinkperiod =  200,
                        timeout     = 7000):
        self.fbtime = fbtime
        self.blinktime = blinktime
        self.blinkperiod = blinkperiod
        self.timeoutTimer = QTimer()
        self.timeoutTimer.setSingleShot(True)
        self.timeoutTimer.setInterval(timeout)
        self.timeoutTimer.timeout.connect(self.onTimeOut)
        self.testTime = QTime()
        
    def onTimeOut(self):
        self.slider.mouseReleaseEvent()
    
    def updateTime(self):
        self.testTime.start()
        self.timeoutTimer.start()
        
        
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
        userText = self.lineEdit.text().upper()
        validation = uidmgr.isValidUid(userText)
        if validation:
            self.choosenUid = userText
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
        self.whiteBox = WhiteBox(uid = self.userUid,
                                 break_function = self.takeABreak)
        self.slayout= QStackedLayout()
        self.slayout.dic = self.makeStckDic('intro',
                                            'a_practicar',
                                            'listo?',
                                            'pausa',
                                            'parciales',
                                            'gracias',
                                            whiteBox = self.whiteBox)
        wdg = self.slayout.dic['intro']
        if self.whiteBox.test.practice:
            wdg = self.slayout.dic['a_practicar']
        self.slayout.setCurrentWidget(wdg)
        self.setLayout(self.slayout)
        self.whiteBox.setTimers(fbtime      =  500, 
                                blinktime   =  200, 
                                blinkperiod =   50,
                                timeout     = 2000)
        QTimer.singleShot(1000,self.showWhite)
    
    def takeABreak(self, breakType=None):
        #self.whiteBox.timeoutTimer.stop()
        if breakType == None:
            breakType = 'intro'
        wdg = self.slayout.dic[breakType]
        self.slayout.setCurrentWidget(wdg)
        QTimer.singleShot(1000,self.showWhite)
    
    def showWhite(self):
        self.slayout.setCurrentWidget(self.slayout.dic['whiteBox'])
        self.whiteBox.updateTime()
        #QTimer.singleShot(5000,self.showRefresh)
        
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
        
    
if __name__ == "__main__":
    app  = QApplication(sys.argv)
    form = FullBox()
    if form.userUid == None:
        print("No se identificó usuario, saliendo.")
        sys.exit(QDialog.Rejected)
    form.showFullScreen()
    sys.exit(app.exec_())
