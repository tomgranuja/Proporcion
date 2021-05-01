 
## Synopsis
Proporcion is a PyQt little game to train intuitive proportional reasoning skills in students. 


During the game a set of two-colored bars will appear in the middle of the screen, representing a fruit juice made by a fruit concentrate (colored portion) and water (blue portion). Your task is to rank how intense is the juice flavor in each mixture, by mouse clicking on a horizontal slider located below the reference bar. In every trial, a visual and auditory feedback will tell you how good was your performance. You have to response as fast and accurate as possible.

Check [this short video](https://github.com/tomgranuja/Proporcion/raw/master/App/Media/quick_game.mkv) of the game. 

If you want to try it, see [installation](./README.md#installation) and [test](./README.md#test) instructions below.


## Code Example

The [fscreengame](./App/Python_Modules/fscreengame.py) module has the core of the game. It begins with some constant definitions that allow tweaking the game default settings:

### Media path

The path to the images and audios used in the game is splitted in a general dir path, `MEDIA_DIR`, and the different media names in that dir:

- `INTRO_PIXMAP` The game introduction image showed in the first frame.
- `SLIDER_PIXMAPS` List with the slider's left side and right side images.
- `PARCIALS_PIXMAPS` List with the "excelent", "good" and "outside" smileys showed in the performance graph pauses.
- `FB_WAVS` List with the "excelent", "good" and "outside" feedback sounds.

### Input data

The game trials present different ratios, heights and widths of the reference bars. The input numbers are stored in the [inputdata](./App/Python_Modules/inputdata.py) module and there are two constant for the input set selection, that contain `inputdata` module's strings:

- `PRACTICE_STR` A string with some practice trials inputs or a null string if the session don't need practice trials. Practice trials records are stored in a different file in the [log dir](./Logger/)
- `EXP_STR` A string with the experiment trials input. Also it can be a null string if there are no trials intended.

You can see the string format as three blank separated values separated by line breaks in the `inputdata` module:

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

The first column is the proportion stimuli (0 to 1). The second column is the scaling factor (i.e. ratio between the width of the response line to the height of the reference column) for example a scaling factor of 4 means that the vertical stimuli bar has a total height of a quarter (1/4) of the horizontal response line. The third column is the width factor (i.e. the width of the reference column).

### Performance feedback

After each slider click, the performance is categorized in one of three levels: "excelent/green", "good/yellow" and "outside/none". The actual performance is presented to the user with the respective color and sound. These categorizations are made by comparing the user's response error (distance between actual response and the perfect one), with the predefined thresholds to get into the "excelent/green" zone or to the "good/yellow" zone. For example, if your error response is say less than 5% you may receive an "excelent" categorization. These thresholds are organiced in two tuples:

- `PRACTICE_ERRORS` tuple with the "good/yellow" and "excelent/green" thresholds for the practice trials.
- `TEST_ERRORS` tuple with the "good/yellow" and "excelent/green" thresholds for the test trials.

### Game's different times

There are six parameters for defining different times in milliseconds:

- `STIM_TIME` The timeout for the user click after the reference bar presentation. If 0, the timeout is canceled and the game waits indefinitely for the user's click. A 'none' response is recorded for each user timeout.
- `PARCIALS_TIME` The displaying time of parcial and final results graphs. Again, if 0, the timeout is canceled.
- `FB_TIME` The time during which it is presented the feedback to the user.
- `FB_BLINK_TIME` The time during which the performance color blinks on the slider.
- `FB_BLINK_PERIOD` The "on" or "off" time of each blink (half the period of the blink).
- `THANKS_TIME` The final thanks frame time before game quits.

### Other parameters

- `FRUIT_BAR_RGB` RGB tuple for the color of the trials reference bars.
- `TWO_VALS` List of the two slider extreme rates allowed in the special control game (see [experimental test](./README.md#experimental-test-with-students)).
- `CONTROL` Boolean True if a control game is intended (see [experimental test](./README.md#experimental-test-with-students)).
- `SESSION` The number of the session for the record file identifier (see [experimental test](./README.md#experimental-test-with-students)).



## Motivation

Proporcion is intended for testing a brief training method that could help children in their understanding of rational numbers. Please do not consider this game as an educational tool yet. The present version is a pilot version, and is currently being tested for educational purposes. Our hope is to continue developing this software in parallel with the basic research that supports it.

## Installation

It requieres Python 3.4 installation and PyQt4 for python3. For windows user a 
minimal installation of PyQt is enough. Remember during python3 installation to 
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
Remember to press Esc key to quit.
The game will progress with the following ratio and heights values (no change in width in this short version):
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

### Full Training Sets 

The [game dir](./Games/), contains a collection of progressive sessions:
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

Control game's objective is slightly different than that of test games: instead of determining the flavor intensisty of the juice (represented by the two colored bars) you have to judge if the mixtures contain more fruit concentrate or more water. In this way the slider allows only extreme values to mark on (mark on the left (or right) end in case of less (or more) fruit concentrate than water). Thus, proportional reasoning is only acomplished by playing the test games. 

Each session begins with a user identification window waiting for a three chars identifier that must be asigned uniquely to each user across all sessions. This identifier is usefull to analyze anonimous data.
After that, there is a welcome frame and a three-trial practice which is only included in the first session. To progress in the game the student must press space bar to make a new juice mixture (a new bar) appear. In every trial, the user mark (position) on the slider plus the response time are recorded. 

The user data can be checked in the [log dir](./Logger/) by user id.
Each session consist of 36 trials, divided in two blocks of 18 trials with a brief pasue in the middle. Partial results graphs are shown every 9 trials to keep users engagement on the game. After completing the 36 trials, a final result graph is presented and a thanks frame.

### Time accuarcy test

There are multiple factors influencing the time record accuarcy of the game. Some of them involve the screen, keyboard and mouse respond delay. For this reason, a time error delay of a few milliseconds is likely to occur. The SO and other programs runing also affects the time record accuarcy.
We have made a [small time test](./App/Python_Modules/time_test.py) module. It is affected with the same time error that the the game is, so it can not be used to meassure the time accuarcy but is usefull to see the consistency of the records by simulating multiple slider mouse clicks separated by a 1000 ms period. Check the [log dir](./Logger/) after runing the time test and find the time test record. It should contain a session record with times a few milliseconds away from 1000.


## Contributors

Camilo Gouet, Salvador Gaviota.

