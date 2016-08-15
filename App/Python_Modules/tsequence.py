#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

#TEST_PARTIALS = [4,10]
#TEST_PAUSES = [6]
TEST_PARTIALS   = range(9,36,9)
TEST_PAUSES     = [18]


class Training():
    def __init__(self, dataStr=None, 
                 yError = 0.15, 
                 gError = 0.05  ):
        self.currentTrial = None
        self.data = self.getRates(dataStr)
        self.yError = yError
        self.gError = gError
        #self.toNextRate()
        
    @property
    def current(self):
        '''(rate, scale, width) or (None, None, None) if outside data.'''
        try:
            rate, scale, width = self.data[self.currentTrial]
        except IndexError:
            print('Current trial outside data range')
            rate, scale, width = None, None, None
        return rate, scale, width
        
    def getRates(self, data):
        '''Rates, scales, widths from data string.'''
        float_tupls = []
        if data:
            for n, line in enumerate(data.splitlines()):
                w = '1.0'
                if len(line.split()) > 2:
                    w = line.split()[2]
                try:
                    r,s =  line.split()[:2]
                    rf,sf, wf = float(r), float(s), float(w)
                except:
                    msg = 'Error in data line {}: {}'
                    print(msg.format(n, repr(line)))
                    raise
                float_tupls.append( (rf, sf, wf) )
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
        RATE, SCALE, _ = range(3)
        if self.current[RATE]:
            if r or r == 0.0 and 0 <= r <= 1:
                result = 'outside'
                error = abs(r - self.current[RATE])
                if error <= self.yError:
                    result = 'in_yellow'
                if error <= self.gError:
                    result = 'in_green'
            else: print('None valid rate value to check')
        else: print('None currentRate to check')
        return result
        
    def __len__(self):
        return len(self.data)
    
    def __str__(self):
        if len(self.data) > 3:
            data = self.data[:3] + ['...']
        else:
            data = self.data
        dataStr = str(data)
        return 'Training({})'.format(dataStr)
        
class TwoValsTraining(Training):
    def __init__(self, dataStr=None, yError=0.15, gError=0.05, 
                 twoVals=[0.15,0.85]):
        super(TwoValsTraining,self).__init__(dataStr, yError, gError)
        MIN, MAX = range(2)
        self.twoValsMin = twoVals[MIN]
        self.twoValsMax = twoVals[MAX]
    def rateCheck(self, r=None):
        '''Check r error against current rate.'''
        result = None
        RATE, SCALE, _ = range(3)
        if self.current[RATE]:
            if r or r == 0.0 and 0 <= r <= 1:
                result = 'outside'
                if self.current[RATE] > 0.5:
                    checkRate = self.twoValsMax
                else:
                    checkRate = self.twoValsMin
                error = abs(r - checkRate)
                if error <= self.yError:
                    result = 'in_yellow'
                if error <= self.gError:
                    result = 'in_green'
            else:
                print('None valid rate value to check')
        else: print('None currentRate to check')
        return result

class DotsTraining(Training):
    @property
    def current(self):
        '''(rate, scale, ipath) or (None, None, None) if outside data.'''
        try:
            rate, scale, ipath = self.data[self.currentTrial]
        except IndexError:
            print('Current trial outside data range')
            rate, scale, ipath = None, None, None
        return rate, scale, ipath

    def getRates(self, data):
        '''rates, scales, ipaths from data string.'''
        mix_tupls = []
        if data:
            for n, line in enumerate(data.splitlines()):
                try:
                    r,s,p =  line.split()[:2] + line.split()[-1:]
                    rf,sf = float(r), float(s)
                except:
                    msg = 'Error in data line {}: {}'
                    print(msg.format(n, repr(line)))
                    raise
                mix_tupls.append( (rf, sf, p) )
        return mix_tupls

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
    def __init__(self,p = None, t = None):
        self.tout = {'practSt'  : 5000,
                     'testSt'   : 5000,
                     'practFb'  : 2000,
                     'testFb'   : 2000,
                     'pparcials': 4000,
                     'tparcials': 4000,
                     'thanks'   : 4000
                     }
        self.practObject = p
        self.testObject  = t
        self.createSequence()

    
    def setTimeouts(self,dic):
        for k in dic:
            self.tout[k] = dic[k]
        self.createSequence()
        
    def createSequence(self,toSection = None, toFrame = None):
        self.framesDic = {}
        self.addIntroToSequence()
        if self.practObject:
            self.addPracticeToSequence(self.practObject)
        if self.testObject:
            self.addTestToSequence(self.testObject)
        self.addThanksToSequence()
        self.frIndex = (toSection, toFrame)
        
    def addIntroToSequence(self):
        k = 'intro'
        self.overview = [k]
        frame = Frame(spListen = True, refreshWdg = 'intro')
        self.framesDic[k] = [frame]
    
    def addPracticeToSequence(self, tr_object):
        k = 'practice'
        self.overview.append(k)
        firstFrame = Frame(spListen = True, 
                           refreshWdg = 'pract')
        restFrame  = Frame(spListen = True, restIsVisible = True,
                           setRate = True)
        rateFrame  = Frame(clkListen = True, isStim = True,
                           timeout = self.tout['practSt'])
        fbFrame    = Frame(timeout = self.tout['practFb'], 
                           fbActive = True, dataWrite = True)
        partFrame  = Frame(refreshWdg = 'parcials', 
                           spListen = True)
        self.framesDic[k] = [firstFrame]
        self.pFrames = []
        for n, rate in enumerate(tr_object.data):
            self.pFrames.append('trial {:02}: {}'.format(n+1,rate))
            self.framesDic[k] += [ restFrame, rateFrame, fbFrame ]
        self.framesDic[k] += [ partFrame ]
        
    def addTestToSequence(self, tr_object):
        k = 'test'
        self.overview.append(k)
        firstFrame = Frame(spListen = True, 
                           refreshWdg = 'ready')
        restFrame  = Frame(spListen = True, restIsVisible = True,
                           setRate = True)
        rateFrame  = Frame(clkListen = True, isStim = True,
                           timeout = self.tout['testSt'])
        fbFrame    = Frame(timeout = self.tout['testFb'], 
                           fbActive = True, dataWrite = True)
        partFrame  = Frame(refreshWdg = 'parcials', 
                           timeout = self.tout['tparcials'])
        pauseFrame = Frame(refreshWdg = 'pause', spListen = True)
        self.framesDic[k] = [firstFrame]
        self.tFrames = []
        for n, rate in enumerate(tr_object.data):
            self.tFrames.append('trial {:02}: {}'.format(n+1,rate))
            if n in TEST_PAUSES:
                self.framesDic[k] += [partFrame]
                self.framesDic[k] += [pauseFrame, restFrame,
                                      rateFrame, fbFrame ]
            elif n in TEST_PARTIALS:
                self.framesDic[k] += [partFrame]
                self.framesDic[k] += [ restFrame, rateFrame, fbFrame ]
            else:
                self.framesDic[k] += [ restFrame, rateFrame, fbFrame ]
        self.framesDic[k] += [ partFrame ]
        
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
    import inputdata
    practice = Training(inputdata.dbgPractice)
    test     = Training(inputdata.dbgTest01)
    #practiceSeq = Sequence(practice)
    #testSeq = Sequence(t=test)
    bothSeq = Sequence(practice, test)
    for section in bothSeq.overview:
        for n, frame in enumerate(bothSeq.framesDic[section]):
            print('{} {:02}'.format(section.upper(),n))
            print(frame.frameAttrs(), '\n')
