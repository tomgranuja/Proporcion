#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

TEST_PARTIALS = [4,10]
TEST_PAUSES = [6]
#TEST_PARTIALS   = range(9,36,9)
#TEST_PAUSES     = [18]

test_data = '''
0.21 1 1
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
0.43 1.5 0.5
0.95 4 1
0.7 4 1
0.76 1 0.5
0.7 1 0.5
0.26 1.5 1
0.8 1 0.5
0.16 1.5 1
0.5 4 1
0.26 1 1
0.21 1.5 0.5
0.61 1 1
0.43 1 1
0.7 1.5 1
0.16 4 0.5
0.01 1.5 0.5
0.95 1.5 1
0.43 4 0.5
0.01 4 1
0.61 4 0.5
0.8 4 1
'''[252:]

practice_data = '''
0.6 1 0.5
0.4 1 1
0.55 1 0.5
'''[20:]
#practice_data = None

class Training():
    GREEN_ERROR  = 0.05
    YELLOW_ERROR = 0.15
    def __init__(self, dataStr=None):
        self.currentTrial = None
        self.data = self.getRates(dataStr)
        #self.toNextRate()
        
    @property
    def current(self):
        '''(height, rate) or (None, None) if outside data.'''
        try:
            height, rate, width = self.data[self.currentTrial]
        except IndexError:
            print('Current trial outside data range')
            height, rate, width = None, None, None
        return height, rate, width
        
    def getRates(self, data):
        '''Heights,rates from data string.'''
        float_tupls = []
        if data:
            for n, line in enumerate(data.splitlines()):
                try:
                    r,s,w =  line.split()
                    hf,rf, wf = 1/float(s), float(r), float(w)
                except:
                    msg = 'Error in data line {}: {}'
                    print(msg.format(n, repr(line)))
                    raise
                float_tupls.append( (hf, rf, wf) )
        return float_tupls
        
    def toNextRate(self):
        '''Update currentTrial to the next one.'''
        if self.currentTrial == None:
            self.currentTrial = 0
        else:
            self.currentTrial += 1
        if self.currentTrial >= len(self.data):
            print('Training finished')
        
    def rateCheck(self, r=None):
        '''Check r error against current rate.'''
        result = None
        HEIGHT, RATE, WIDTH = range(3)
        if self.current[RATE]:
            if r or r == 0.0 and 0 <= r <= 1:
                result = 'outside'
                error = abs(r - self.current[RATE])
                if error <= Training.YELLOW_ERROR:
                    result = 'in_yellow'
                    if error <= Training.GREEN_ERROR:
                        result = 'in_green'
            else: print('None valid rate value to check')
        else: print('None currentRate to check')
        return result
        
    def __str__(self):
        if len(self.data) > 3:
            data = self.data[:3] + ['...']
        else:
            data = self.data
        dataStr = str(data)
        return 'Training({})'.format(dataStr)
        
class Frame():
    def __init__(self, spListen = False, clkListen = False,
                 isStim = False, timeout = 0, fbActive = False,
                 restIsVisible = False, refreshWdg = None,
                 setRate = False, dataWrite = False):
        self.spListen      = spListen
        self.clkListen     = clkListen
        self.isStim        = isStim
        self.timeout       = timeout
        self.fbActive      = fbActive
        self.restIsVisible = restIsVisible
        self.refreshWdg    = refreshWdg
        if self.refreshWdg:
            self.restIsVisible = True
            self.fbActive      = False
        self.mustSetRate       = setRate
        self.mustDataWrite     = dataWrite
    
    def frameAttrs(self):
        ss =  ['Special wdg : {}'.format(self.refreshWdg)]
        ss += ['Space Listen: {}'.format(self.spListen)]
        ss += ['Clic Listen : {}'.format(self.clkListen)]
        ss += ['Show stimul : {}'.format(self.isStim)]
        ss += ['Timeout ms  : {}'.format(self.timeout)]
        ss += ['Feedbk Activ: {}'.format(self.fbActive)]
        ss += ['Estim. rest : {}'.format(self.restIsVisible)]
        ss += ['File write  : {}'.format(self.mustDataWrite)]
        ss += ['Set rates   : {}'.format(self.mustSetRate)]
        return '\n'.join(ss)
    
