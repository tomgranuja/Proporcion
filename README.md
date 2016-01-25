 
## Synopsis
Proporcion is a PyQt little game to train proportion perception in elementary 
students. The game was designed by my friend Camilo.

The script [quick_game](./App/Media/quick_game.mkv) runs fullscreen, Esc key press to quit. It shows a reference bar and slider that waits for mouse click in order to record mouse x position and time. Inmediatly after slider interaction, the widget shows a reference area of what would be the better proportion selection and plays a sound depending on how close the choice was from the reference bar proportion.

If you want to try it, see installation and test instructions below.




## Code Example

The [fscreengame](./App/Python_Modules/fscreengame.py) module has the core of the game. It begins with some constant definitions that allow to tweak the game default settings:

### Media path

The path to the images and audios used in the game is splitted in a general dir path, `MEDIA_DIR`, and the different media names in that dir:

- `INTRO_PIXMAP` The game introduction image showed in the first frame.
- `SLIDER_PIXMAPS` List with the slider's left side and right side images.
- `PARCIALS_PIXMAPS` List with the "excelent", "good" and "outside" smileys showed in the performance graph pauses.
- `FB_WAVS` List with the "excelent", "good" and "outside" feedback sounds.

### Input data

The game trials present different rates, heights and widths of the reference bars. The input numbers are stored in the [inputdata](./App/Python_Modules/inputdata.py) module and there are two constant for the input set selection, they contains `inputdata` module's strings:

- `PRACTICE_STR` A string with some practice trials inputs or a null string if the session don't need practice trials. practice trials records are stored in a different file in the [log dir](./Logger/)
- `EXP_STR` A string with the experiment trials input. Also it can be a null string if there are no trials intended.

You can see the string format as three blank separated vals separated by line breaks in the `inputdata` module:

```python
'''0.21 1 1
0.76 1.5 0.5
0.01 1 0.5
0.5 1.5 1
0.95 1 0.5
0.03 1 0.5
0.5 1 0.5
0.16 1 1
0.76 4 1
0.26 4 0.5
0.21 4 1
0.61 1.5 1
0.8 1.5 0.5
0.03 1.5 0.5
0.03 4 0.5
0.43 1.5 0.5...
```

The first column is the rate (0 to 1), the second is the maximum height downscaling factor (1/height) and the third is the width factor.

### Performance feedback

After each slider click, the performance is categorized in one of three levels: "excelent/green", "good/yellow" and "outside/none". The actual performance is presented to the user with the respective color and a sound. These determination is made comparing the user rate selection error with the predefined umbrals for the "good/yellow" zone or the "excelent/green" zone.
These umbrals (the maximum diference from the current rate allowed) are organiced in two tuples:

- `PRACTICE_ERRORS` tuple with the "good/yellow" umbral and the "excelent/green" umbral for the practice trials.
- `TEST_ERRORS` tuple with the "good/yellow" umbral and the "excelent/green" umbral for the test trials.

### Game's different times

There are six constant for defining different times in milliseconds

- `STIM_TIME` The timeout for the user click after rate trial presentation. If 0, the timeout is canceled and the games wait indefinitely for the user. A 'none' rate is recorded for each user timeout.
- `PARCIALS_TIME` The time during the presentation of the parcials and finals results graphs. Again, if 0, the timeout is canceled.
- `FB_TIME` The time in wich is presented the feedback to the user selection
- `FB_BLINK_TIME` The time in wich the performance color blinks on the slider.
- `FB_BLINK_PERIOD` The "on" or "off" time of each blink (half the period of the blink).
- `THANKS_TIME` The final thanks frame time before game quit.

### Other constants

- `FRUIT_BAR_RGB` RGB tuple for the color of the trials reference rate bars.
- `TWO_VALS` List of the two slider extreme rates allowed in the special control game (see [experimental test](./README.md#experimental-test-with-students)).
- `CONTROL` Boolean True if a control game is intended (see [experimental test](./README.md#experimental-test-with-students)).
- `SESSION` The number of the session for the record file identifier (see [experimental test](./README.md#experimental-test-with-students)).



## Motivation

Proporcion is intended for test a brief training method that could assist in 
the student understanding of rational numbers. A pilot experiment was conducted with this software in november 2015 and the data recorded is beeing analized in order to verify Camilo's hypothesis.
Our hope is to continue the software development once we get the conclusions
from the pilot test.

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

In order to test fullscreen just run [quick_game](./quick_game.pyw).
Remember Esc key press to quit.
The game will progress with the following height and rate sucession:
```python
('0.26', '1.00')
('0.21', '0.67')
('0.61', '1.00')
('0.43', '1.00')
('0.7', '0.67')
('0.16', '0.25')
('0.01', '0.67')
('0.95', '0.67')
('0.43', '0.25')
('0.01', '0.25')
('0.61', '0.25')
('0.8', '0.25')
```
For windows user it can be run by double-clicking the file 
if the windows PATH environ contains python dir and pyqt dir
(see [Installation section](./README.md#installation) above).

### Experimental test with students

The [game dir](./Games/), contains a collection of progressive sessions to try with students. 
There are five test games:

- [sesion_01_T](./Games/sesion_01_T.pyw)
- [sesion_02_T](./Games/sesion_02_T.pyw)
- [sesion_03_T](./Games/sesion_03_T.pyw)
- [sesion_04_T](./Games/sesion_04_T.pyw)
- [sesion_05_T](./Games/sesion_05_T.pyw)

and five control games:

- [sesion_01_C](./Games/sesion_01_C.pyw)
- [sesion_02_C](./Games/sesion_02_C.pyw)
- [sesion_03_C](./Games/sesion_03_C.pyw)
- [sesion_04_C](./Games/sesion_04_C.pyw)
- [sesion_05_C](./Games/sesion_05_C.pyw)

The control games show a modified slider that only allows the extreme values
so the game objective is slighly different, to only select if the reference
has more "water" or "fruit". Thus, the real proportion training is only acomplished by playing the test games. You can split the student group into a "test" group and a "control" group to observe the differences.

This sessions begin with a user identification window waiting for a three chars identifier that must be asigned uniquely to each user across all sessions. This identifier is usefull to analyze anonimous data.
After entering the three chars identifier, there is some introduction pages and a three trial practice in the case of the first session. To progress in the game the student must press space bar until a new proportion is showed waiting for an slider click selection.
For each rate presented, the user performance is recorded after slider click.
The user data can be checked in the [log dir](./Logger/) by user id.
Each session consist of 36 trials plus some partial result graph frames and a brief pause on the middle. After completing the 36 trials, a final result graph is presented and a thanks frame.

### Time accuarcy test

There are multiple factors influencing the time record accuarcy of the test. Some of them involves the screen, keyboard and mouse respond delay. For this reason is probably to get a time error of a few milliseconds. The SO and other programs runing also affects the time record accuarcy.
We have made an [small time test](./App/Python_Modules/time_test.py) module. It is affected with the same time error of the game sessions so it can't be used to meassure the time accuarcy but is usefull to see the consistence of the record by simulating multiple slider mouse click separated by 1000 ms period. Check the [log dir](./Logger/) after runing the test and find the time test record. It should contain a session record with times a few milliseconds away from 1000.


## Contributors

Camilo Eureka Gouett, Salvador Gaviota.

