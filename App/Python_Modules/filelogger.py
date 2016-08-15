#!/usr/bin/python3 -tt
#-*- coding:utf-8 -*-

LOGDIR = '../../Logger'

stim_id = {'bars': 'B', 'dots': 'D'}
ans_id  = {'prop': 'PRP', 'ord': 'ORD'}

def testLogPath(uid, sess = 1, stim = None, ans = None):
    stimul_type = stim_id.get(stim,'n')
    answer_type = ans_id.get(ans, 'n')
    gm_type = stimul_type + answer_type
    fpath = '{}/{}_S{:02}_{}'.format(LOGDIR, uid, sess, gm_type)
    return fpath

def practiceLogPath(uid, sess = 1, stim = None, ans = None):
    stimul_type = stim_id.get(stim,'n')
    answer_type = ans_id.get(ans, 'n')
    gm_type = stimul_type + answer_type
    fpath = '{}/{}_P{:02}_{}'.format(LOGDIR, uid, sess, gm_type)
    return fpath
    

class Logger():
    def __init__(self, fpath):
        self.fpath = fpath
        self.initFile()
        
    def initFile(self):
        with open(self.fpath, 'w') as f:
            head = '{}\n'.format(self.fpath)
            f.write(head)
        
    def write(self, *args):
        with open(self.fpath, 'a')as f:
            arg_strings = [ str(arg) for arg in args ]
            line = ' '.join(arg_strings) + '\n'
            f.write(line)

if __name__ == "__main__":
    practPath = practiceLogPath('ABC')
    practLogger = Logger(practPath)
    n, t, r = (0, 3000, 0.3)
    practLogger.write(n, t, r)
    
    testPath  = testLogPath('ABC')
    testLogger  = Logger(testPath)
    n, t, r = (0,2500, 0.75)
    testLogger.write(n, t, r)