class Sequence():
    def __init__(self,p = None, t = None, **kargs):
        self.framesDic = {}
        self.addIntroToSequence()
        self.tout = {'practSt'  : 5000,
                     'testSt'   : 5000,
                     'practFb'  : 2000,
                     'testFb'   : 2000,
                     'pparcials': 4000,
                     'tparcials': 4000,
                     'thanks'   : 4000
                     }
        self.setTimeouts(kargs)
        if p:
            self.addPracticeToSequence(p)
        if t:
            self.addTestToSequence(t)
        self.addThanksToSequence()
        self.frIndex = (None, None)
    
    def setTimeouts(self,kargs):
        for k in kargs:
            self.tout[k] = kargs[k]
    
    def addIntroToSequence(self):
        k = 'intro'
        self.overview = [k]
        frame = Frame(spListen = True, refreshWdg = 'intro')
        self.framesDic[k] = [frame]
    
    def addPracticeToSequence(self, tr_object):
        k = 'practice'
        self.overview.append(k)
        firstFrame = Frame(spListen = True, refreshWdg = 'pract',
                           setRate = True)
        rateFrame  = Frame(clkListen = True, isStim = True,
                           timeout = self.tout['practSt'])
        fbFrame    = Frame(timeout = self.tout['practFb'], 
                           fbActive = True, dataWrite = True)
        restFrame  = Frame(spListen = True, restIsVisible = True,
                           setRate = True)
        partFrame  = Frame(refreshWdg = 'parcials', 
                           timeout = self.tout['pparcials'])
        self.framesDic[k] = [firstFrame]
        self.pFrames = []
        for n, rate in enumerate(tr_object.data):
            self.pFrames.append('trial {:02}: {}'.format(n+1,rate))
            self.framesDic[k] += [ rateFrame, fbFrame, restFrame ]
        self.framesDic[k][-1] = partFrame
        
    def addTestToSequence(self, tr_object):
        k = 'test'
        self.overview.append(k)
        firstFrame = Frame(spListen = True, refreshWdg = 'ready',
                           setRate = True)
        rateFrame  = Frame(clkListen = True, isStim = True,
                           timeout = self.tout['testSt'])
        fbFrame    = Frame(timeout = self.tout['testFb'], 
                           fbActive = True, dataWrite = True)
        restFrame  = Frame(spListen = True, restIsVisible = True,
                           setRate = True)
        partFrame  = Frame(refreshWdg = 'parcials', 
                           timeout = self.tout['tparcials'])
        pauseFrame = Frame(refreshWdg = 'pause', spListen = True,
                           setRate = True)
        self.framesDic[k] = [firstFrame]
        self.tFrames = []
        for n, rate in enumerate(tr_object.data):
            self.tFrames.append('trial {:02}: {}'.format(n+1,rate))
            if n in TEST_PAUSES:
                self.framesDic[k][-1] = partFrame
                self.framesDic[k] += [pauseFrame, rateFrame,
                                     fbFrame, restFrame]
            elif n in TEST_PARTIALS:
                self.framesDic[k][-1] = partFrame
                self.framesDic[k] += [ restFrame, rateFrame,
                                     fbFrame, restFrame]
            else:
                self.framesDic[k] += [ rateFrame, fbFrame, restFrame ]
        self.framesDic[k][-1] = partFrame
        
    def addThanksToSequence(self):
        k = 'thanks'
        self.overview.append(k)
        self.framesDic[k]= [Frame(refreshWdg = k, 
                                  timeout = self.tout['thanks'])]

    def nextFrameSection(self):
        frSec, frN = self.frIndex
        if frN == None:
            frSec, frN = (0, 0)
        else:
            frN += 1
        sectionName = self.overview[frSec]
        if frN >= len(self.framesDic[sectionName]):
            frN = 0
            frSec += 1
            if frSec >= len(self.overview):
                sectionName = None
            else:
                sectionName = self.overview[frSec]
        self.frIndex = (frSec, frN)
        if sectionName:
            print('{} {:02}'.format(sectionName,frN))
            print(self.framesDic[sectionName][frN].frameAttrs(), '\n')
        return sectionName


    def __str__(self):
        return 'Sequence: {}'.format(str(self.overview))

def sequenceMap(seq):
    mapList = []
    for section in seq.overview:
        if section == 'intro':
            mapList.append('-Introduction')
        elif section == 'practice':
            mapList.append('-Practice:')
            for rate in seq.pFrames:
                mapList.append('    -{}'.format(rate))
        elif section == 'test':
            mapList.append('-Test:')
            for rate in seq.tFrames:
                mapList.append('    -{}'.format(rate))
        elif section == 'thanks':
            mapList.append('-Thanks')
    return '\n'.join(mapList)

if __name__ == "__main__":
    practice = Training(practice_data)
    test     = Training(test_data)
    practiceSeq = Sequence(practice)
    testSeq = Sequence(t=test)
    bothSeq = Sequence(practice, test)
    n = 0
    while n < len(bothSeq.allFrames):
        print('Frame {}:'.format(n))
        print(bothSeq.allFrames[n].frameAttrs())
        print('')
        n += 1