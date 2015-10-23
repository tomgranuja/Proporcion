 
## Synopsis
Proporcion is a PyQt little game to train proportion perception in elementary 
students. The game was designed by my friend Camilo.


The script [fscreen_game.pyw](./fscreen_game.pyw) runs fullscreen, Esc key press to quit.
It shows a slider that waits for mouse click in order to 
record mouse x position and time. Inmediatly after slider interaction, the 
widget shows a reference area of what would be the better proportion selection and
plays a sound depending on how close the choice was from the current proportion.

## Code Example

### `slider` module

The draw of the slider consist of two rectangles in the `Slider(QWidget)` class defined
in slider.py:
```python
painter = QPainter(self)
#Cuadro
painter.drawRect(self.cuadro)
#Riel
painter.setBrush(self.palette().brush(QPalette.Midlight))
painter.drawRect(self.riel)
#Raya
w = 10
over =  20 
h = self.riel.height() + 2 * over
uppery = self.riel.top() - over
if self._userClickX:
    upperx = self._userClickX - w / 2
    raya = QRect(upperx, uppery, w, h)
    painter.setBrush(self.palette().brush(QPalette.Button))
    painter.drawRect(raya)
```

The reference area displayed after user interaction consist of two rectangles 
defined in `CheckWidget(QWidget)` class:
```python
painter = QPainter(self)
greenColor = QColor(0,128,0)
yellowColor = QColor(222,205,135)

h = self.riel.height()
top = self.riel.top()
if self.spanLeft:
    painter.setBrush(yellowColor)
    #yellowBox
    yellowBox = QRect(self.spanLeft, top, self.yellWidth, h)
    painter.drawRect(yellowBox)
    #greenBox
    painter.setBrush(greenColor)
    dx = (self.yellWidth - self.greenWidth)/ 2
    green = yellowBox.translated(dx , 0)
    green.setWidth(self.greenWidth)
    painter.drawRect(green)
```

The `Slider` class reimplement `QWidget.mouseReleaseEvent()` to send feedback to the user for certain amount of 
time with the reference area and a sound. During this time, there is no processing of further mouse events:
```python
def mouseReleaseEvent(self,event):
    if self._mouseListen:
        self._mouseListen = False
        self.checkUserEvent(None, event.x())
        self.refresh()
        QTimer.singleShot(2000, self.nextGame)
```

The `Training()` class manage the game information. On initialization, loads a float list with the proportions to be tested:

```python
def __init__(self, rates_data=None):
    self.currentTrial = None
    self.rates = self.getRates(rates_data)

def getRates(self, data):
    '''Rates from data string, reset trial counter.'''
    float_list = None
    if data:
        float_list = [ float(n) for n in data.split() ]
        self.currentTrial = 0
        print(float_list)
    return float_list
```

Also in `Training` class are defined two class vars, `Training.GREEN_ERROR` and `Trainig.YELLOW_ERROR` to control the reference feedback box width and sound played for the user uppon slider interaction.

### Script fscreen_game.pyw

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

`WhiteBox()` instance is a fixed widget with fixed dimensions, parent of all the
dinamic widgets (slider, rateBox and the photo boxes):

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

The `rateBox` widget has two rectangles (blue and red), whoes dimensions are 
changed with `rateBox.setBars(height, rate)`. It's arguments are two rates,
one for the height of the blue bar, and the other for the proportion of the
red bar that is drawed in front of the blue.

```python
def setBars(self, height, rate):
    blueHeight = 1.0
    if 0.0 < height  <= 1.0:
        blueHeight = height * (self.height() - RateBox.MARGIN * 2)
        self.blueRect = QRect(
                        RateBox.MARGIN,
                        self.height() - blueHeight - RateBox.MARGIN,
                        self.width() - 2 * RateBox.MARGIN,
                        blueHeight
                        )
        if 0.0 < rate <= 1.0:
            redHeight = rate * blueHeight
            self.redRect = QRect(
                        RateBox.MARGIN,
                        self.height() - redHeight - RateBox.MARGIN,
                        self.width() - 2 * RateBox.MARGIN,
                        redHeight
                        )
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
The game will progress with a rate sucession from 0.2 to 0.8. The rateBox bars
are still fixed at a 0.5 rate, and maximum height (1.0).
(it requieres the three wavs from the project dir and the `slider` module).
For windows user it can be run by double-clicking the file 
if the windows PATH environ contains python dir and pyqt dir (see Installation 
section above).

If fscreen_game.pyw is run from a command line interface, (CMD on windows) it 
shows in the terminal the current trial number, the time (not yet, just 'None') and the x value of the user mouse click release.

## Contributors

Camilo Eureka Gouett, Salvador Gaviota.

