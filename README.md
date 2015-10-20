 
## Synopsis
Proporcion is a PyQt little game to train proportion perception in elementary 
students. The game was designed by my friend Camilo.


Right now it just contains a simple widget [slider_camilo.pyw](./slider_camilo.pyw).
It's a custom widget with an slider that waits for mouse click in order to 
record mouse x position and time. Inmediatly after slider interaction, the 
widget shows a reference area of what would be the better proportion selection.

## Code Example

The draw of the slider consist of two rectangles in the Slider class:
```python
#Riel
painter.setBrush(self.palette().brush(QPalette.Midlight))
painter.drawRect(self.riel)
#Boton
w = 10
over =  20 
h = self.riel.height() + 2 * over
uppery = self.riel.top() - over
upperx = self._userval - w / 2
but = QRect(upperx, uppery, w, h)
painter.setBrush(self.palette().brush(QPalette.Button))
painter.drawRect(but)
```

The reference area displayed after user interaction consist of three rectangles 
defined in CheckWidget class:
```python
#Green
w = self.greenWidth
h = self.riel.height()
uppery = self.riel.top()
upperx = self.riel.left() + self.okval - w / 2
green = QRect(upperx, uppery, w, h)
painter.setBrush(QColor(0,128,0))
painter.drawRect(green)
        
#leftYell
w = self.yellWidth
leftYell = green.translated(-w, 0)
leftYell.setWidth(w)
painter.setBrush(QColor(222,205,135))
painter.drawRect(leftYell)
        
#rightYell
dx = leftYell.width() + green.width()
rightYell = leftYell.translated(dx , 0)
painter.drawRect(rightYell)
```

The Slider class reimplement mouseReleaseEvent to show for certain amount of 
time the reference area. During this time, there is no processing of others 
mouseReleaseEvent:
```python
def mouseReleaseEvent(self,event):
    if self._mouseListen:
        self._mouseListen = False
        QTimer.singleShot(2000, self.pausa)
        min_val = self.riel.left()
        max_val = self.riel.right()
        x = max(self.riel.left(), min(self.riel.right(), event.x()))
        self._userval = x
        print(self._userval)
        self.update()
        self.check.setVisible(True)
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

At the moment there is only one [script to download](./slider_camilo.pyw).

## Test

Right now there is only one small interactive widget to test called 
[slider_camilo.pyw](./slider_camilo.pyw). For windows user it can be run by double-clicking the file 
if the windows PATH environ contains python dir and pyqt dir (see Installation 
section above).


If slider_camilo.pyw is run from a command line interface, (CMD on windows) it 
shows in the terminal the x value of the user mouse click release.

## Contributors

Camilo Eureka Gouett, Salvador Gaviota.

