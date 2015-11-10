#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

TEST_PARTIALS   = [2,4,6,8,10]
TEST_PAUSES     = [6]

test_data = '''
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
1.0 0.8
1.0 0.5
1.0 0.25
1.0 0.75
1.0 0.5
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
1.0 0.8
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
'''[203:]

practice_data = '''
0.75 0.25
0.75 0.75
0.75 0.5
'''[1:]
#practice_data = None

class Training():
    GREEN_ERROR  = 0.05
    YELLOW_ERROR = 0.15
    def __init__(self, dataStr=None):
        self.currentTrial = None
        self.data = self.getRates(dataStr)
        self.toNextRate()
        
    @property
    def current(self):
        '''(height, rate) or (None, None) if outside data.'''
        try:
            height, rate = self.data[self.currentTrial]
        except IndexError:
            print('Current trial outside data range')
            height, rate = None, None
        return height, rate
        
    def getRates(self, data):
        '''Heights,rates from data string.'''
        float_tupls = []
        if data:
            for n, line in enumerate(data.splitlines()):
                try:
                    h,r =  line.split()
                    hf,rf = float(h), float(r)
                except:
                    msg = 'Error in data line {}: {}'
                    print(msg.format(n, repr(line)))
                    raise
                float_tupls.append( (hf, rf) )
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
        HEIGHT, RATE = range(2)
        if self.current[RATE]:
            if r and 0 <= r <= 1:
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
                 timeout = 0, restIsVisible = False, 
                 refreshWdg = None                         ):
        self.spListen = spListen
        self.clkListen = clkListen
        self.timeout = timeout
        self.restIsVisible = restIsVisible
        self.refreshWdg = refreshWdg
        if self.refreshWdg:
            self.restIsVisible = True
    
    def frameAttrs(self):
        ss =  ['Special wdg : {}'.format(self.refreshWdg)]
        ss += ['Space Listen: {}'.format(self.spListen)]
        ss += ['Clic Listen : {}'.format(self.clkListen)]
        ss += ['Timeout ms  : {}'.format(self.timeout)]
        ss += ['Estim. rest : {}'.format(self.restIsVisible)]
        return '\n'.join(ss)
    
class Sequence():
    def __init__(self,p = None, t = None):
        self.addIntroToSequence()
        if p:
            self.addPracticeToSequence(p)
        if t:
            self.addTestToSequence(t)
        self.addThanksToSequence()
            
    def addIntroToSequence(self):
        self.overview = ['intro']
        frame = Frame(spListen = True, refreshWdg = 'intro')
        self.allFrames = [frame]
    
    def addPracticeToSequence(self, tr_object):
        self.overview.append('practice')
        firstFrame = Frame(spListen = True, refreshWdg = 'pract')
        rateFrame  = Frame(clkListen = True)
        restFrame  = Frame(spListen = True, restIsVisible = True)
        partFrame  = Frame(refreshWdg = 'parcials', timeout = 5000)
        self.allFrames.append(firstFrame)
        self.pFrames = []
        for n, rate in enumerate(tr_object.data):
            self.pFrames.append('rate {}'.format(n+1))
            self.allFrames += [ rateFrame, restFrame ]
        self.allFrames[-1] = partFrame
        
    def addTestToSequence(self, tr_object):
        self.overview.append('test')
        firstFrame = Frame(spListen = True, refreshWdg = 'ready')
        rateFrame  = Frame(clkListen = True, timeout = 5000)
        restFrame  = Frame(spListen = True, restIsVisible = True)
        partFrame  = Frame(refreshWdg = 'parcials', timeout = 5000)
        pauseFrame = Frame(refreshWdg = 'pause', spListen = True)
        self.allFrames.append(firstFrame)
        self.tFrames = []
        for n, rate in enumerate(tr_object.data):
            self.tFrames.append('rate {}'.format(n+1))
            if n in TEST_PAUSES:
                self.allFrames[-1] = partFrame
                self.allFrames += [ pauseFrame, rateFrame, restFrame]
            elif n in TEST_PARTIALS:
                self.allFrames[-1] = partFrame
                self.allFrames += [ restFrame, rateFrame, restFrame]
            else:
                self.allFrames += [ rateFrame, restFrame ]
        self.allFrames[-1] = partFrame
        
    
    def addThanksToSequence(self):
        self.overview.append('thanks')
        thanksFrame= Frame(refreshWdg = 'thanks')
        self.allFrames.append(thanksFrame)
        
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
    for n in range(15):
        print('Frame {}:'.format(n))
        print(bothSeq.allFrames[n].frameAttrs())
        print('')