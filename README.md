 
## Synopsis
Proporcion is a PyQt little game to train proportion perception in elementary 
students. The game was designed by my friend Camilo.


The script [fscreen_game.pyw](./fscreen_game.pyw) runs fullscreen, Esc key press to quit.
It shows a slider that waits for mouse click in order to 
record mouse x position and time. Inmediatly after slider interaction, the 
widget shows a reference area of what would be the better proportion selection and
plays a sound (currently desactivated) depending on how close the choice was from the current proportion.

## Code Example


### Data set and Training class

The game input data consist of two values lines that are readed into tuples (height, rate)
in `Training()` class:
```python
example_data = '''
1.0 0.5
1.0 0.25
0.6 0.5
0.6 0.75
0.6 0.25
0.3 0.8
0.3 0.2
0.3 0.5
0.3 0.75
1.0 0.2
1.0 0.7
1.0 0.3
0.5 0.5
'''[1:]
```

You can modify the class var `TEST_BREAKS` with a list of data index to trigger a user refresh pause in that data samples.

```python
class Training():
    GREEN_ERROR  = 0.05
    YELLOW_ERROR = 0.15
    #Pausas en [3, 6, 9, 12, ...,33]
    TEST_BREAKS  = range(3,36,3)...

    def getRates(self, data):
        '''Heights,rates from data string, reset trial counter.'''
        tupls_list = None
        if data:
            tupls_list = [ (float(h), float(r)) for h,r in[
                           tuple(l.split()) for l in data.splitlines() ]]
            self.currentTrial = 0
            print(tupls_list)
        return tupls_list
```
The class variables `GREEN_ERROR` and `YELLOW_ERROR` are used to eval the user's choice
error in terms of rate. They are also used in `CheckWidget(CustomRateWidget)` class to calculate the green
and yellow length of the feedback rectangles [see CheckBox below](./README.md#feedback-and-checkwidget-class).

### Rate representation and RateBox class

The `RateBox(CustomRateWidget)` widget has two rectangles (blue and red), whoes dimensions are 
changed with `setBars(height, rate)`. It's arguments are two rates,
one for the height of the blue bar, and the other for the proportion of the
red bar that is drawed in front of the blue.

```python
class RateBox(CustomRateWidget):
    ...
    
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
```


### User interaction and Slider class

The draw of the slider consist of a line (`riel`) and a button (`raya`) in the
`Slider(CustomRateWidget)`
class:
```python
class Slider(CustomRateWidget):
    ...
    def __init__(self, parent=None):
        ...
        self.riel=QLine(self.xFromRate(0),
                        self.yFromRate(0.5),
                        self.xFromRate(1),
                        self.yFromRate(0.5))
        ...
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
    ...
```
When user click release is generated, the custom signal `sliderMouseRelease(float)`
is emitted with the user selected rate:
```python
    ...
    def mouseReleaseEvent(self,event):
        if self._mouseListen:
            self._mouseListen = False
            self.checkUserEvent(None, event.x())
            self.update()
    
    def checkUserEvent(self, time, x):
        self._userClickX = max(self.riel.x1(), min(self.riel.x2(), x))
        rate = self.rateFromX(self._userClickX)
        self.sliderMouseRelease.emit(rate)
```


### Feedback and CheckWidget class

The reference area displayed after user interaction consist of two rectangles 
defined in `CheckWidget(CustomRateWidget)` class. First, the yellow and green
left sides are calculated whit a rate center value using `adjustRate(center)`:
```python
class CheckWidget(CustomRateWidget):
    ...
    def __init__(self, greenError=None, yellError=None, parent=None):
        ...
        self.gSemiWidth = self.wFromRate(greenError)
        self.ySemiWidth = self.wFromRate(yellError)
        ...
    
    def adjustRate(self, center):
        spanCenterX = self.xFromRate(center)
        self.yellLeftX  = spanCenterX - self.ySemiWidth
        self.greenLeftX = spanCenterX - self.gSemiWidth
```
Then, the rectangles are drawn:
```python
    ...
    
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
        ...
```


### Top level and central widget

The top level widget is `FullBox(QDialog)`:

```python
class FullBox(QDialog):
    def __init__(self, parent=None):
        super(FullBox, self).__init__(parent)
        p = self.palette()
        bgColor = QColor(179,179,179)
        p.setColor(self.backgroundRole(), bgColor)
        self.setPalette(p)
        self.setAutoFillBackground(True)
        self.whiteBox = WhiteBox()
        layout = QHBoxLayout()
        layout.addWidget(self.whiteBox)
        self.setLayout(layout)
```

`WhiteBox(CustomRateWidget)` instance is a fixed widget with fixed dimensions, parent of all the
dinamic widgets (slider, rateBox, checkBox and the photo boxes):

```python
class WhiteBox(QWidget):
    ...
    def __init__(self, parent=None):
        ...
        layout = QVBoxLayout()
        layout.addLayout(self.rateBoxLayout())
        layout.addStretch()
        layout.addLayout(self.sliderLayout())
        self.setLayout(layout)
```
Two methods in this class are used to update the widgets after user rate selection.
First the `onSliderMouseRelease(rate)` is called. After processing the user rate selected
and show feedback, a timer in this method launch the second method, `nextGame()` in order
to progress to the next game:
```python
    ...
    def onSliderMouseRelease(self, rate):
        self.test.writeAnswer(None, rate)
        self.check.feedback = self.test.rateCheck(rate)
        self.check.adjustRate(self.test.currentRate)
        #self.check.playFeedbackSound()
        self.check.setVisible(True)
        self.check.fbBlink(1600, 200)
        QTimer.singleShot(3000, self.nextGame)
        
    def nextGame(self):
        self.check.setVisible(False)
        self.test.toNextRate()
        self.rateBox.setBars(self.test.currentHeight,
                             self.test.currentRate)
        self.rateBox.update()
        self.slider._mouseListen = True
```


## Motivation

Proporcion is intended for test a brief training method that could assist in 
the student understanding of rational numbers. This is a paralel effort to test the 
game **performance** in PyQt (timing and space accuarcy of user interaction 
information).

## Installation

Requieres Python 3.4 installation and PyQt4 for python3. For windows user a 
minimal installation of PyQt is enough, remember during python3 installation to 
add c:\Python34\ to the system PATH enviromental variable. 

- In Windows **64bit**:  
  - [Python3 msi installer](https://www.python.org/ftp/python/3.4.3/python-3.4.3.amd64.msi)  
  - [PyQt4 for python3](http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/PyQt4-4.11.4-gpl-Py3.4-Qt4.8.7-x64.exe)  
- In Windows **32bit**:  
  - [Python3 msi installer](https://www.python.org/ftp/python/3.4.3/python-3.4.3.msi)  
  - [PyQt4 for python3](http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/PyQt4-4.11.4-gpl-Py3.4-Qt4.8.7-x32.exe)

Once you get the python/pyqt installation, you can download the [project zip](https://github.com/tomgranuja/Proporcion/archive/master.zip).


## Test

In order to test fullscreen just run [fscreen_game.pyw](./fscreen_game.pyw).
Remember Esc key press to quit.
The game will progress with the following height and rate sucession:
```python
(1.0, 0.5)
(1.0, 0.25)
(0.6, 0.5)
(0.6, 0.75)
(0.6, 0.25)
(0.3, 0.8)
(0.3, 0.2)
(0.3, 0.5)
(0.3, 0.75)
(1.0, 0.2)
(1.0, 0.7)
(1.0, 0.3)
(0.5, 0.5)
```
For windows user it can be run by double-clicking the file 
if the windows PATH environ contains python dir and pyqt dir (see Installation 
section above).

If fscreen_game.pyw is run from a command line interface, (CMD on windows) it 
shows in the terminal the current trial number, the time in milliseconds and
the rate value of the user mouse click release.

Use the time_test.py script to simulate some predefined user mouse releases
in the slider center spaced by 5 seconds, and compare time meassures.
Sice feedback time are setted to 1 second, you should expect elapsed times
round 4000 milliseconds after the first 5000 millisecond record.

## Contributors

Camilo Eureka Gouett, Salvador Gaviota.

